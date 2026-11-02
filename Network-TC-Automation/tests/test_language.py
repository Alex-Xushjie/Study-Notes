import unittest
from PySide6.QtWidgets import QApplication,QPushButton,QLabel
from PySide6.QtCore import Qt
from gui import i18n
from gui.main import MainWindow
from core.models import Device,Task

class LanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])
    def test_switch_preserves_data_and_checks(self):
        old=i18n.language
        try:
            i18n.set_language('zh');w=MainWindow()
            w.devices=[Device('CE-1','192.0.2.1','cisco_ios')];w.tasks=[Task('one','CE-1','show version','quick')];w.refresh()
            w.task_table.item(0,0).setCheckState(Qt.Unchecked);w.password.setText('test');w.did.setText('unsaved-host')
            w.language_selector.setCurrentIndex(1)
            self.assertEqual(w.nav.item(1).text(),'Devices')
            self.assertEqual(w.device_table.horizontalHeaderItem(1).text(),'Address')
            self.assertIn('Add device',[b.text() for b in w.findChildren(QPushButton)])
            self.assertEqual(w.task_table.item(0,0).checkState(),Qt.Unchecked)
            self.assertEqual(w.password.text(),'test');self.assertEqual(w.did.text(),'unsaved-host')
            self.assertEqual(w.tasks[0].command,'show version');self.assertEqual(w.library_id.itemData(0),'system.version')
            self.assertEqual(i18n.settings.value('language'),'en')
            w.language_selector.setCurrentIndex(0)
            self.assertEqual(w.device_table.horizontalHeaderItem(0).text(),'主机名')
            self.assertEqual(w.nav.item(1).text(),'设备');w.close()
        finally:i18n.set_language(old)
    def test_catalog_covers_ui_literals(self):
        import ast
        from pathlib import Path
        root=ast.parse(Path('gui/main.py').read_text(encoding='utf-8'))
        for node in ast.walk(root):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='tr' and node.args and isinstance(node.args[0],ast.Constant):
                self.assertIn(node.args[0].value,i18n.CATALOG)
