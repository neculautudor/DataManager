import os
import sqlite3


class Database(object):
	def __init__(self):
		if not os.path.isfile('firme_si_angajati.db'):
			file = open('firme_si_angajati.db', 'a+')
			file.close()
		self.connection = sqlite3.connect('firme_si_angajati.db')
		self.cursor = self.connection.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS angajat (nume	TEXT, data TEXT, UNIQUE (nume) ON CONFLICT REPLACE)')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS client (nume TEXT, date_added TEXT, UNIQUE (nume) ON CONFLICT REPLACE)')
		self.cursor.execute(
			'CREATE TABLE IF NOT EXISTS client_to_angajat (nume_client TEXT, nume_angajat	TEXT, UNIQUE(nume_client, nume_angajat) ON CONFLICT REPLACE)')
		self.cursor.execute(
			'CREATE TABLE IF NOT EXISTS plata_angajat (id	INTEGER, nume_angajat TEXT, suma REAL, client TEXT, data TEXT, cash	INTEGER, observatii	TEXT)')
		self.cursor.execute(
			'CREATE TABLE IF NOT EXISTS plata_client (nume_client	TEXT, suma REAL, date_added	TEXT, cash INTEGER, observatii TEXT)')
		self.connection.commit()
		# self.cursor.row_factory = lambda cursor, row: row[0]

	def test(self):
		# self.cursor.execute('CREATE TABLE client2 (nume TEXT, date_added TEXT, UNIQUE (nume) ON CONFLICT REPLACE)')
		# self.cursor.execute('INSERT INTO client2 SELECT * FROM client')
		self.cursor.execute('DROP TABLE client')
		self.cursor.execute('ALTER TABLE client2 RENAME TO client')
		self.connection.commit()

	# DATA EDITING
	def create_table(self, creation):
		self.cursor.execute(creation)

	def insert_value(self, table, values):
		self.cursor.execute('INSERT INTO %s VALUES %s' % (table, str(values)))
		self.connection.commit()

	def select(self):
		rows = self.cursor.execute('SELECT nume_angajat, suma, data FROM plata_angajat').fetchall()
		print([row[0] for row in rows])

	def delete(self, table, row, value):
		self.cursor.execute("DELETE FROM %s WHERE %s = '%s'" % (table, row, value))
		self.connection.commit()

	def add_payment(self, client, suma, sume_individuale, data, cash, observatii):
		angajati = sume_individuale.keys()
		self.cursor.execute('INSERT INTO %s VALUES %s' % ('plata_client', str((client, suma, str(data), cash, observatii))))
		rowid = self.cursor.execute('SELECT last_insert_rowid()').fetchall()[0]
		for angajat in angajati:
			self.cursor.execute('INSERT INTO %s VALUES %s' % ('plata_angajat', str((rowid[0], angajat, sume_individuale[angajat], client, str(data), cash, observatii))))
		self.connection.commit()

	def delete_employee_payments(self, id):
		self.cursor.execute("DELETE FROM plata_angajat WHERE id = '%d'" % id)
		self.connection.commit()

	def edit_payment(self, id, client, suma, sume_individuale, data, cash, observatii):
		self.delete_payment(id)
		self.add_payment(client, suma, sume_individuale, data, cash, observatii)

	def delete_payment(self, id):
		self.cursor.execute("DELETE FROM plata_client WHERE rowid = '%d'" % id)
		self.cursor.execute("DELETE FROM plata_angajat WHERE id = '%d'" % id)
		self.connection.commit()

	def modify_employee_payment(self, primary_key, suma):
		self.cursor.execute("UPDATE plata_angajat SET suma = %d WHERE id = '%d'" % (suma, primary_key))
		self.connection.commit()

	def add_client(self, client, angajati, data):
		self.cursor.execute('INSERT INTO %s VALUES %s' % ('client', str((client, str(data)))))
		self.cursor.execute("DELETE FROM client_to_angajat WHERE nume_client = '%s'" % client)
		for angajat in angajati:
			self.cursor.execute('INSERT INTO %s VALUES %s' % ('client_to_angajat', str((client, angajat))))
		self.connection.commit()

	def delete_client(self, client):
		self.cursor.execute("DELETE FROM client WHERE nume = '%s'" % client)
		self.cursor.execute("DELETE FROM client_to_angajat WHERE nume_client = '%s'" % client)
		self.connection.commit()

	def add_employee(self, angajat, clienti, data):
		self.cursor.execute('INSERT INTO %s VALUES %s' % ('angajat', str((angajat, str(data)))))
		self.cursor.execute("DELETE FROM client_to_angajat WHERE nume_angajat = '%s'" % angajat)
		for client in clienti:
			self.cursor.execute('INSERT INTO %s VALUES %s' % ('client_to_angajat', str((client, angajat))))
		self.connection.commit()

	def delete_employee(self, employee):
		self.cursor.execute("DELETE FROM angajat WHERE nume = '%s'" % employee)
		self.cursor.execute("DELETE FROM client_to_angajat WHERE nume_angajat = '%s'" % employee)
		self.connection.commit()

	# DATA FETCHING
	def get_employees(self):
		return self.cursor.execute("SELECT * FROM angajat").fetchall()

	def get_clients(self):
		return self.cursor.execute("SELECT * FROM client ORDER BY nume").fetchall()

	def get_employee_clients(self, employee):
		return self.cursor.execute("SELECT nume_client FROM client_to_angajat WHERE nume_angajat = '%s'" % employee).fetchall()

	def get_client_employees(self, client):
		return self.cursor.execute("SELECT nume_angajat FROM client_to_angajat WHERE nume_client = '%s'" % client).fetchall()

	def get_all_client_payments(self):
		return self.cursor.execute("SELECT rowid, * FROM plata_client ORDER BY date_added DESC").fetchall()

	def get_specific_client_payments(self, client):
		return self.cursor.execute("SELECT rowid, * FROM plata_client WHERE nume_client = '%s' ORDER BY date_added DESC" % client).fetchall()

	def get_all_employee_payments(self):
		return self.cursor.execute("SELECT * FROM plata_angajat ORDER BY data DESC").fetchall()

	def get_specific_employee_payments(self, employee):
		return self.cursor.execute("SELECT * FROM plata_angajat WHERE nume_angajat = '%s' ORDER BY data DESC" % employee).fetchall()

	def get_period_client_payments(self, date1, date2):
		return self.cursor.execute(
			"SELECT rowid, * FROM plata_client WHERE date_added >= '%s' AND date_added <= '%s' ORDER BY date_added DESC" % (date1, date2)
		).fetchall()

	def get_period_employee_payments(self, date1, date2):
		return self.cursor.execute(
			"SELECT * FROM plata_angajat WHERE data >= '%s' AND data <= '%s' ORDER BY data DESC" % (date1, date2)
		).fetchall()

	def get_period_specific_client_payments(self, client, date1, date2):
		return self.cursor.execute(
			"SELECT rowid, * FROM plata_client WHERE nume_client = '%s' AND date_added >= '%s' AND date_added <= '%s' ORDER BY date_added DESC" % (client, date1, date2)
		).fetchall()

	def get_period_specific_employee_payments(self, employee, date1, date2):
		return self.cursor.execute(
			"SELECT * FROM plata_angajat WHERE nume_angajat = '%s' AND data >= '%s' AND data <= '%s' ORDER BY data DESC" % (employee, date1, date2)
		).fetchall()

	def get_employee_payments_by_id(self, id):
		return self.cursor.execute(f"SELECT nume_angajat, suma FROM plata_angajat WHERE id = '{id}'").fetchall()
