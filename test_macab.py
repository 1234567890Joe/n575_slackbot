import sys
import MeCab
import subprocess

cmd = 'echo `mecab-config --dicdir`"/mecab-ipadic-neologd"'
path = (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
m = MeCab.Tagger("-d {0}".format(path))

print(m.parse("横浜流星"))
