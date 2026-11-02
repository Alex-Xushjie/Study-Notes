from gui.i18n import tr, message
from gui import i18n
import sys, json, shutil
from pathlib import Path
from dataclasses import asdict, replace
from threading import Event
from PySide6.QtCore import QThread, Signal, Qt, QUrl, QTranslator, QLibraryInfo
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QPushButton, QLabel, QLineEdit, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog, QMessageBox, QInputDialog, QProgressBar, QAbstractItemView
from core.models import Device, Task
from core.engine import Engine
from core.scheduler import Scheduler
from adapters.ssh import SSHAdapter
from adapters.profiles import PROFILES
from services.tasks import quick, library, deduplicate
from services import excel
from services.templates import TEMPLATES, apply as apply_templates
from services.reporting import export_index
from storage import project
from storage.evidence import EvidenceStore, history, review
from gui.pages import projects, devices, execution, results, evidence, settings
BASE = Path(__file__).resolve().parents[1]

class Worker(QThread):
    item = Signal(object)
    failed = Signal(str)

    def __init__(self, adapter, tasks, devices, root):
        super().__init__()
        self.adapter = adapter
        self.tasks = tasks
        self.devices = devices
        self.root = root
        self.stop = Event()

    def run(self):
        try:
            Scheduler().run(Engine(self.adapter, EvidenceStore(self.root)), self.tasks, self.devices, self.stop.is_set, self.item.emit)
        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            self.adapter = None

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Network T&C Automation')
        self.resize(1250, 820)
        self.devices = []
        self.tasks = []
        self.rows = []
        self.path = None
        self.worker = None
        self.dirty = False
        self.pages = {}
        self.locked = []
        shell = QWidget()
        layout = QHBoxLayout(shell)
        self.nav = QListWidget()
        self.stack = QStackedWidget()
        for module in (projects, devices, execution, results, evidence, settings):
            page = module.Page()
            name = page.title
            self.pages[name] = page.content
            self.nav.addItem(name)
            self.stack.addWidget(page)
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)
        layout.addWidget(self.nav, 1)
        layout.addWidget(self.stack, 6)
        self.setCentralWidget(shell)
        self.build_projects()
        self.build_devices()
        self.build_execution()
        self.build_results()
        self.build_evidence()
        self.build_settings()
        self.name.textEdited.connect(lambda: setattr(self, 'dirty', True))
        self.install_language_selector()
        self.refresh()
        self.retranslate()

    def status_text(self,code):
        if i18n.language=='en':return code
        return {'PASS':'通过','FAIL':'不通过','REVIEW':'待复核','N/A':'不适用','PASS WITH COMMENTS':'带意见通过','ERROR':'异常','COMPLETED':'已完成'}.get(code,code)

    def install_language_selector(self):
        from PySide6.QtWidgets import QToolBar
        toolbar=QToolBar(self); toolbar.setMovable(False); self.addToolBar(toolbar)
        toolbar.addWidget(QLabel('语言 / Language: '))
        self.language_selector=QComboBox(); self.language_selector.addItem('简体中文','zh'); self.language_selector.addItem('English','en')
        self.language_selector.setCurrentIndex(1 if i18n.language=='en' else 0)
        toolbar.addWidget(self.language_selector)
        self.language_selector.currentIndexChanged.connect(self.change_language)
        self.qt_translator=None

    def change_language(self):
        i18n.set_language(self.language_selector.currentData())
        self.retranslate()
        # Only result presentation changes. Queue checks, edits, selection and credentials stay intact.
        self.refresh_results()

    def retranslate(self):
        from PySide6.QtWidgets import QAbstractButton
        app=QApplication.instance()
        if self.qt_translator is not None:app.removeTranslator(self.qt_translator)
        self.qt_translator=QTranslator(self)
        if i18n.language=='zh' and self.qt_translator.load('qtbase_zh_CN',QLibraryInfo.path(QLibraryInfo.TranslationsPath)):
            app.installTranslator(self.qt_translator)
        inverse={v:k for k,v in i18n.CATALOG.items()}
        inverse.update({v:k for k,v in i18n.ZH.items()})
        def source(text):return inverse.get(text,text)
        for widget in self.findChildren(QWidget):
            if isinstance(widget,(QLabel,QAbstractButton)):
                text=widget.property('translationSource')
                if text is None:
                    text=source(widget.text())
                    if text not in i18n.CATALOG and text not in i18n.ZH:continue
                    widget.setProperty('translationSource',text)
                widget.setText(tr(text))
        for i,module in enumerate((projects,devices,execution,results,evidence,settings)):
            self.nav.item(i).setText(tr(module.Page.title))
        for table in (self.device_table,self.task_table,self.result_table):
            for col in range(table.columnCount()):
                item=table.horizontalHeaderItem(col)
                text=item.data(Qt.UserRole) or source(item.text()); item.setData(Qt.UserRole,text); item.setText(tr(text))
        # Library IDs stay stable as data, while their labels follow the UI language.
        labels={'system.version':('系统版本','System version'),'interfaces.brief':('接口摘要','Interface summary')}
        for i in range(self.library_id.count()):
            key=self.library_id.itemData(i); pair=labels.get(key,(key,key));self.library_id.setItemText(i,pair[0 if i18n.language=='zh' else 1])
        self.setWindowTitle('网络 T&C 自动化工具' if i18n.language=='zh' else 'Network T&C Automation')

    def button(self, layout, title, callback, lock=True):
        button = QPushButton(title)
        button.clicked.connect(lambda: self.guard(callback))
        layout.addWidget(button)
        if lock:
            self.locked.append(button)
        return button

    def guard(self, callback):
        try:
            callback()
        except Exception as exc:
            QMessageBox.warning(self, tr('操作失败'), message(str(exc)))

    def text(self, layout, label, value=''):
        layout.addWidget(QLabel(label))
        widget = QLineEdit(value)
        layout.addWidget(widget)
        return widget

    def combo(self, layout, label, items):
        layout.addWidget(QLabel(label))
        widget = QComboBox()
        widget.addItems(items)
        layout.addWidget(widget)
        return widget

    def table(self, layout, headers):
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        return table

    def fill(self, table, rows):
        table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

    def confirm_discard(self):
        return not self.dirty or QMessageBox.question(self, tr('未保存修改'), tr('放弃当前未保存的修改？')) == QMessageBox.Yes

    def build_projects(self):
        box = self.pages['项目']
        self.project_label = QLabel(tr('未打开项目'))
        box.addWidget(self.project_label)
        self.name = self.text(box, tr('项目名称'), 'EVE-NG Lab')
        row = QHBoxLayout()
        box.addLayout(row)
        self.button(row, tr('新建项目'), self.new_project)
        self.button(row, tr('打开项目'), self.open_project)
        self.button(row, tr('保存项目'), self.save_project)
        box.addWidget(QLabel(tr('项目保存设备、任务和本机加密凭据；证据位于项目同级 evidence 目录。')))
        box.addStretch()

    def new_project(self):
        if not self.confirm_discard():
            return
        path, _ = QFileDialog.getSaveFileName(self, tr('新建项目'), str(BASE / 'projects' / 'lab' / 'project.json'), 'JSON (*.json)')
        if not path:
            return
        project.save(path, self.name.text(), [], [])
        self.path = Path(path)
        self.devices = []
        self.tasks = []
        self.dirty = False
        self.refresh()

    def open_project(self):
        if not self.confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(self, tr('打开项目'), str(BASE / 'projects'), 'JSON (*.json)')
        if not path:
            return
        name, devices, tasks = project.load(path)
        self.path = Path(path)
        self.name.setText(name)
        self.devices = devices
        self.tasks = tasks
        self.dirty = False
        self.refresh()

    def save_project(self):
        path = self.path
        if path is None:
            value, _ = QFileDialog.getSaveFileName(self, tr('保存项目'), str(BASE / 'projects' / 'lab' / 'project.json'), 'JSON (*.json)')
            if not value:
                return False
            path = Path(value)
        project.save(path, self.name.text(), self.devices, self.tasks)
        self.path = path
        self.dirty = False
        self.refresh()
        return True

    def evidence_root(self):
        return self.path.parent / 'evidence' if self.path else BASE / 'runtime' / 'evidence'

    def build_devices(self):
        box = self.pages['设备']
        self.device_table = self.table(box, [tr('Hostname'), tr('地址'), tr('平台'), tr('端口'), tr('用户名'), tr('分组')])
        from PySide6.QtWidgets import QGridLayout
        form=QGridLayout(); box.addLayout(form)
        fields=[]
        for index in range(7):
            cell=QWidget(); column=QVBoxLayout(cell); column.setContentsMargins(0,0,8,0); form.addWidget(cell,index//3,index%3);fields.append(column)
        self.did=self.text(fields[0],tr('Hostname'))
        self.host=self.text(fields[1],tr('管理 IP（必填）'))
        self.platform=self.combo(fields[2],tr('平台'),list(PROFILES))
        fields[3].addWidget(QLabel(tr('端口')));self.port=QSpinBox();self.port.setRange(1,65535);self.port.setValue(22);fields[3].addWidget(self.port)
        self.duser=self.text(fields[4],tr('SSH 用户名'));self.password=self.text(fields[5],tr('SSH 密码'));self.password.setEchoMode(QLineEdit.Password);self.group=self.text(fields[6],tr('分组'))
        self.button(box,tr('从 Excel 导入设备和凭据'),self.import_excel)
        row = QHBoxLayout()
        box.addLayout(row)
        self.button(row, tr('新增设备'), self.add_device)
        self.button(row, tr('载入选中设备'), self.select_device)
        self.button(row, tr('更新选中设备'), self.update_device)
        self.button(row, tr('删除选中设备'), self.delete_device)
        self.button(box, tr('SSH 连通测试（使用设备凭据）'), self.connection_test)
        notice=QLabel(tr('Hostname被任务引用后不允许修改；需要先删除关联任务。SSH 测试结果也会保存证据。'));notice.setWordWrap(True);box.addWidget(notice)

    def form_device(self):
        d = Device(self.did.text().strip(), self.host.text().strip(), self.platform.currentText(), self.port.value(), self.duser.text().strip(), self.group.text().strip(), self.password.text())
        project.validate([d], [])
        return d

    def add_device(self):
        d = self.form_device()
        project.validate(self.devices + [d], self.tasks)
        self.devices.append(d)
        self.dirty = True
        self.refresh()

    def select_device(self):
        i = self.device_table.currentRow()
        if i < 0:
            return
        d = self.devices[i]
        self.did.setText(d.id)
        self.host.setText(d.host)
        self.platform.setCurrentText(d.platform)
        self.port.setValue(d.port)
        self.duser.setText(d.username)
        self.password.setText(d.password)
        self.group.setText(d.group)

    def update_device(self):
        i = self.device_table.currentRow()
        if i < 0:
            raise ValueError(tr('请先选中设备'))
        devices = list(self.devices)
        devices[i] = self.form_device()
        project.validate(devices, self.tasks)
        self.devices = devices
        self.dirty = True
        self.refresh()

    def delete_device(self):
        selected = sorted({x.row() for x in self.device_table.selectedIndexes()}, reverse=True)
        devices = [d for i, d in enumerate(self.devices) if i not in selected]
        project.validate(devices, self.tasks)
        self.devices = devices
        self.dirty = True
        self.refresh()

    def build_execution(self):
        box = self.pages['执行']
        row = QHBoxLayout()
        box.addLayout(row)
        self.button(row, tr('导入 Excel 设备和计划（合并）'), self.import_excel)
        self.button(row, tr('下载 Excel 模板'), self.export_template)
        row = QHBoxLayout()
        box.addLayout(row)
        self.target = self.combo(row, tr('目标设备'), [])
        self.library_id = self.combo(row, tr('内置测试'), list(PROFILES['cisco_ios']))
        for i in range(self.library_id.count()): self.library_id.setItemData(i,self.library_id.itemText(i))
        self.button(row, tr('从测试库加入队列'), self.add_library)
        row = QHBoxLayout()
        box.addLayout(row)
        self.command = self.text(row, tr('Quick Command（单行）'))
        self.expected = self.text(row, tr('预期包含文本（可选，区分大小写）'))
        self.button(row, tr('临时命令加入队列'), self.add_quick)
        self.task_table = self.table(box, [tr('执行'), tr('Test ID'), tr('Hostname'), tr('章节'), tr('测试名称'), tr('步骤数'), tr('命令 / 首步骤'), tr('预期包含')])
        self.task_table.setColumnWidth(0, 45)
        self.task_table.setColumnWidth(4, 180)
        self.button(box, tr('批量套用 T&C 模板（选择设备和检查项）'), self.batch_templates)
        self.button(box,tr('冗余测试工作流（可自定义）'),self.open_workflow)
        row = QHBoxLayout()
        box.addLayout(row)
        self.button(row, tr('编辑选中任务'), self.edit_task)
        self.button(row, tr('删除选中任务'), self.delete_tasks)
        self.button(row, tr('上移'), lambda: self.move_task(-1))
        self.button(row, tr('下移'), lambda: self.move_task(1))
        self.button(row, tr('清空队列'), self.clear_tasks)
        row = QHBoxLayout()
        box.addLayout(row)
        row.addWidget(QLabel(tr('运行方式：SSH 真实设备连接')))
        self.button(row, tr('执行勾选测试项'), self.run_checked)
        self.button(row, tr('全选'), lambda: self.check_all(True))
        self.button(row, tr('全不选'), lambda: self.check_all(False))
        self.cancel = self.button(row, tr('停止后续任务'), self.cancel_run, False)
        self.cancel.setEnabled(False)
        self.progress = QProgressBar()
        box.addWidget(self.progress)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        box.addWidget(self.log)

    def open_workflow(self):
        from gui.workflow import WorkflowDialog
        if self.worker is not None:return
        if not self.devices:raise ValueError(tr('请先添加设备'))
        if self.path is None or self.dirty:
            if not self.save_project():return
        dialog=WorkflowDialog(self.devices,self.evidence_root(),self.timeout.value(),self)
        dialog.exec();self.refresh_results()

    def target_device(self):
        return next((d for d in self.devices if d.id == self.target.currentText()))

    def add_library(self):
        self.tasks.append(library(self.target_device(), self.library_id.currentData() or self.library_id.currentText()))
        self.dirty = True
        self.refresh()

    def add_quick(self):
        self.tasks.append(replace(quick(self.target_device(), self.command.text()), expected=self.expected.text()))
        self.dirty = True
        self.refresh()

    def import_excel(self):
        path, _ = QFileDialog.getOpenFileName(self, tr('导入 Excel'), '', 'Excel (*.xlsx)')
        if not path:
            return
        devices, tasks = excel.load(path)
        existing = {d.id: d for d in self.devices}
        existing.update(devices)
        merged = deduplicate(self.tasks + tasks)
        project.validate(list(existing.values()), merged)
        self.devices = list(existing.values())
        self.tasks = merged
        self.dirty = True
        self.refresh()

    def export_template(self):
        path, _ = QFileDialog.getSaveFileName(self, tr('保存模板'), 'test-plan.xlsx', 'Excel (*.xlsx)')
        if path:
            excel.template(path)

    def edit_task(self):
        i = self.task_table.currentRow()
        if i < 0:
            return
        t = self.tasks[i]
        values = {}
        for key, label, value, multi in [('id', tr('Test ID'), t.id, False), ('section', tr('章节'), t.section, False), ('name', tr('测试名称'), t.name, False), ('logical_group', tr('逻辑设备组 / Stack'), t.logical_group, False), ('criteria', tr('验收标准 / 项目预期（用于人工复核）'), t.criteria, True), ('expected', tr('自动判断：包含文本（可留空）'), t.expected, False), ('steps', tr('查询命令步骤（一行一条）'), '\n'.join(t.steps or [t.command]), True)]:
            fn = QInputDialog.getMultiLineText if multi else QInputDialog.getText
            value, ok = fn(self, tr('编辑测试项'), label, text=value)
            if not ok:
                return
            values[key] = value
        steps = [c.strip() for c in values.pop('steps').splitlines() if c.strip()]
        if not steps:
            raise ValueError(tr('至少填写一个查询步骤'))
        values['id'] = values['id'].strip()
        tasks = list(self.tasks)
        tasks[i] = replace(t, **values, command=steps[0], steps=steps)
        project.validate(self.devices, tasks)
        self.tasks = tasks
        self.dirty = True
        self.refresh()

    def check_all(self, checked):
        for row in range(self.task_table.rowCount()):
            self.task_table.item(row, 0).setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def run_checked(self):
        tasks = [t for i, t in enumerate(self.tasks) if self.task_table.item(i, 0).checkState() == Qt.Checked]
        self.start(tasks)

    def batch_templates(self):
        from PySide6.QtWidgets import QDialog, QDialogButtonBox
        if not self.devices:
            raise ValueError(tr('请先添加设备'))
        dialog = QDialog(self)
        dialog.setWindowTitle(tr('批量套用 T&C 模板'))
        dialog.resize(700, 520)
        box = QVBoxLayout(dialog)
        box.addWidget(QLabel(tr('勾选设备（可多选）')))
        devices = QListWidget()
        box.addWidget(devices)
        for d in self.devices:
            from PySide6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(d.id + ' | ' + d.host, devices)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
        box.addWidget(QLabel(tr('勾选测试项；命令需按实际型号核对，默认结论待复核')))
        cases = QListWidget()
        box.addWidget(cases)
        for key in TEMPLATES:
            item = QListWidgetItem(tr(key), cases)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        box.addWidget(buttons)
        if dialog.exec() != QDialog.Accepted:
            return
        selected = [d for i, d in enumerate(self.devices) if devices.item(i).checkState() == Qt.Checked]
        keys = [k for i, k in enumerate(TEMPLATES) if cases.item(i).checkState() == Qt.Checked]
        if not selected or not keys:
            raise ValueError(tr('至少选择一台设备和一个测试项'))
        created=apply_templates(selected,keys)
        if i18n.language=='en': created=[replace(t,name=tr(t.name),criteria=tr(t.criteria)) for t in created]
        self.tasks = deduplicate(self.tasks + created)
        self.dirty = True
        self.refresh()

    def delete_tasks(self):
        selected = {i.row() for i in self.task_table.selectedIndexes()}
        self.tasks = [t for i, t in enumerate(self.tasks) if i not in selected]
        self.dirty = True
        self.refresh()

    def clear_tasks(self):
        if QMessageBox.question(self, tr('清空'), tr('删除队列中所有任务？')) == QMessageBox.Yes:
            self.tasks = []
            self.dirty = True
            self.refresh()

    def move_task(self, offset):
        i = self.task_table.currentRow()
        j = i + offset
        if i >= 0 and 0 <= j < len(self.tasks):
            self.tasks[i], self.tasks[j] = (self.tasks[j], self.tasks[i])
            self.dirty = True
            self.refresh()
            self.task_table.selectRow(j)

    def connection_test(self):
        i = self.device_table.currentRow()
        if i < 0:
            raise ValueError(tr('请选中一台设备'))
        self.start([library(self.devices[i], 'system.version')])

    def start(self, tasks):
        if self.worker is not None:
            return
        if not tasks:
            raise ValueError(tr('任务队列为空'))
        project.validate(self.devices, tasks)
        if self.path is None or self.dirty:
            if not self.save_project():
                return
        targets={t.device_id for t in tasks}
        if any(not d.username or not d.password for d in self.devices if d.id in targets):raise ValueError(tr('请在设备页填写每台设备的 SSH 用户名和密码'))
        commands = '\n'.join((f'{t.device_id} / {t.section} / {t.name or t.id}: ' + ' ; '.join(t.steps or [t.command]) for t in tasks))
        if QMessageBox.question(self, tr('确认 SSH 执行'), (f'将连接设备执行 {len(tasks)} 个测试项。请确认命令均为查询命令。\n\n' if i18n.language=='zh' else f'Connect to devices and run {len(tasks)} tests. Confirm that all commands are read-only.\n\n')+commands[:2500]) != QMessageBox.Yes:
            return
        adapter = SSHAdapter('', '', self.timeout.value())
        self.progress.setRange(0, len(tasks))
        self.progress.setValue(0)
        self.log.clear()
        self.worker = Worker(adapter, list(tasks), {d.id: d for d in self.devices}, self.evidence_root())
        self.worker.item.connect(self.got_result)
        self.worker.failed.connect(lambda text: self.log.append(tr('运行中止: ') + message(text)))
        self.worker.finished.connect(self.run_finished)
        for widget in self.locked:
            widget.setEnabled(False)
        self.cancel.setEnabled(True)
        self.worker.start()

    def got_result(self, result):
        self.progress.setValue(self.progress.value() + 1)
        self.log.append(f'{result.task.device_id} / {result.task.id}: {self.status_text(result.status)} {message(result.error)}')

    def cancel_run(self):
        if self.worker:
            self.worker.stop.set()
            self.log.append(tr('已请求停止；等待当前 SSH 调用结束或超时。'))

    def run_finished(self):
        worker = self.worker
        self.worker = None
        if worker:
            worker.deleteLater()
        for widget in self.locked:
            widget.setEnabled(True)
        self.cancel.setEnabled(False)
        self.password.clear()
        self.log.append(tr('运行结束。设备凭据保留于当前项目，输入框已清除。'))
        self.refresh_results()

    def build_results(self):
        box = self.pages['结果']
        self.result_table = self.table(box, [tr('时间 UTC'), tr('设备名称'), tr('IP 地址'), tr('章节'), tr('Test ID'), tr('测试名称'), tr('执行状态'), tr('自动判断'), tr('人工复核')])
        self.result_table.itemSelectionChanged.connect(self.show_result)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        box.addWidget(self.output)
        row = QHBoxLayout()
        box.addLayout(row)
        self.button(row, tr('刷新历史'), self.refresh_results)
        self.button(row, tr('人工复核'), self.manual_review)
        self.button(row, tr('打开所选证据目录'), self.open_selected)
        self.button(row, tr('复测选中记录'), self.retest_selected)

    def refresh_results(self):
        self.rows = history(self.evidence_root())
        data = []
        for r in self.rows:
            try:
                manual = json.loads((Path(r['evidence_dir']) / 'review.json').read_text(encoding='utf-8')).get('status', '')
            except (OSError, ValueError):
                manual = ''
            data.append([r['started_at'], r.get('device_name', r['task']['device_id']), r.get('device_ip', ''), r['task'].get('section', ''), r['task']['id'], r['task'].get('name', ''), self.status_text(r.get('execution_status') or ('ERROR' if r['status'] == 'ERROR' else 'COMPLETED')), self.status_text(r['status']), self.status_text(manual)])
        self.fill(self.result_table, data)
        self.evidence_label.setText(str(self.evidence_root()))

    def selected_result(self):
        i = self.result_table.currentRow()
        if i < 0 or i >= len(self.rows):
            raise ValueError(tr('请在结果页选中一条记录'))
        return self.rows[i]

    def show_result(self):
        i = self.result_table.currentRow()
        if 0 <= i < len(self.rows):
            r = self.rows[i]
            t = r['task']
            self.output.setPlainText(tr('章节')+': '+t.get('section','')+'\n'+tr('测试名称')+': '+t.get('name','')+'\n'+tr('逻辑设备组 / Stack')+': '+t.get('logical_group','')+'\n'+tr('验收标准 / 项目预期（用于人工复核）')+': '+t.get('criteria','')+'\n\n'+r['output']+'\n'+r['error'])

    def manual_review(self):
        r = self.selected_result()
        codes=['PASS','FAIL','REVIEW','N/A','PASS WITH COMMENTS']
        labels=[self.status_text(c) for c in codes]
        status, ok = QInputDialog.getItem(self, tr('人工复核'), tr('状态'), labels, 0, False)
        if ok: status=codes[labels.index(status)]
        if not ok:
            return
        actual, ok = QInputDialog.getMultiLineText(self, tr('人工复核'), tr('实际结果'))
        if not ok:
            return
        note, ok = QInputDialog.getMultiLineText(self, tr('人工复核'), tr('备注（N/A 与带意见通过需说明原因）'))
        if ok:
            if status in ('N/A', 'PASS WITH COMMENTS') and (not note.strip()):
                raise ValueError(tr('请填写原因'))
            review(r['evidence_dir'], status, note, actual)
            self.refresh_results()

    def retest_selected(self):
        indices = sorted({i.row() for i in self.result_table.selectedIndexes()})
        if not indices:
            raise ValueError(tr('请在结果页选中需要复测的记录，可多选'))
        tasks = [replace(Task(**self.rows[i]['task']), retest_of=self.rows[i]['evidence_dir']) for i in indices]
        self.start(tasks)

    def export_results(self):
        path, _ = QFileDialog.getSaveFileName(self, tr('导出结果与证据索引'), 'tc-results.csv', 'CSV (*.csv)')
        if path:
            export_index(self.evidence_root(), path)

    def open_selected(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.selected_result()['evidence_dir']))

    def build_evidence(self):
        box = self.pages['证据']
        self.evidence_label = QLabel()
        self.evidence_label.setWordWrap(True)
        box.addWidget(self.evidence_label)
        self.button(box, tr('打开当前项目证据目录'), lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.evidence_root()))))
        self.button(box, tr('导出当前项目全部证据 ZIP'), self.export_zip)
        self.button(box, tr('导出结果与证据索引 CSV'), self.export_results)
        box.addWidget(QLabel(tr('按日期时间归档；文件以设备名称-IP-命令命名，附带 Test ID 与重复序号。\n人工复核保存为 review.json，不修改原始状态和证据。PNG 是 CLI 文本渲染图。')))
        box.addStretch()

    def export_zip(self):
        if not self.evidence_root().exists():
            raise ValueError(tr('尚无证据'))
        path, _ = QFileDialog.getSaveFileName(self, tr('导出 ZIP'), 'evidence.zip', 'ZIP (*.zip)')
        if path:
            from zipfile import ZipFile, ZIP_DEFLATED
            target = Path(path).resolve()
            root = self.evidence_root().resolve()
            if target == root or root in target.parents:
                raise ValueError(tr('ZIP 请保存到证据目录以外'))
            with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
                for record in history(root):
                    for item in Path(record['evidence_dir']).iterdir():
                        if item.is_file():
                            archive.write(item, item.relative_to(root))
                workflow_root=root.parent/'workflow-runs'
                if workflow_root.exists():
                    for item in workflow_root.glob('*/workflow.json'):
                        archive.write(item,Path('workflow-runs')/item.relative_to(workflow_root))

    def build_settings(self):
        box = self.pages['设置']
        box.addWidget(QLabel(tr('超时（秒）；连接、认证、命令各阶段使用此值')))
        self.timeout = QSpinBox()
        self.timeout.setRange(5, 300)
        self.timeout.setValue(30)
        box.addWidget(self.timeout)
        box.addWidget(QLabel(tr('SSH 严格校验主机密钥。首次连接请用 Windows OpenSSH 登录并核对指纹，\n将主机写入用户 ~/.ssh/known_hosts。无需关闭主机密钥验证。\n当前为顺序执行、账号密码认证；不包含 enable 提权和自动配置变更。')))
        box.addStretch()

    def refresh(self):
        self.project_label.setText(str(self.path or tr('未保存项目')) + (' *' if self.dirty else ''))
        self.fill(self.device_table, [[d.id, d.host, d.platform, d.port, d.username, d.group] for d in self.devices])
        self.fill(self.task_table, [['', t.id, t.device_id, t.section, t.name or t.command, len(t.steps or [t.command]), t.command, t.expected] for t in self.tasks])
        for i in range(len(self.tasks)):
            item = self.task_table.item(i, 0)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
        selected = self.target.currentText()
        self.target.clear()
        self.target.addItems([d.id for d in self.devices])
        self.target.setCurrentText(selected)
        self.refresh_results()

    def closeEvent(self, event):
        if self.worker is not None:
            QMessageBox.information(self, tr('执行中'), tr('请先停止后续任务，等待当前调用结束后再关闭。'))
            event.ignore()
            return
        if not self.confirm_discard():
            event.ignore()
            return
        self.password.clear()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
if __name__ == '__main__':
    main()
