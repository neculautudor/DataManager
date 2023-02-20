from datetime import date

import xlsxwriter
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QDateEdit, QPushButton, QVBoxLayout, QLabel

from backend.DBConnection import db
from data_types import FiltersData, UpdateEmployeePaymentData, UpdateClientPaymentData
from frontend.DataFetching.get_data import get_clients, get_employees
from frontend.components.CommonComponents.common_components import SelectDelete, PopupWindow, \
    button
from frontend.components.PaymentTab.Tabs.ModifyTabFolder.Components.PaymentsList import ScrollablePaymentButtons
from frontend.components.PaymentTab.Tabs.ModifyTabFolder.Components.UpdatePaymentForm import FormUpdatePayment
from frontend.components.Root.UpdateHandler import updateHandler

ALL_ENTITIES = '--TOTI--'


class ModifyPayment(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.filters = PaymentFilters()
		self.generate_button = QPushButton('Genereaza')
		self.generate_button.clicked.connect(lambda: self.generate_button_handle())
		self.export_pdf_button = QPushButton('Export Excel')
		self.export_pdf_button.clicked.connect(lambda: self.generate_pdf())
		self.update_payment_form = None
		self.payment_buttons = None
		self.current_payment_fields = None
		self.payments_field = None
		self.current_payment_data = None
		self.payments_data = None
		self.update_button = None
		self.back_button = None

		self.layout.addWidget(self.filters)
		self.layout.addWidget(self.generate_button)
		self.layout.addWidget(self.export_pdf_button)
		self.setLayout(self.layout)

		updateHandler.add_object(self)

	def generate_button_handle(self):
		print('generate')
		self.remove_current_payment_fields()
		payments_data = 'empty'
		filters_data = self.filters.get_filters()
		if filters_data.client_or_employee == 'Client':
			if filters_data.entity == ALL_ENTITIES:
				if filters_data.apply_period:
					payments_data = db.get_period_client_payments(filters_data.start_date, filters_data.end_date)
				else:
					payments_data = db.get_all_client_payments()
			else:
				if filters_data.apply_period:
					payments_data = db.get_period_specific_client_payments(filters_data.entity, filters_data.start_date, filters_data.end_date)
				else:
					payments_data = db.get_specific_client_payments(filters_data.entity)
		elif filters_data.client_or_employee == 'Angajat':
			if filters_data.entity == ALL_ENTITIES:
				if filters_data.apply_period:
					payments_data = db.get_period_employee_payments(filters_data.start_date, filters_data.end_date)
				else:
					payments_data = db.get_all_employee_payments()
			else:
				if filters_data.apply_period:
					payments_data = db.get_period_specific_employee_payments(filters_data.entity, filters_data.start_date, filters_data.end_date)
				else:
					payments_data = db.get_specific_employee_payments(filters_data.entity)
		self.payments_data = payments_data
		if self.payment_buttons:
			self.layout.removeWidget(self.payment_buttons)
			self.payment_buttons.deleteLater()
		self.payment_buttons = ScrollablePaymentButtons(payments_data, self.current_payment_data_setter, self.handle_edit_payment, self.handle_delete_payment)
		self.remove_current_payments_field()
		self.payments_field = CurrentPayments(self.payments_data)
		self.layout.addWidget(self.payment_buttons)
		self.layout.addWidget(self.payments_field)

	def current_payment_data_setter(self, current_payment_data):
		self.current_payment_data = current_payment_data
		self.set_current_payment_fields()

	def set_current_payment_fields(self):
		if self.current_payment_fields:
			self.current_payment_fields.setParent(None)
		self.current_payment_fields = CurrentPayment(self.current_payment_data)
		self.layout.addWidget(self.current_payment_fields)

	def remove_current_payment_fields(self):
		if self.current_payment_fields:
			self.current_payment_fields.setParent(None)
			# self.layout.removeWidget(self.current_payment_fields)
			# self.current_payment_fields.deleteLater()
			# self.current_payment_fields = None
			# self.current_payment_data = None

	def remove_current_payments_field(self):
		if self.payments_field:
			# self.layout.removeWidget(self.payments_field)
			self.payments_field.setParent(None)

	def handle_edit_payment(self, data, is_client):
		# self.current_payment_data_setter(None)
		self.filters.setParent(None)
		self.generate_button.setParent(None)
		if self.current_payment_fields:
			self.current_payment_fields.setParent(None)
		if self.payments_field:
			self.payments_field.setParent(None)
		if self.payment_buttons:
			self.payment_buttons.setParent(None)
		self.layout.update()

		self.back_button = button('Inapoi', lambda: self.handle_back_button())
		self.back_button.setIcon(QIcon("/frontend/icons/back.png"))
		self.layout.addWidget(self.back_button)

		self.update_payment_form = FormUpdatePayment(data, self.handle_back_button, is_client)
		self.layout.addWidget(self.update_payment_form)

		self.update_button = button('Actualizeaza', lambda: self.handle_update_payment())  # TODO action
		self.layout.addWidget(self.update_button)

	def handle_delete_payment(self, data):
		is_client = len(data) == 6

		def confirm_delete():
			print(f'(DONE)ACTIUNE: Delete {data}')
			if is_client:
				db.delete_payment(data[0])
				updateHandler.update_all()
				self.generate_button_handle()
			else:
				# db.delete_employee_payment(data[0])
				self.generate_button_handle()

		PopupWindow('Confirmare', f'Sterge plata client {data[1]} suma {data[2]}', lambda: confirm_delete(), True)

	def handle_back_button(self):
		self.update_payment_form.setParent(None)
		self.update_button.setParent(None)
		self.payments_data = None
		# self.payments_field.setParent(None)
		# self.payments_field = None
		self.back_button.setParent(None)
		self.back_button = None
		self.layout.addWidget(self.filters)
		self.layout.addWidget(self.generate_button)
		if self.payment_buttons:
			self.layout.addWidget(self.payment_buttons)
		if self.payments_field:
			self.layout.addWidget(self.payments_field)
		if self.current_payment_fields:
			self.layout.addWidget(self.current_payment_fields)
		self.layout.update()

	def handle_update_payment(self):
		print('called')
		print(self.update_payment_form.get_data())
		if type(self.update_payment_form.get_data()) == UpdateClientPaymentData:
			data = self.update_payment_form.get_data()
			print(f'(DONE)ACTIUNE: Update payment with: {data}')
			db.edit_payment(data.id, data.name, data.amount, data.individual_amounts, data.date, data.cash, data.observations)
			updateHandler.update_all()
			self.handle_back_button()
			return
		elif type(self.update_payment_form.get_data()) == UpdateEmployeePaymentData:
			print(f'(DEPRECATED)ACTIUNE: Update payment with: {self.update_payment_form.get_data()}')
			updateHandler.update_all()
			self.handle_back_button()
			return
		PopupWindow('Eroare', self.update_payment_form.get_data(), None, False)

	def update(self):
		self.generate_button_handle()

	def generate_pdf(self):
		if self.payments_data:
			print(self.payments_data)
			is_client = len(self.payments_data[0]) == 6
			workbook = xlsxwriter.Workbook(f'Plati_perioada_{self.filters.get_filters().start_date} - {self.filters.get_filters().end_date}_generat_pe_{str(date.today())}.xlsx')
			worksheet = workbook.add_worksheet()
			if is_client:
				for index, payment in enumerate(self.payments_data):
					worksheet.write(index, 0, payment[1])
					worksheet.write(index, 1, payment[2])
					worksheet.write(index, 2, payment[3])
					worksheet.write(index, 3, 'cash' if payment[4] else 'banca')
					worksheet.write(index, 4, payment[5])
			else:
				for index, payment in enumerate(self.payments_data):
					worksheet.write(index, 0, payment[1])
					worksheet.write(index, 1, payment[2])
					worksheet.write(index, 2, payment[3])
					worksheet.write(index, 3, payment[4])
					worksheet.write(index, 4, 'cash' if payment[5] else 'banca')
					worksheet.write(index, 5, payment[6])
			workbook.close()


class CurrentPayments(QWidget):
	def __init__(self, data):
		super().__init__()
		self.data = data
		self.total = self.set_total_price(self.data)
		self.length = len(self.data)

		self.total_field = QLabel(f'Total: {round(self.total, 2)}')
		self.total_field.setFont(QFont('Consolas', 15))

		self.length_field = QLabel(f'Nr plati: {self.length}')
		self.length_field.setFont(QFont('Consolas', 15))

		self.layout = QHBoxLayout()
		self.layout.addWidget(self.total_field)
		self.layout.addWidget(self.length_field)
		self.setLayout(self.layout)

	def set_total_price(self, data):
		return sum([payment[2] for payment in data])


class CurrentPayment(QWidget):
	def __init__(self, data):
		super().__init__()
		self.data = data
		self.observations = QLabel(f'Observatii: {str(data[-1])}')
		self.observations.setFont(QFont('Consolas', 13))
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.observations)
		self.setLayout(self.layout)


