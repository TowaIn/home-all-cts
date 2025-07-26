#!/bin/bash
CONFIG_FILE="/home/toin/git/home-all-cts/jenkins/scripts/pod_list.conf"

if [ "$#" -ne 2 ]; then
  echo "使い方: $0 <stop|start> <ターゲット>"
  exit 1
fi

 CONTROLL=$1
   TARGET=$2
MAX_RETRY=10
 INTERVAL=10

while IFS=',' read -r name resource namespace; do

  case "$name" in
    *"$TARGET"*)

      if [ "$CONTROLL" = "stop" ]; then
        echo "${name}の停止を開始します..."
        kubectl scale ${resource} ${name} --replicas=0 ${namespace}

        for i in $(seq 1 $MAX_RETRY); do
          if ! kubectl get po ${namespace} | grep $name > /dev/null; then
            echo "${name}は正常に停止しました"
            break
          fi
          sleep $INTERVAL
        done

      elif [ "$CONTROLL" = "start" ]; then
        echo "${name}の起動を開始します..."
        kubectl scale ${resource} ${name} --replicas=1 ${namespace}

        for i in $(seq 1 $MAX_RETRY); do
          STATUS=$(kubectl get po ${namespace} | grep $name | awk '{print $3}')
          if [ "$STATUS" = "Running" ]; then
            echo "${name}は正常に起動しました"
            break
          fi
          sleep $INTERVAL
        done

      else
        echo "ERROR: 不明なアクション '${CONTROLL}' です。"
        exit 1
      fi
      ;;
  esac
done < "$CONFIG_FILE"

kubectl get po -A
exit 0
