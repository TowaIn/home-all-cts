# home-all-cts

## 概要
自宅サーバで運用しているアプリケーションコンテナのソースコード、マニフェストのすべて

## 構成
Ubuntu上のmicrok8sで各コンテナを実行している

ingressコントローラーとcloudflaredコンテナを挟み外部に公開

なお、OpenWebUIと接続しているAIモデルのみ、ollamaを使用しローカルで動作させている
