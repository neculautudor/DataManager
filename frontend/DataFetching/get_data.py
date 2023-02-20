from backend.DBConnection import db


def get_clients():
	return [client[0] for client in db.get_clients()]


def get_employees():
	return [employee[0] for employee in db.get_employees()]


def get_period_payments(entity_type, entity_name, date1, date2):
	return db.get_period_specific_client_payments(entity_name, date1, date2)\
			if entity_type == 'Clienti' else\
			db.get_period_specific_employee_payments(entity_name, date1, date2)


def get_client_employees(client):
	return [employee[0] for employee in db.get_client_employees(client)]


def get_employee_clients(employee):
	return [employee[0] for employee in db.get_employee_clients(employee)]
