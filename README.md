# Proxy Checker
httpのproxyを高速で動作確認する事が出来ます。

# ガイド
## 1 - ライブラリのインストール
ライブラリのインストールを行う必要があります。<br>
`requirements.txt`を利用して、楽にインストールできます。
```
pip install -r requirements.txt
```
必ずpython環境(バージョン`3.10.9`推奨)をPCにセットアップしておく必要があります。
## 2 - スクリプトを実行
ライブラリのインストールが完了したら、スクリプトを実行するだけです。<br>
以下の3つのどれかでpythonを実行する事が出来ます。
```
py main.py
python main.py
python3 main.py
```
## 3 - 設定
コンソールに「`Proxy File: `」と表示されたら、proxyが書いてあるtxtをd&dしてpathを指定します。<br>
pathを指定してエンダーキーを押すとproxyの確認が開始されます。

## 4 - 開始
コンソールに「`proxy loaded.`」と表示されると、確認が開始されたと言う意味です。<br>
また、コンソールに「`Check is complete.`」と表示されると、確認が完了したと言う意味です。<br>
動作したproxyはすべて「`working_proxies.txt`」に保存されます。

# 注意
- このツールは、httpのみ対応でsocks4やhttps等は非対応です。
- pythonツールのため、python環境とpip環境を整えて利用する必要があります。
- このツールはチェックのみを行い、収集は事前にしておく必要があります。
