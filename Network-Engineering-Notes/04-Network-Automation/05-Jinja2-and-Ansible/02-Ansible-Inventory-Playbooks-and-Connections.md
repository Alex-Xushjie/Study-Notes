# Ansible清单、Playbook与连接方式

[返回网络自动化目录](../Network-Automation.md)

## 1. Ansible的角色

控制端读取Inventory、变量和Playbook，通过选定连接方式执行模块。网络设备常用network_cli、netconf或httpapi等，设备侧未必运行Python；Linux主机模块与网络模块的前置条件不同。

Inventory定义主机与分组，Play按hosts选择范围，Task调用模块，Collection提供模块/插件。变量可能来自多个位置，必须理解优先级，避免组变量或命令行覆盖把测试目标替换成生产。

## 2. 最小离线Playbook

下面保存为render-local.yml，YAML顶层为Play列表。使用local连接，在控制端打印教学配置，不访问设备，也不写文件。需已安装ansible-core并确认控制端环境；原生Windows通常不作为受支持控制端，使用按官方支持的Linux/WSL等环境。

~~~yaml
- name: Render a local lab snippet
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    interface_name: Ethernet1
    interface_description: LAB uplink
  tasks:
    - name: Validate required values
      ansible.builtin.assert:
        that:
          - interface_name == 'Ethernet1'
          - interface_description == 'LAB uplink'
    - name: Show the planned snippet
      ansible.builtin.debug:
        msg: |
          interface {{ interface_name }}
           description {{ interface_description }}
~~~

用ansible-playbook -i localhost, render-local.yml执行；localhost后逗号表示内联清单形式。这里debug成功不是设备配置已生效，changed状态也不代表业务健康。

## 3. 连接真实设备前

明确ansible_connection、network_os、认证、主机密钥和必要的enable权限，按Collection文档设置。FQCN如cisco.ios.ios_command避免模块名称歧义；Collection与ansible-core有独立版本及依赖。

先用--list-hosts和--limit核对范围，再用一台隔离设备执行只读任务。不要把生产组默认作为所有Play的目标；不要在清单中硬编码明文密码。

## 4. 变量和结果

register保存任务结果，不能只检查rc就忽略模块返回结构。循环结果、unreachable、failed和skipped语义不同。条件表达式要处理缺字段与错误类型，缺数据不默认为设备合规。

## 5. 练习

完成本地Play，故意修改输入触发assert失败。之后接一个只读实验设备，保存清单展开、模块版本、任务结果和真实设备证据。把“本地渲染”与“设备执行”分别标注。

[Ansible网络入门](https://docs.ansible.com/ansible/latest/network/getting_started/index.html)、[变量优先级](https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html)、[控制端要求](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)。
