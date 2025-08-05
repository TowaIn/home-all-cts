#!/bin/bash

DEPLOYMENT_NAME="open-webui"
CONTAINER_NAME="open-webui"
TARGET_STATUS="False"
set -e

cat <<EOF > /tmp/openwebui-auth-patch.yaml
spec:
  template:
    spec:
      containers:
      - name: ${CONTAINER_NAME}
        env:
        - name: WEBUI_AUTH
          value: "${TARGET_STATUS}"
        - name: ENABLE_PERSISTENT_CONFIG
          value: "${TARGET_STATUS}"
EOF

kubectl patch deployment "${DEPLOYMENT_NAME}" \
  --patch-file /tmp/openwebui-auth-patch.yaml

echo "${DEPLOYMENT_NAME} をログイン不要モードに切り替えました"

rm /tmp/openwebui-auth-patch.yaml