from datetime import date

from PyQt6 import sip
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QFormLayout, QLineEdit, QDateEdit, QScrollArea, \
    QHBoxLayout, QLabel

from backend.DBConnection import db
from data_types import AddClientPaymentData
from frontend.DataFetching.get_data import get_clients, get_client_employees
from frontend.components.CommonComponents.common_components import SelectDelete, button, PopupWindow
from frontend.components.Root.UpdateHandler import updateHandler


class AdaugaPayment(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.form = FormPayment()
		self.layout.addWidget(self.form)
		self.selectable_button = button('submit', lambda: self.handle_submit()) # TODO action
		self.layout.addWidget(self.selectable_button)
		self.setLayout(self.layout)

	def handle_submit(self):
		data = self.form.get_data()
		if type(data) == str:
			PopupWindow('Eroare', data, None, False)
		else:
			print(f'(DONE)ACTIUNE: Submit (Add Payment) {str(data)}')
			print(data.individual_amounts)
			db.add_payment(data.client, data.amount, data.individual_amounts, data.date, data.cash, data.observations)
			updateHandler.update_all()
			self.form.reset()

	def get_form(self):
		return self.form


class FormPayment(QWidget):
	def __init__(self):
		super().__init__()
		self.client_box = SelectDelete([''] + get_clients())
		self.is_cash = QCheckBox('Cash')
		self.employees = get_client_employees(self.client_box.currentText())
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
		self.date_field.setDate(date.today())

		self.client_box.currentTextChanged.connect(lambda: self.on_client_change())

		self.layout.addRow('Suma: ', self.amount_field)
		self.layout.addRow('Client: ', self.client_box)
		self.layout.addRow('Data: ', self.date_field)
		self.layout.addRow('Cash: ', self.is_cash)
		self.layout.addRow('Observatii: ', self.observations)
		self.layout.addRow('Impartire: ', self.split_field)

		updateHandler.add_object(self)

	def get_data(self):
		if not self.client_box.currentText():
			return "Selectati un client"
		if self.amount_field.text() == '':
			return "Introdu suma"
		individual_sums, total_sum = self.get_employee_payments()
		print(total_sum)
		print(individual_sums)
		if total_sum != float(self.amount_field.text()):
			return "Sumele individuale nu insumeaza suma totala"
		client_payment = AddClientPaymentData(
			client=self.client_box.currentText(),
			amount=self.amount_field.text(),
			individual_amounts= individual_sums,
			date=self.date_field.date().toPyDate(),
			cash=self.is_cash.isChecked(),
			observations=self.observations.text()
		)
		return client_payment

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
			if self.amount_field.text() != '':
				specific_employee_sum.setText(str('%.2f' % (float(self.amount_field.text()) / len(self.employees))))
			self.split_fields[employee] = specific_employee_sum
			employee_layout.addWidget(specific_employee_sum)
			employee_field.setLayout(employee_layout)
			layout.addWidget(employee_field)
		connections.setLayout(layout)
		scroll.setWidget(connections)
		return scroll

	def on_client_change(self):
		self.employees = get_client_employees(self.client_box.currentText())
		self.layout.removeWidget(self.split_field)
		self.layout.removeRow(5)
		sip.delete(self.split_field)
		self.split_fields.clear()
		self.split_field = self.employee_split()
		self.layout.addRow('Impartire: ', self.split_field)
		self.layout.update()

	def get_employee_payments(self):
		employee_sums = {}
		total_sum = 0
		for field in self.split_fields.keys():
			if self.split_fields[field].text():
				employee_sums[field] = self.split_fields[field].text()
				total_sum += float(self.split_fields[field].text())
		return (employee_sums, total_sum)

	def reset(self):
		self.amount_field.clear()
		for field in self.split_fields.keys():
			self.split_fields[field].clear()
		self.date_field.setDate(date.today())
		if self.is_cash.isChecked():
			self.is_cash.click()
		self.observations.clear()

	def update(self):
		self.client_box.reset([''] + get_clients())

		self.employees = get_client_employees(self.client_box.currentText())
		self.split_field.setParent(None)
		self.layout.removeRow(5)
		self.split_field = self.employee_split()
		self.layout.addRow('Impartire: ', self.split_field)

