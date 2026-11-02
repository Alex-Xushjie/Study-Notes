import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from core.models import Device, Task
from core.engine import Engine
from tests.fakes import MockAdapter
from storage.evidence import EvidenceStore
from services.tasks import quick, library
class EngineTests(unittest.TestCase):
    def test_sources_and_evidence(self):
        d = Device('d','192.0.2.1')
        with TemporaryDirectory() as root:
            engine = Engine(MockAdapter(), EvidenceStore(root))
            for task in [library(d,'system.version'), quick(d,'display version'), Task('excel','d','display version','excel','Version')]:
                self.assertNotEqual(engine.run(task,d).status,'ERROR')
            self.assertEqual(len(list(Path(root).rglob('*.txt'))),3)
            self.assertEqual(len(list(Path(root).rglob('*.png'))),3)
    def test_failure(self):
        class Broken:
            def execute(self,*args): raise RuntimeError('offline')
        with TemporaryDirectory() as root:
            self.assertEqual(Engine(Broken(),EvidenceStore(root)).run(Task('t','d','show version','quick'),Device('d','x')).status,'ERROR')
    def test_expectation(self):
        with TemporaryDirectory() as root:
            self.assertEqual(Engine(MockAdapter(),EvidenceStore(root)).run(Task('t','d','show version','excel','missing'),Device('d','x')).status,'FAIL')
if __name__ == '__main__': unittest.main()
