from datetime import datetime, date

from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtWidgets import QWidget, QCheckBox, QFormLayout, QLineEdit, QDateEdit, QLabel, QScrollArea, QHBoxLayout, \
    QVBoxLayout

from data_types import UpdateClientPaymentData, UpdateEmployeePaymentData
from frontend.DataFetching.get_data import get_client_employees
from frontend.components.Root.UpdateHandler import updateHandler


class FormUpdatePayment(QWidget):
	def __init__(self, data, handle_back_button, is_client):
		super().__init__()
		self.data = data
		self.is_client = is_client
		self.client_name = self.data[1]
		self.is_cash = QCheckBox('Cash')
		self.employees = get_client_employees(self.client_name)
		self.split_fields = {}
		self.split_field = self.employee_split()
		self.employee_payments = {}

		self.layout = QFormLayout()
		self.setLayout(self.layout)
		self.observations = QLineEdit(self)
		self.amount_field = QLineEdit(self)
		self.amount_field.setValidator(QDoubleValidator())
		self.date_field = QDateEdit(self)
		self.date_field.setCalendarPopup(True)
		self.date_field.setDate(datetime.strptime(self.data[3], '%Y-%m-%d').date() if is_client else datetime.strptime(self.data[4], '%Y-%m-%d').date())
		print(datetime.strptime(self.data[3], '%Y-%m-%d').date() if is_client else datetime.strptime(self.data[4], '%Y-%m-%d').date(), date.today())

		self.layout.addRow('Client: ', QLabel(str(data[1])))
		self.layout.addRow('Suma: ', self.amount_field)
		self.layout.addRow('Data: ', self.date_field)
		self.layout.addRow('Cash: ', self.is_cash)
		self.layout.addRow('Observatii: ', self.observations)
		if self.is_client:
			self.layout.addRow('Impartire: ', self.split_field)

		updateHandler.add_object(self)

	def get_data(self):
		if self.amount_field.text() == '':
			return "Introdu suma"
		individual_sums, total_sum = self.get_employee_payments()
		if self.is_client and total_sum != float(self.amount_field.text()):
			return "Sumele individuale nu insumeaza suma totala"
		if self.is_client:
			return UpdateClientPaymentData(
					id=self.data[0],
					name=self.client_name,
					amount=self.amount_field.text(),
					individual_amounts= individual_sums,
					date=self.date_field.date().toPyDate(),
					cash=self.is_cash.isChecked(),
					observations=self.observations.text()
				)
		return UpdateEmployeePaymentData(
			id=self.data[0],
			amount=self.amount_field.text(),
			date=self.date_field.date().toPyDate(),
			cash=self.is_cash.isChecked(),
			observations=self.observations.text()
		)

	def employee_split(self):
		scroll = QScrollArea()
		connections = QWidget()
		layout = QVBoxLayout()
		for employee in self.employees:
			employee_field = QWidget()
			employee_layout = QHBoxLayout()
			employee_layout.addWidget(QLabel(employee))
			specific_employee_sum = QLineEdit()
			specific_employee_sum.setValidator(QDoubleValidator())
			self.split_fields[employee] = specific_employee_sum
			employee_layout.addWidget(specific_employee_sum)
			employee_field.setLayout(employee_layout)
			layout.addWidget(employee_field)
		connections.setLayout(layout)
		scroll.setWidget(connections)
		return scroll

	def get_employee_payments(self):
		employee_sums = {}
		total_sum = 0
		for field in self.split_fields.keys():
			employee_sums[field] = self.split_fields[field].text()
			if self.split_fields[field].text():
				total_sum += float(self.split_fields[field].text())
		return (employee_sums, total_sum)

	def update(self):
		if self.is_client:
			self.employees = get_client_employees(self.client_name)
			self.split_field.setParent(None)
			self.layout.removeRow(5)
			self.split_field = self.employee_split()
			self.layout.addRow('Impartire: ', self.split_field)

