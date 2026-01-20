# from netmiko import ConnectHandler

# device = {
#     'device_type': 'cisco_ios',
#     'host': '10.160.14.9',
#     'username': 'cisco',
#     'password': 'Cisco123'}
# net_connect = ConnectHandler(**device)
# output = net_connect.send_command('show ip int brief')
# print(output)
# net_connect.disconnect()

import time

cmd = input('C:\Administrator> ')
ip_str = cmd.split('ping')[1].strip()
print(f'来自 {ip_str} 的回复: 请求超时')
