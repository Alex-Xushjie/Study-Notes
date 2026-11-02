# 云网络分阶段实验与综合设计

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 先完成离线设计，再选平台实测

本篇分离线推导、小规模AWS/Azure实测、混合连接/容灾三档。不要求同时搭两家云，也不自动创建收费资源。CLI只读查询与新建日志分析也可能涉及权限/服务费用，先固定实验范围和预算。

没有账号仍可交付设计与故障推演，但在报告中标明未实测。已有[云实验C1–C4](../../../Network-Career-Lab/03-Cloud/02-Labs-and-Design.md)提供相同主线，本篇补充前置条件、证据与结课要求。

## 2. C1：AWS三网与本地DC

| 网络 | 实验前缀 | 要求 |
|---|---|---|
| Prod | 10.10.0.0/16 | 访问Shared/DC，不能直接到Dev |
| Dev | 10.20.0.0/16 | 访问Shared/DC，不能直接到Prod |
| Shared | 10.30.0.0/16 | 提供指定共享服务与返回路径 |
| DC | 10.100.0.0/16 | 依业务规则访问云侧 |

为每个VPC写业务子网表；为TGW写workload/shared/dc表、入口关联及路由传播。DX/VPN场景说明实际Attachment类型，不把DX电路本身画成任意直接TGW端口。

逐跳演算Prod→Shared、Dev→Prod拒绝、DC→Dev及返回。故障注入为删除Shared回程、Dev误关联shared、发布重叠CIDR、主接入撤路由。离线测试只能验证逻辑，不证明TGW真实安装或云网关收敛。

## 3. C2：Azure集中检查

Hub 10.40.0.0/16、App 10.50.0.0/16、Data 10.60.0.0/16。App→Data TCP5432必须经Hub检查，其他不需要的跨区流量拒绝。列双向UDR、Peering选项、NSG、Firewall/NVA状态与有效路由。

故意只配置App侧路径，分析Data是否从另一可达路径返回。不要为追求案例结果新增不合理路径；如果现有拓扑根本无直达回程，就说明会黑洞而非假定一定非对称。

## 4. C3：最小云实机

只选一家云、一个隔离网络、两子网和两台小型Linux测试机。记录账号/订阅、区域/AZ、实例、网卡与子网ID。主机可用10.10.1.10/24与10.10.2.10/24，但必须按云分配机制取得合法IP，不能在OS随意设置未分配地址。

测试服务在服务端私网IP启动。先进入空的临时测试目录，防止暴露真实文件：

~~~bash
python3 -m http.server 8000 --bind 10.10.2.10
~~~

仅允许实验客户端访问TCP8000，不开放公网；Ctrl+C停止。客户端测试：

~~~bash
ip route get 10.10.2.10
curl --connect-timeout 3 --max-time 10 -v http://10.10.2.10:8000/
~~~

Python程序未安装或地址未分配会失败；先满足前置条件。ip route展示主机视角，云侧有效路由与安全另查。

每次只改变一个条件：服务监听、平台允许规则、子网路由/关联。先预测结果，再保存请求、主机状态及平台证据，随后恢复。不要通过全局放开规则来“修复实验”。

## 5. 只读云状态查询

AWS示例先确认身份和区域，VPC ID必须换成实际实验资源ID。以下命令不创建/修改资源，返回内容仍需脱敏：

~~~bash
aws sts get-caller-identity
aws ec2 describe-route-tables --region ap-southeast-1 --filters Name=vpc-id,Values=vpc-EXAMPLE
~~~

Azure示例中的资源组/NIC名称也需替换，订阅必须先由你确认：

~~~bash
az account show --output table
az network nic show-effective-route-table --resource-group rg-network-lab --name nic-lab-app
az network nic list-effective-nsg --resource-group rg-network-lab --name nic-lab-app
~~~

只读API需要相应权限和资源状态；报权限错误不能证明网络故障。命令不可用先核对CLI版本/帮助，不改现网角色权限来绕过实验问题。

## 6. C4：DNS与私有访问

离线设计双向条件转发和私有区可见性。若已有隔离端点/Resolver环境，再验证云VM与本地同一服务名的CNAME/A/AAAA、TTL与最终连接。新建端点、Resolver或日志之前先估算费用，不作为基础实验强制项。

注入错误转发、缺失区关联、正确私网解析但无路由、网络正常但权限拒绝。每种至少给一个能排除其他候选的证据。

## 7. C5：综合设计与故障验收

两DC、两云区域、Prod/Dev/Shared、双接入位置、VPN备份。提交IPAM、资源归属、双向路由、DNS、安全服务链、N-1容量、费用假设和恢复Runbook。工业/能源生产控制业务的云接入适用性单独列为评审边界。

| 验收维度 | 必交证据 |
|---|---|
| 可达与回程 | 至少三条完整逐跳路径 |
| 隔离 | 允许与拒绝矩阵及实际/推演证据 |
| 私有访问 | DNS、网络、TLS与权限分别确认 |
| 容灾 | 单线路、接入位置、AZ/区域与共享依赖 |
| 容量与费用 | 正常/N-1、配额与明确假设 |
| 排错 | 路由、DNS、状态检查三个不同RCA |

## 8. 清理与复核

清理前列出精确实验资源ID与依赖，按云平台流程只处理本次测试资源；不使用按名称模糊匹配的一键批量删除。测试实例结束后仍可能有磁盘、IP、NAT、端点、日志、快照或连接费用，查剩余资源与账单。

最终报告注明“离线/软件/云实测/真实线路”，引用[实验记录模板](../../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)。本次教材编写未运行上述云命令或创建任何云资源。

[AWS路由表CLI](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-route-tables.html)、[Azure NIC CLI](https://learn.microsoft.com/en-us/cli/azure/network/nic?view=azure-cli-latest)。
