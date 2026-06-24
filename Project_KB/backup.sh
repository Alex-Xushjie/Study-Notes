#!/bin/bash
mkdir -p backups
echo "正在导出数据库..."
docker compose exec -t db pg_dump -U wikijs wikijs > backups/db_backup.sql

echo "正在使用 AES-256 加密..."
openssl enc -aes-256-cbc -salt -pbkdf2 -in backups/db_backup.sql -out backups/db_backup.enc -k Xsj@951224

rm backups/db_backup.sql
echo "备份成功，已生成安全的加密文件：backups/db_backup.enc"