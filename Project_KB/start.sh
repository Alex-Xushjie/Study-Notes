#!/bin/bash
mkdir -p db_data wiki_data backups
sudo docker compose up -d
echo "=========================================="
echo "知识库系统已启动！"
echo "请在浏览器访问: http://10.34.45.45:8080"
echo "=========================================="