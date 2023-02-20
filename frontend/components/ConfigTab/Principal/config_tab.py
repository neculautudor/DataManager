from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget, QGridLayout, \
	QMessageBox

from backend.DBConnection import db
from frontend.components.CommonComponents.common_components import button, SelectDelete, PopupWindow
from frontend.components.ConfigTab.Principal.config_tab_components import FormEmployee, FormClient
from frontend.Translations.translations import translations_dict
from frontend.components.Root.UpdateHandler import updateHandler


class ConfigTab(QWidget):
	"""Create the General page UI."""
	def __init__(self, ):
		super().__init__()
		self.layout = QVBoxLayout()
		self.tabs = QTabWidget()
		self.tabs.addTab(AdaugaAngajat(), 'Angajat')
		self.tabs.addTab(AdaugaClient(), 'Client')
		self.tabs.addTab(Sterge(), 'Sterge')
	# tabs.setTabPosition(QTabWidget.TabPosition.West)
		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)

class AdaugaAngajat(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.form = FormEmployee()
		self.layout.addWidget(self.form)
		self.selectable_button = button('submit', lambda: self.handle_submit()) # TODO action
		self.layout.addWidget(self.selectable_button)
		self.setLayout(self.layout)

	def handle_submit(self):
		if type(self.form.get_data()) == str:
			PopupWindow('Eroare', self.form.get_data(), None, False)
		else:
			data = self.form.get_data()
			print(f'(DONE)ACTIUNE: Submit( Add employee ) {str(self.form.get_data())}')
			db.add_employee(' '.join([data.name, data.surname]), data.clients, data.date)
			updateHandler.update_all()
			self.form.reset()

class AdaugaClient(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.form = FormClient()
		self.layout.addWidget(self.form)
		self.selectable_button = button('submit', lambda: self.handle_submit())  # TODO action
		self.layout.addWidget(self.selectable_button)
		self.setLayout(self.layout)

	def handle_submit(self):
		if type(self.form.get_data()) == str:
			PopupWindow('Eroare', self.form.get_data(), None, False)
		else:
			data = self.form.get_data()
			print(f'(DONE)ACTIUNE: Submit( Add client ) {str(self.form.get_data())}')
			db.add_client(data.name, data.employees, data.date)
			updateHandler.update_all()
			self.form.reset()

class Sterge(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QGridLayout()
		self.employee_box = SelectDelete([angajat[0] for angajat in db.get_employees()])
		self.client_box = SelectDelete([client[0] for client in db.get_clients()])
		self.delete_employee = QPushButton('Sterge angajat')
		self.delete_client = QPushButton('Sterge client')
		self.delete_employee.clicked.connect(lambda: self.delete('employee'))
		self.delete_client.clicked.connect(lambda: self.delete('client'))

		self.popup_delete = QMessageBox()
		self.popup_delete.setWindowTitle('Confirm')
		# popup_delete_employee.setText(f'Stergi angajatul {employee_box.currentText()}?')
		# popup_delete_client.setText(f'Stergi clientul {client_box.currentText()}?')


		self.layout.addWidget(self.employee_box, 0, 0)
		self.layout.addWidget(self.delete_employee, 0, 1)
		self.layout.addWidget(self.client_box, 1, 0)
		self.layout.addWidget(self.delete_client, 1, 1)
		self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.layout.setSpacing(50)
		self.setLayout(self.layout)

		updateHandler.add_object(self)

	def delete(self, type_):
		def client_action():
			print(f'(DONE)ACTIUNE: Success delete {self.client_box.currentText()}')
			db.delete_client(self.client_box.currentText())
			updateHandler.update_all()

		def employee_action():
			print(f'(DONE)ACTIUNE: Success delete {self.employee_box.currentText()}')
			db.delete_employee(self.employee_box.currentText())
			updateHandler.update_all()

		PopupWindow(
			title=f'Sterge {translations_dict[type_]}',
			description=f'Sterge {translations_dict[type_]} {self.client_box.currentText()}' if type_ == 'client' else
			f'Sterge {translations_dict[type_]} {self.employee_box.currentText()}',
			action=(lambda: (
				client_action() if type_ == 'client' else employee_action()
				  # TODO action
			)),
			with_cancel=True)


	def update(self):
		self.employee_box.reset([angajat[0] for angajat in db.get_employees()])
		self.client_box.reset([client[0] for client in db.get_clients()])



