# home-all-cts

## 概要
自宅サーバで運用しているアプリケーションコンテナのソースコード、マニフェストのすべて

## 構成
Ubuntu上のmicrok8sで各コンテナを実行している

ingressコントローラーとcloudflaredコンテナを挟み外部に公開

OpenWebUIと接続しているAIモデルのみ、ollamaを使用しローカルで動作させている

## Secretについて
SecretはbitnamiのSealed Secretsを用いて暗号化している

作成手順は以下の通り

1. Secretのyamlファイルを作成
2. 下記コマンドで暗号化版を生成
```
kubeseal --format yaml < secret.yaml > sealedsecret.yaml
```
