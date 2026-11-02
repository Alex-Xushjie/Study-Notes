from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from services.excel import template
template(Path(__file__).resolve().parents[1]/'projects/example/test-plan.xlsx')
