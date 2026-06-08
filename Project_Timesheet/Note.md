从本地复制项目到Ubuntu（由于/opt/通常需要root权限，scp可能会因为权限失败，建议先复制到home目录
```bash
scp -r C:\Users\shengchie\Desktop\Project_Timesheet alexxu@192.168.153.131:/home/alexxu/
```
登录Ubuntu后再移动到/opt
```bash
sudo mv ~/Project_Timesheet /opt/
sudo chown -R alexxu:alexxu /opt/Project_Timesheet
cd /opt/Project_Timesheet
```
启动项目
```bash
docker compose up -d --build
```
检查
```bash
docker ps
```
测试后端
```bash
curl http://localhost:8000
curl http://localhost:8000/health
```
