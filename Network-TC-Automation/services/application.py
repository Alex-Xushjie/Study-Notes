"""UI-independent SSH application service."""
from core.engine import Engine
from core.scheduler import Scheduler
from storage.evidence import EvidenceStore

def run(adapter,tasks,devices,evidence_root):
    return Scheduler().run(Engine(adapter,EvidenceStore(evidence_root)),tasks,devices)
