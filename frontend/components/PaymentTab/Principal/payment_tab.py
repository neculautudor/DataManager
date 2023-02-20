from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget, QGridLayout, \
	QMessageBox

from frontend.components.CommonComponents.common_components import SelectDelete
from frontend.components.PaymentTab.Tabs.AddTab import AdaugaPayment
from frontend.components.PaymentTab.Tabs.ModifyTabFolder.Principal.ModifyTab import ModifyPayment
from frontend.components.PaymentTab.Tabs.RaportsTab import Reports


class PaymentTab(QWidget):
	"""Create the General page UI."""
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.tabs = QTabWidget()
		self.add_payment = AdaugaPayment()
		self.modify_payment = ModifyPayment()
		self.reports = Reports()
		self.tabs.addTab(self.add_payment, 'Adauga')
		self.tabs.addTab(self.modify_payment, 'Detalii')
		self.tabs.addTab(self.reports, 'Rapoarte')
	# tabs.addTab(sterge(), 'Sterge')
	# tabs.setTabPosition(QTabWidget.TabPosition.West)
		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)

	def get_add_payment(self):
		return self.add_payment


# not used anywhere, might delete
def sterge():
	networkTab = QWidget()
	layout = QGridLayout()
	employee_box = SelectDelete(['angajat1', 'angajat2', 'angajat3'])
	client_box = SelectDelete(['client1', 'client2', 'client3'])
	delete_employee = QPushButton('Sterge angajat')
	delete_client = QPushButton('Sterge client')
	delete_employee.clicked.connect(lambda: print(f'ACTIUNE: sterge angajat {employee_box.currentText()}'))
	delete_client.clicked.connect(lambda: print(f'ACTIUNE: sterge client {client_box.currentText()}'))

	popup_delete = QMessageBox()
	popup_delete.setWindowTitle('Confirm')


	layout.addWidget(employee_box, 0, 0)
	layout.addWidget(delete_employee, 0, 1)
	layout.addWidget(client_box, 1, 0)
	layout.addWidget(delete_client, 1, 1)
	layout.setAlignment(Qt.AlignmentFlag.AlignTop)
	layout.setSpacing(50)
	networkTab.setLayout(layout)
	return networkTab


