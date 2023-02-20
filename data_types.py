from dataclasses import dataclass

@dataclass
class AddEmployeeData():
	name: str
	surname: str
	date: str
	clients: list[str]

@dataclass
class AddClientData():
	name: str
	date: str
	employees: list[str]

@dataclass
class AddClientPaymentData():
	client: str
	amount: int
	individual_amounts: {str: str}
	date: str
	cash: int
	observations: str

@dataclass
class UpdateClientPaymentData():
	id: str
	name: str
	amount: int
	individual_amounts: {str: str}
	date: str
	cash: int
	observations: str

@dataclass
class UpdateEmployeePaymentData():
	id: str
	amount: int
	date: str
	cash: int
	observations: str

@dataclass
class FiltersData():
	client_or_employee: str
	entity: str
	apply_period: bool
	start_date: str
	end_date: str

@dataclass
class ReportFiltersData():
	client_or_employee: str
	start_date: str
	end_date: str
