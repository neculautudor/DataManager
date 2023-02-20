from datetime import date

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit, QSizePolicy

from data_types import ReportFiltersData
from frontend.DataFetching.get_data import get_clients, get_employees, get_period_payments
from frontend.components.CommonComponents.common_components import SelectDelete
from frontend.components.Root.UpdateHandler import updateHandler
import xlsxwriter

class Reports(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.report_filters = ReportFilters()
		self.scrollable_reports = None
		self.generate_button = QPushButton('Genereaza')
		self.generate_button.clicked.connect(lambda: self.generate_button_handle())
		self.export_pdf_button = QPushButton('Export Excel')
		self.export_pdf_button.clicked.connect(lambda: self.generate_pdf())

		self.layout.addWidget(self.report_filters)
		self.layout.addWidget(self.generate_button)
		self.layout.addWidget(self.export_pdf_button)
		self.setLayout(self.layout)

		updateHandler.add_object(self)

	def generate_button_handle(self):
		if self.scrollable_reports:
			self.scrollable_reports.setParent(None)
		self.scrollable_reports = ScrollableReports(self.report_filters.get_filters())
		self.layout.addWidget(self.scrollable_reports)

	def generate_pdf(self):
		if self.scrollable_reports:
			payments_data = self.scrollable_reports.get_fields_data()
			workbook = xlsxwriter.Workbook(f'Plati {self.report_filters.get_chosen_entity()}-{str(date.today())}.xlsx')
			worksheet = workbook.add_worksheet()
			for index, payment in enumerate(payments_data):
				worksheet.write(index, 0, payment[0])
				worksheet.write(index, 1, payment[1])
			workbook.close()

	def update(self):
		if self.scrollable_reports:
			self.generate_button_handle()

class ReportFilters(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QHBoxLayout()
		self.entities = ['Clienti', 'Angajati']
		self.entities_field = SelectDelete(self.entities)

		self.start_date_field = QDateEdit(self)
		self.start_date_field.setCalendarPopup(True)
		self.start_date_field.setDate(date.today().replace(day=1))

		self.end_date_field = QDateEdit(self)
		self.end_date_field.setCalendarPopup(True)
		self.end_date_field.setDate(date.today())

		self.layout.addWidget(self.entities_field)
		self.layout.addWidget(self.start_date_field)
		self.layout.addWidget(self.end_date_field)
		self.setLayout(self.layout)

	def get_filters(self):
		return ReportFiltersData(
			client_or_employee=self.entities_field.currentText(),
			start_date=self.start_date_field.date().toPyDate(),
			end_date=self.end_date_field.date().toPyDate(),
		)

	def get_chosen_entity(self):
		return self.entities_field.currentText()

class ScrollableReports(QScrollArea):
	def __init__(self, data: ReportFiltersData):
		super().__init__()
		self.data = data
		self.widget = QWidget()
		self.layout = QVBoxLayout()
		self.fields_data = None
		self.fields = self.generate_fields(self.data)
		self.add_fields(self.fields)

		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)

	def generate_fields(self, data):
		entity_type = data.client_or_employee
		entities = get_clients() if entity_type == 'Clienti' else get_employees()
		fields_data = []
		for entity in entities:
			field = get_period_payments(entity_type, entity, data.start_date, data.end_date)
			if field:
				fields_data.append([field[0][1], sum([individual[2] for individual in field])])
		fields = []
		for field in fields_data:
			widget = QWidget()
			layout = QHBoxLayout()
			nume = QLabel(text=f'{field[0]}')
			nume.setStyleSheet("border: 1px solid black;")
			# nume.resize(1000, 1000)
			suma = QLabel(text=f'  TOTAL --- {field[1]}lei')
			nume.setFont(QFont('Times', 15))
			suma.setFont(QFont('Times', 15))


			layout.addWidget(nume)
			layout.addWidget(suma)
			widget.setLayout(layout)

			fields.append(widget)
		self.fields_data = fields_data
		return fields

	def add_fields(self, fields):
		for field in fields:
			self.layout.addWidget(field)

	def get_fields_data(self):
		return self.fields_data