import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QApplication

from frontend.components.CommonComponents.common_components import button
from frontend.components.ConfigTab.Principal.config_tab import ConfigTab
from frontend.components.PaymentTab.Principal.payment_tab import PaymentTab

WIDTH = 800
HEIGHT = 600

app = QApplication(sys.argv)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('qt.png'))
        self.setWindowTitle('Data Manager')
        self.setGeometry(100, 100, WIDTH, HEIGHT)
        # self.setStyleSheet('background-color: grey')
        # self.setContentsMargins(0, 0, 20, 20)
        self.showMaximized()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.payment_tab = PaymentTab()
        self.config_tab = ConfigTab()
        tabs = QTabWidget()
        tabs.addTab(self.payment_tab, "Plata")
        tabs.addTab(self.config_tab, "Config")
        self.layout.addWidget(tabs)
        self.layout.addWidget(button("exit", app.quit))

