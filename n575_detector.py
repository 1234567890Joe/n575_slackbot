import MeCab
import subprocess
from kanjize import int2kanji


def yomi_to_mora(yomi):
    small_num = yomi.count("ャ") + yomi.count("ュ") + yomi.count("ョ") + yomi.count(
        "ァ") + yomi.count("ィ") + yomi.count("ゥ") + yomi.count("ェ") + yomi.count("ォ")
    return len(yomi) - small_num


def n575_detector(text):
    cmd = 'echo `mecab-config --dicdir`"/mecab-ipadic-neologd"'
    path = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             shell=True).communicate()[0]).decode('utf-8')
    m = MeCab.Tagger("-d {0}".format(path))

    text = text.replace(' ', '')
    text = text.replace('¥n', '')
    node = m.parseToNode(text)
    all_list = []
    while node:
        hinshi = node.feature.split(",")[0]
        if hinshi != "BOS/EOS":
            try:
                int(node.surface.split()[0])
            except ValueError:
                all_list.append(node.surface.split()+node.feature.split(","))
            else:
                # 数字はMecab君が読めないので、漢数字に一旦直してlistに追加する
                number_parsed = m.parse(
                    int2kanji(int(node.surface.split()[0]))).split()
                tmp = number_parsed[1].split(",")
                tmp.insert(0, node.surface.split()[0])
                all_list.append(tmp)
        node = node.next

    now_mora = 0
    haiku = ""
    first_index = 0
    haiku_list = []

    for i in all_list:
        if i[1] == "記号":
            haiku += i[0]
            continue
        if i[7] == "*" and len(i) != 10:
            continue
        else:
            mora = yomi_to_mora(i[9])
            now_mora += mora
        haiku += i[0]
        if now_mora > 17:
            while 1:
                first = all_list[first_index]
                if first[1] == "記号":
                    first_index += 1
                    haiku = haiku.lstrip(first[0])
                elif first[7] == "*" and len(first) != 10:
                    continue
                else:
                    now_mora -= yomi_to_mora(first[9])
                    haiku = haiku.lstrip(first[0])
                    first_index += 1
                if now_mora <= 17:
                    break
        if now_mora == 17:
            first = all_list[first_index]
            end = i
            if first[1] == "名詞" and first[2] != "非自立":
                if end[1] == "動詞" or end[1] == "形容詞" or end[1] == "形容動詞" or end[1] == "名詞" or end[1] == "助動詞":
                    print("n575: " + haiku)
                    haiku_list.append(haiku)

    return haiku_list
