import csv,json,tempfile,unittest
from pathlib import Path
from core.models import Device,Task
from core.engine import Engine
from storage.evidence import EvidenceStore,history,review
from storage.project import load,save
from services.templates import apply
from services.reporting import export_index

class RoundOneTests(unittest.TestCase):
    def test_multistep_failure_preserves_success_and_retest(self):
        class Adapter:
            hostname='CE-1';prompt='CE-1#'
            def execute(self,d,c):
                if c=='bad':raise RuntimeError('offline')
                return 'CE-1#'+c+'\nok\nCE-1#'
        with tempfile.TemporaryDirectory() as root:
            d=Device('r','192.0.2.1');task=Task('1','r','show version','quick',name='Identity',section='Basic',steps=['show version','bad'],criteria='approved version')
            result=Engine(Adapter(),EvidenceStore(root)).run(task,d)
            self.assertEqual(result.execution_status,'ERROR');self.assertEqual(len(result.step_results),2);self.assertIn('ok',result.output)
            review(result.evidence_dir,'N/A','not applicable','observed')
            output=Path(root)/'index.csv';export_index(root,output)
            with output.open(encoding='utf-8-sig',newline='') as f:row=list(csv.DictReader(f))[0]
            self.assertEqual(row['Review'],'N/A');self.assertEqual(row['Actual Result'],'observed');self.assertEqual(row['Section'],'Basic');self.assertTrue(Path(row['Metadata']).exists())
    def test_old_project_and_template_roundtrip(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'project.json';p.write_text(json.dumps({'schema_version':1,'name':'Old','devices':[{'id':'r','host':'192.0.2.1','platform':'cisco_ios'}],'tasks':[{'id':'1','device_id':'r','command':'show version','source':'quick'}]}))
            name,devices,tasks=load(p);self.assertEqual(tasks[0].steps,[])
            tasks=apply(devices,['Basic / NTP','Routing / OSPF']);self.assertEqual(len(tasks[0].steps),3)
            save(p,name,devices,tasks);self.assertEqual(load(p)[2],tasks)
    def test_excel_extended_and_grouped_gui(self):
        from openpyxl import Workbook
        from services.excel import load as import_excel
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'plan.xlsx';book=Workbook();w=book.active;w.title='Devices';w.append(['Hostname','Management IP','Platform']);w.append(['r','192.0.2.1','cisco_ios'])
            w=book.create_sheet('Test Cases');w.append(['Test ID','Hostname','Command','Test Name','Section','Steps','Criteria','Logical Group']);w.append(['1','r','show version','Identity','Basic','show version\nshow inventory','approved','Stack-A']);book.save(p)
            devices,tasks=import_excel(p);self.assertEqual(tasks[0].steps,['show version','show inventory']);self.assertEqual(tasks[0].logical_group,'Stack-A')
