import textfsm

template_file = "interface.template"
with open(template_file) as template:
    fsm = textfsm.TextFSM(template)

    raw_data = """
    Interface   Status  Description
    Gi1/0/1    up      Server1
    Gi1/0/2    down    Printer
    Gi1/0/3    up      Switch
    """
parsed_data = [dict(zip(fsm.header.row)) for row in results]
print(parsed_data)
