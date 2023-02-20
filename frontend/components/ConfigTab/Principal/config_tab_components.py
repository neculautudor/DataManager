from datetime import date

from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QDateEdit, QScrollArea, QVBoxLayout, QCheckBox

from backend.DBConnection import db
from data_types import AddEmployeeData, AddClientData
from frontend.components.Root.UpdateHandler import updateHandler


class FormEmployee(QWidget):
	def __init__(self):
		super().__init__()

		self.selected_clients = []
		self.clients = set()
		self.clients.update([client[0] for client in db.get_clients()])
		self.checkboxes = []

		self.layout = QFormLayout()
		self.setLayout(self.layout)
		self.name_field = QLineEdit(self)
		self.surname_field = QLineEdit(self)
		self.date_field = QDateEdit(self)
		self.date_field.setCalendarPopup(True)
		self.date_field.setDate(date.today())
		# self.clients_field = SelectConnections(self.clients, lambda: self.on_client_select())
		self.layout.addRow('Nume: ', self.name_field)
		self.layout.addRow('Prenume: ', self.surname_field)
		self.layout.addRow('Data: ', self.date_field)
		# self.layout.addWidget(self.clients_field)
		self.layout.addRow('Conexiuni: ', self.clients_checkboxes())

		updateHandler.add_object(self)

	def get_data(self):
		if self.name_field.text() == '' or self.surname_field.text() == '':
			return "Nume sau prenume necompletat"
		checked_checkboxes = []
		for checkbox in self.checkboxes:
			if checkbox.isChecked():
				checked_checkboxes.append(checkbox.text())
		# if not checked_checkboxes:
		# 	return "Selectati macar un client"

		employee = AddEmployeeData(
			name=self.name_field.text(),
			surname=self.surname_field.text(),
			date=self.date_field.date().toPyDate(),
			clients=checked_checkboxes
		)
		return employee

	def clients_checkboxes(self):
		self.checkboxes =[]
		scroll = QScrollArea()
		connections = QWidget()
		layout = QVBoxLayout()
		for index, client in enumerate(self.clients):
			checkbox = QCheckBox(client)
			self.checkboxes.append(checkbox)
			layout.addWidget(checkbox)
		connections.setLayout(layout)
		scroll.setWidget(connections)
		return scroll

	def reset(self):
		self.name_field.clear()
		self.surname_field.clear()
		self.date_field.setDate(date.today())
		for checkbox in self.checkboxes:
			if checkbox.isChecked():
				checkbox.click()

	def update(self):
		self.clients = set()
		self.clients.update([client[0] for client in db.get_clients()])
		self.layout.removeRow(3)
		self.layout.addRow('Conexiuni: ', self.clients_checkboxes())

class FormClient(QWidget):
	def __init__(self):
		super().__init__()

		self.selected_clients = []
		self.clients = set()
		self.clients.update([client[0] for client in db.get_employees()])
		self.checkboxes = []

		self.layout = QFormLayout()
		self.setLayout(self.layout)
		self.name_field = QLineEdit(self)
		self.date_field = QDateEdit(self)
		self.date_field.setCalendarPopup(True)
		self.date_field.setDate(date.today())
		self.layout.addRow('Nume: ', self.name_field)
		self.layout.addRow('Data: ', self.date_field)
		self.layout.addRow('Conexiuni: ', self.clients_checkboxes())

		updateHandler.add_object(self)

	def get_data(self):
		if self.name_field.text() == '':
			return "Nume necompletat"
		checked_checkboxes = []
		for checkbox in self.checkboxes:
			if checkbox.isChecked():
				checked_checkboxes.append(checkbox.text())
		# if not checked_checkboxes:
		# 	return "Selectati macar un angajat"
		employee = AddClientData(
			name=self.name_field.text(),
			date=self.date_field.date().toPyDate(),
			employees=checked_checkboxes
		)
		return employee

	def reset(self):
		self.name_field.clear()
		self.date_field.setDate(date.today())
		for checkbox in self.checkboxes:
			if checkbox.isChecked():
				checkbox.click()

	def clients_checkboxes(self):
		self.checkboxes =[]
		scroll = QScrollArea()
		connections = QWidget()
		layout = QVBoxLayout()
		for index, client in enumerate(self.clients):
			checkbox = QCheckBox(client)
			self.checkboxes.append(checkbox)
			layout.addWidget(checkbox)
		connections.setLayout(layout)
		scroll.setWidget(connections)
		return scroll

	def update(self):
		self.clients = set()
		self.clients.update([client[0] for client in db.get_employees()])
		self.layout.removeRow(2)
		self.layout.addRow('Conexiuni: ', self.clients_checkboxes())
