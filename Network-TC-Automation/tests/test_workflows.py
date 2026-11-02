import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from services.workflows import Session,templates,validate
from core.models import Device

def plan():
    return {'version':1,'name':'Uplink','steps':[
        {'kind':'collect','title':'Baseline','targets':['r'],'commands':['show version']},
        {'kind':'fault_manual','title':'Unplug','instruction':'Unplug r e0/1'},
        {'kind':'collect','title':'Fault','targets':['r'],'commands':['show ip interface brief']},
        {'kind':'restore_manual','title':'Restore','instruction':'Reconnect r e0/1'},
        {'kind':'collect','title':'Recovery','targets':['r'],'commands':['show ip interface brief']},
        {'kind':'review','title':'Review'}]}

class WorkflowTests(unittest.TestCase):
    def test_missing_restore_rejected(self):
        p=plan();p['steps'].pop(3)
        with self.assertRaises(ValueError):validate(p,{'r':None})
    def test_templates_and_placeholders(self):
        self.assertEqual(len(templates()),9)
        p=plan();validate(p,{'r':None})
        p['steps'][0]['commands']=['show interface {interface}']
        with self.assertRaises(ValueError):validate(p,{'r':None})
    def test_abort_and_resume_require_restore(self):
        with tempfile.TemporaryDirectory() as root:
            p=plan();session=Session.create(root,p);p['name']='changed'
            self.assertEqual(session.data['plan']['name'],'Uplink')
            session.complete(evidence=['baseline']);session.arm();session.complete('unplugged')
            resumed=Session.load(session.path);self.assertTrue(resumed.data['needs_restore'])
            resumed.abort('stop');self.assertEqual(resumed.data['index'],3);self.assertEqual(resumed.data['state'],'recovering')
            resumed.complete('reconnected');self.assertFalse(resumed.data['needs_restore'])
            self.assertTrue(resumed.data['aborted']);self.assertGreater(len(resumed.data['events']),3)
    def test_pre_fault_abort(self):
        with tempfile.TemporaryDirectory() as root:
            s=Session.create(root,plan());s.abort('baseline bad');self.assertEqual(s.data['state'],'aborted')

class WorkflowGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PySide6.QtWidgets import QApplication
        cls.app=QApplication.instance() or QApplication([])
    def test_editor_and_manual_recovery(self):
        from gui.workflow import WorkflowDialog,StepEditor
        from PySide6.QtWidgets import QMessageBox
        with tempfile.TemporaryDirectory() as root:
            w=WorkflowDialog([Device('r','192.0.2.1','cisco_ios',username='lab',password='test')],Path(root)/'evidence',5)
            self.assertEqual(w.preset.count(),9)
            editor=StepEditor(plan()['steps'][1],{'r':None});self.assertEqual(editor.value()['kind'],'fault_manual')
            w.plan={'version':1,'name':'Manual','steps':[plan()['steps'][1],plan()['steps'][3],plan()['steps'][-1]]};w.refresh()
            with patch('gui.workflow.QMessageBox.question',return_value=QMessageBox.Yes):
                w.start();self.assertTrue(w.session.data['needs_restore']);w.advance()
                w.abort();self.assertEqual(w.session.data['state'],'recovering');w.advance()
            self.assertFalse(w.session.data['needs_restore'])
            with patch('gui.workflow.QInputDialog.getItem',return_value=('REVIEW',True)):w.advance()
            self.assertEqual(w.session.data['state'],'completed');self.assertTrue(w.session.path.exists());w.close()
    def test_collection_worker_and_cli_are_mocked(self):
        from gui.workflow import StepWorker
        class Adapter:
            hostname='r';prompt='r#'
            def execute(self,d,c):return 'r#'+c+'\nok\nr#'
            def configure(self,d,commands):return 'r(config)#'+str(commands)
        with tempfile.TemporaryDirectory() as root:
            for kind in ('collect','fault_cli'):
                step={'kind':kind,'title':kind,'targets':['r'],'commands':['show version']}
                worker=StepWorker(step,{'r':Device('r','192.0.2.1')},root,5);captured=[];worker.done.connect(lambda paths,error:captured.append((paths,error)))
                with patch('gui.workflow.SSHAdapter',return_value=Adapter()):worker.run()
                self.assertEqual(captured[0][1],'');self.assertTrue((Path(captured[0][0][0])/'result.json').exists())
