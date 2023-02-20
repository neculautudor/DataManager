from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from frontend.components.CommonComponents.common_components import Button, SelectableButton
from datetime import datetime


class ScrollablePaymentButtons(QScrollArea):
	def __init__(self, buttons_data, current_data_setter, handle_edit_payment, handle_delete_payment):
		super().__init__()
		self.handle_edit_payment = handle_edit_payment
		self.handle_delete_payment = handle_delete_payment
		self.buttons_data = buttons_data
		self.current_data_setter = current_data_setter
		self.widget = QWidget()
		self.layout = QVBoxLayout()
		self.add_buttons(buttons_data)
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.current_button = None

	def add_buttons(self, buttons_data):
		for data in buttons_data:
			button = PaymentWidget(data, self.set_current_button, self.handle_edit_payment, self.handle_delete_payment)
			self.layout.addWidget(button)

	def set_current_button(self, current_button):
		if self.current_button != current_button:
			if self.current_button:
				self.current_button.select_or_deselect()
			self.current_button = current_button
			self.current_data_setter(self.current_button.get_button_data())
		else:
			self.current_button = None

	def get_current_buttons_data(self):
		return self.buttons_data

	def get_current_button_data(self):
		return self.current_button


class PaymentWidget(QWidget):
	def __init__(self, data, current_setter, handle_edit_payment, handle_delete_payment):
		super().__init__()
		self.data = data
		self.is_client = len(self.data) == 6
		self.current_setter = current_setter
		self.handle_edit_payment = handle_edit_payment
		self.layout = QHBoxLayout()
		self.payment_button = PaymentButton(data, self.current_setter)
		self.edit_payment_button = EditPaymentButton(data, lambda: self.handle_edit_payment(data=self.data, is_client=self.is_client))
		self.delete_payment_button = Button('Sterge', lambda: handle_delete_payment(self.data), 'frontend/icons/delete.png')
		self.layout.addWidget(self.payment_button)
		if self.is_client:
			self.layout.addWidget(self.edit_payment_button)
			self.layout.addWidget(self.delete_payment_button)
		self.setLayout(self.layout)


class PaymentButton(SelectableButton):
	def __init__(self, data, current_setter):
		self.data = data
		self.current_setter = current_setter
		self.is_client = len(self.data) == 6
		self.isCash = self.set_isCash()
		self.name = self.data[1].ljust(10, ' ')
		self.full_name = self.set_full_name()
		super().__init__(self.full_name, lambda: self.current_setter(self))
		self.setFont(QFont('Times', 13))

	def get_button_data(self):
		return self.data

	def set_full_name(self):
		if self.is_client:
			date = datetime.strptime(self.data[3], '%Y-%m-%d').strftime('%d-%m-%Y')
			return f"{self.name} --- {self.data[2]}lei ---- {date} ---- {self.isCash} --- Obs: {self.data[-1][:20] + '...' if self.data[-1] else ''}"
		date = datetime.strptime(self.data[4], '%Y-%m-%d').strftime('%d-%m-%Y')
		return f"{self.name} --- {self.data[2]}lei ---- {date} ---- {self.isCash} ---- Client: {self.data[3]} --- Obs: {self.data[-1][:20] + '...' if self.data[-1] else ''}"

	def set_isCash(self):
		if self.is_client:
			return 'Cash' if self.data[4] else 'Bancar'
		return 'Cash' if self.data[5] else 'Bancar'


class EditPaymentButton(QPushButton):
	def __init__(self, data, handle_edit_payment):
		super().__init__()
		self.handle_edit_payment = handle_edit_payment
		self.setText('Edit')
		self.clicked.connect(self.handle_edit_payment)