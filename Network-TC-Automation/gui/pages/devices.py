from PySide6.QtWidgets import QWidget, QVBoxLayout
class Page(QWidget):
    title = '设备'
    def __init__(self):
        super().__init__()
        self.content = QVBoxLayout(self)
