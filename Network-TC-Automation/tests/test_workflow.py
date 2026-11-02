import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from core.models import Device, Task
from adapters.ssh import SSHAdapter
from tests.fakes import MockAdapter
from core.engine import Engine
from core.scheduler import Scheduler
from storage.evidence import EvidenceStore, history, review
from storage import project
from services import excel

class WorkflowTests(unittest.TestCase):
    def test_project_roundtrip_and_validation(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'project.json'; d=Device('r','192.0.2.1','cisco_ios',2222,'user')
            t=Task('tc','r','show version','quick')
            project.save(p,'Lab',[d],[t]); self.assertEqual(project.load(p),('Lab',[d],[t]))
            self.assertNotIn('password',p.read_text())
            with self.assertRaises(ValueError): project.validate([d,d],[t])
            with self.assertRaises(ValueError): project.validate([], [t])
    def test_excel_template_and_invalid_device(self):
        from openpyxl import load_workbook
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'test.xlsx'; excel.template(p); devices,tasks=excel.load(p)
            self.assertEqual(tasks[1].command,'show ip interface brief'); self.assertEqual(tasks[0].source,'excel')
            book=load_workbook(p); book['Test Cases']['B2']='missing'; book.save(p); book.close()
            with self.assertRaisesRegex(ValueError,'2'): excel.load(p)
    def test_cancel_and_review_preserves_original(self):
        with tempfile.TemporaryDirectory() as root:
            d=Device('r','x'); tasks=[Task('1','r','display version','quick'),Task('2','r','display version','quick')]
            stop=[False]
            def done(r): stop[0]=True
            results=Scheduler().run(Engine(MockAdapter(),EvidenceStore(root)),tasks,{'r':d},lambda:stop[0],done)
            self.assertEqual(len(results),1); record=history(root)[0]; self.assertEqual(record['device_name'],'r')
            folder=Path(record['evidence_dir']); original=(folder/'result.json').read_bytes()
            review(folder,'PASS','checked'); self.assertEqual((folder/'result.json').read_bytes(),original)
            self.assertEqual(next(folder.glob('*.txt')).read_bytes(),results[0].output.encode())
    def test_readable_names_collision_and_legacy_filter(self):
        with tempfile.TemporaryDirectory() as root:
            d=Device('CE-1','192.0.2.1'); store=EvidenceStore(root)
            engine=Engine(MockAdapter(),store); t=Task('TC-1','CE-1','show ip interface brief','quick')
            first=engine.run(t,d); second=engine.run(t,d)
            self.assertNotEqual(first.evidence_dir,second.evidence_dir)
            self.assertTrue(Path(first.evidence_dir).name.startswith('CE-1-192.0.2.1-show_ip_interface_brief-'))
            self.assertTrue(any(p.name.startswith('CE-1-192.0.2.1-') for p in Path(first.evidence_dir).glob('*.png')))
            legacy=Path(root)/'old'/'mock'; legacy.mkdir(parents=True)
            (legacy/'result.json').write_text(json.dumps({'simulated':True}))
            self.assertEqual(len(history(root)),2)
            with self.assertRaises(ValueError): project.validate([Device('r','router.local')],[])

    def test_ssh_parameters_and_credential_redaction(self):
        d=Device('r','192.0.2.1','cisco_ios',2222,'device-user')
        with patch('netmiko.ConnectHandler') as connect:
            connect.return_value.__enter__.return_value.find_prompt.return_value='CE-1#'
            connect.return_value.__enter__.return_value.send_command.return_value='show version\nok\nCE-1#'
            self.assertEqual(SSHAdapter('fallback','secret',12).execute(d,'show version'),'CE-1#show version\nok\nCE-1#')
            self.assertFalse(connect.return_value.__enter__.return_value.send_command.call_args.kwargs['strip_prompt'])
            self.assertEqual(connect.call_args.kwargs['port'],2222)
            self.assertEqual(connect.call_args.kwargs['username'],'device-user')
            self.assertTrue(connect.call_args.kwargs['ssh_strict'])
            connect.side_effect=RuntimeError('secret')
            with self.assertRaises(RuntimeError) as caught: SSHAdapter('u','secret').execute(d,'show version')
            self.assertNotIn('secret',str(caught.exception))

class GuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PySide6.QtWidgets import QApplication
        cls.app=QApplication.instance() or QApplication([])
    def test_background_run_and_history(self):
        from PySide6.QtTest import QTest
        from gui.main import MainWindow
        with tempfile.TemporaryDirectory() as root:
            w=MainWindow(); self.assertEqual(w.stack.count(),6)
            w.devices=[Device('r','192.0.2.1','cisco_ios',22,'lab',password='test')]; w.tasks=[Task('1','r','show version','quick'),Task('2','r','show ip interface brief','quick')]; w.path=Path(root)/'project.json'; w.save_project()
            self.assertEqual(len(w.devices),1); self.assertEqual(len(w.tasks),2)
            w.show(); w.password.setText('test')
            with patch('gui.main.SSHAdapter',return_value=MockAdapter()), patch('gui.main.QMessageBox.question',return_value=16384):
                w.start(w.tasks)
            for _ in range(200):
                QTest.qWait(25)
                if w.worker is None: break
            self.assertIsNone(w.worker); self.assertEqual(w.progress.value(),2); self.assertEqual(len(w.rows),2)
            self.assertFalse(hasattr(w,'mode')); self.assertFalse(hasattr(w,'load_demo')); w.result_table.selectRow(0)
            self.assertIn('SIMULATED',w.output.toPlainText()); w.close()

if __name__=='__main__':unittest.main()
