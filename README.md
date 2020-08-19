# n575_slackbot

## はじめに
このbotをあなたのワークスペースに導入すると任意のチャンネルで誰かの発言に含まれている575を検出できます。  
導入されたbotは誰でも遊べますが、botを導入するには権限が必要になります。  
もしあなたに権限がないなら、偉い人に相談して権限をもらうか、偉い人にこれをやらせるかしてください。  

## bot作成編
https://api.slack.com/apps?new_granular_bot_app=1 にアクセスするとこんな画面が出るので、App nameには`n575_bot` を入力し、Development Slack Workspaceではあなたがbotを導入したいworkspaceを選びましょう。  
<img src="https://i.imgur.com/UG6ZDFk.png" width=50%>  
入力したら右下のCreate appボタンが緑色になるので押しましょう。  

botは生まれた瞬間は全く権限を持っていません。  
なので、左サイドバーの OAuth & Permission から権限を与えてあげる必要があります。  
<img src="https://i.imgur.com/nYTOziF.png" width=20%>

OAuth & Permissionのページを下の方にスクロールしていくと、Scopesというのがあると思います。  
<img src="https://i.imgur.com/TBOKNTE.png" width=50%>  

ここでbotに様々な権限を与えられます。  
脳死で全部与えても良いですが、乗っ取られたりすると悲しくなるのでここではn575_botが使用する権限だけ与えます。  
Add an OAuth Scope を押し、`chat:write`と`users:read`を選択しましょう。  

選択後、ページの一番上までスクロールすると`Install App to Workspace`が緑色になっているのでポチッと押しましょう。  
<img src="https://i.imgur.com/SfYlNXF.png" width=50%>  

確認画面が出るので、もしOKなら `許可する` を押しましょう。  
<img src="https://i.imgur.com/Q37QLlG.png" width=50%>  

許可するを押すと、元いた画面に戻り、謎の文字列が表示されていると思います。  
<img src="https://i.imgur.com/S0tYTmL.png" width=50%>  

この文字列は秘密の文字列なので他人に教えたりgitにpushしたりしないようにしましょう。  

## PythonでMeCabを使えるようにする
このbotでは575を検出するのにMeCabを使っています。  
また、新語等に対応するためにNEologd辞書を使用しています。  
細かい設定については本筋から離れるのでしませんが、以下のリンクが参考になると思います。  
ubuntu: https://qiita.com/ekzemplaro/items/c98c7f6698f130b55d53  
Mac: https://qiita.com/berry-clione/items/b3a537962c84244a2a09  
ちゃんと使える状態になっているかは[test_macab.py](https://github.com/1234567890Joe/n575_slackbot/blob/master/test_macab.py)を実行して、横浜流星が1単語になっているかで確認できます。  

## slackでメッセージを投げた時にそれを拾ってくれるサーバーを作る
あなたのターミナル上で下記のコマンドを順番に実行してください  
`git clone git@github.com:1234567890Joe/n575_slackbot.git`  
`pip install -r requuirements.txt`  
`export SLACK_BOT_TOKEN=xoxb-XXXXXXXXXXXX-xxxxxxxxxxxx-XXXXXXXXXXXXXXXXXXXXXXXX`  
=の後にはさっきの秘密の文字列を入れましょう。  
`export SLACK_SIGNING_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`  
=の後には、Signing Secretを入れます。  
Signing Secretは左サイドバーの Basic Informationをクリックして、下にスクロールしていくと App Credentials という場所があります。  
この中のSigning Secretを入れます。(このSigning Secretも秘密なので扱いには気を付けましょう)  
`FLASK_ENV=development python app.py`

```
ローカルでこれを実行している場合、リクエストをパブリックURLからマシンにトンネリングする必要があります。  
トンネルの設定にはngrokをお勧めします。  
ngorkは https://ngrok.com/ でアカウントを作れば後は表示される通りにコマンドを実行していけば行けます。  
./ngrok http 80 みたいなコマンドが最後に載っていると思いますが、app.pyの一番下の行に書いてある`app.run(port=3000)`で指定したポート番号に変えましょう。(今回なら3000)
```


## slackでメッセージを投げた時にそれをbotが見れるようにする
左サイドバーから Event Subscriptions を選び、Enable Events をOnにしましょう。  
Enable Eventsをポチッと押して、botが見れるeventを追加しましょう。  
Request URLにはngorkのコマンドを叩いた時に
`Forwarding http://hoge.ngrok.io -> http://localhost:3000` みたいに出るので、 `http://hoge.ngrok.io`に`/slack/events`を足して入力しましょう。  
入力例: `http://hoge.ngrok.io/slack/events`  
Add Bot User Eventの`message.channels`の権限を追加します。  
save changeを押して、reinstallすればめんどくさい作業は大体終わりです。  

## 実際にslackで575を見つけよう
任意のチャンネルに作成したbotをinviteして、そのチャンネルで575を発言してみましょう。  
こんな感じになります。楽C  
<img src="https://i.imgur.com/SxImWqd.png" width=80%>  