class PaymentFilters(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QHBoxLayout()
		self.entities = [ALL_ENTITIES] + get_clients()
		self.entities_field = SelectDelete(self.entities)
		self.client_or_employee_field = SelectDelete(['Client', 'Angajat'])

		self.period = QCheckBox('Aplica Perioada')
		self.period.click()

		self.start_date_field = QDateEdit(self)
		self.start_date_field.setCalendarPopup(True)
		self.start_date_field.setDate(date.today())

		self.end_date_field = QDateEdit(self)
		self.end_date_field.setCalendarPopup(True)
		self.end_date_field.setDate(date.today())

		self.apply = QPushButton('Aplica')
		self.apply.clicked.connect(lambda: print('apply filters'))

		self.layout.addWidget(self.client_or_employee_field)
		self.layout.addWidget(self.entities_field)
		self.layout.addWidget(self.period)
		self.layout.addWidget(self.start_date_field)
		self.layout.addWidget(self.end_date_field)

		self.client_or_employee_field.currentTextChanged.connect(lambda: self.client_or_employee_on_change())

		self.setLayout(self.layout)

	def client_or_employee_on_change(self):
		if self.client_or_employee_field.currentText() == 'Client':
			self.entities = [ALL_ENTITIES] + get_clients()
		else:
			self.entities = [ALL_ENTITIES] + get_employees()
		self.entities_field.reset(self.entities)
		self.entities_field.update()

	def get_filters(self):
		return FiltersData(
			client_or_employee=self.client_or_employee_field.currentText(),
			entity=self.entities_field.currentText(),
			apply_period=self.period.isChecked(),
			start_date=self.start_date_field.date().toPyDate(),
			end_date=self.end_date_field.date().toPyDate(),
		)

	def get_entities_field(self):
		if self.client_or_employee_field.currentText() != 'Client':
			return None

	def update(self):
		self.client_or_employee_on_change()
