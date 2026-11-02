import unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
from core.models import Device
from storage.project import save,load
from adapters.ssh import SSHAdapter
class CredentialsTests(unittest.TestCase):
    def test_encrypted_roundtrip(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'project.json';d=Device('r','192.0.2.1','cisco_ios',username='lab',password='unique-test-secret')
            save(path,'Lab',[d],[])
            self.assertNotIn('unique-test-secret',path.read_text());self.assertEqual(load(path)[1][0].password,'unique-test-secret')
            self.assertNotIn('unique-test-secret',repr(d))
    def test_device_password_used(self):
        with patch('netmiko.ConnectHandler') as connect:
            c=connect.return_value.__enter__.return_value;c.find_prompt.return_value='r#';c.send_command.return_value='show version\nok\nr#'
            adapter=SSHAdapter('fallback','fallback')
            for name,password in [('one','p1'),('two','p2')]:
                adapter.execute(Device(name,'192.0.2.1','cisco_ios',username=name,password=password),'show version')
                self.assertEqual(connect.call_args.kwargs['username'],name);self.assertEqual(connect.call_args.kwargs['password'],password)
    def test_excel_credentials(self):
        from services.excel import template,load as import_excel
        from openpyxl import load_workbook
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'devices.xlsx';template(path);book=load_workbook(path);ws=book['Devices'];headers=[c.value for c in ws[1]];ws.cell(2,headers.index('Password')+1,'excel-secret');book.save(path);book.close()
            devices,tasks=import_excel(path);self.assertEqual(devices['R1'].password,'excel-secret')
