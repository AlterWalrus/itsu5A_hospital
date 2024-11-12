import mysql.connector
from mysql.connector import Error

class MySQL_Conn:
	def __init__(self):
		self.conn = None
		self.dbcursor = None
		self.connect()

	def connect(self):
		#Conexion con MySQL (recuerda encender el servicio de MySQL, si no, no sirve esta jalada)
		try:
			self.conn = mysql.connector.connect(
				host="localhost",
				user="root",
				password="",
				database="hospitalv1"
			)
			self.dbcursor = self.conn.cursor(buffered=True)
		except Error as e:
			print(f"Error en MySQL: {e}")
	
	#AGREGAR VALOR A TABLA
	def insert_into(self, table_name, args_names, args_values):
		try:
			columns = ', '.join(args_names)
			placeholders = ', '.join(['%s'] * len(args_values))
			query = f"INSERT INTO {table_name}({columns}) VALUES({placeholders});"
			self.dbcursor.execute(query, args_values)
			self.conn.commit()

			print(f"query exitosa: {query}: {args_values}")
			return True
		except Error as e:
			print(f"Error en MySQL: {e}")
		return False

	#NOMBRES DE LAS TABLAS
	def get_columns(self, table_name):
		result = None
		try:
			query = f"SELECT * FROM {table_name} LIMIT 1;"
			self.dbcursor.execute(query)
			result = [i[0] for i in self.dbcursor.description]
		except Error as e:
			print(f"Error en MySQL: {e}")
		return result
	
	#De una lista de columnas quitar los PKs y FKs
	#Probablemente es una guarrada, pero me vale roña xdxdxdxd
	def only_own_columns(self, columns):
		return [col for col in columns if not col.startswith('id')]

	def get_table(self, table_name, getcolumns=False):
		columns = self.get_columns(table_name)[1:]
		foreign_keys = [col for col in columns if col.startswith('id')]
		table_alias = table_name[0:2]
		query = "SELECT"

		unique_columns = self.only_own_columns(columns)
		if len(foreign_keys) != 0:
			for u in unique_columns:
				query += f" {table_alias}.{u},"
		else:
			for u in unique_columns:
				query += f" {u}"
				if u != unique_columns[-1]:
					query += ","

		joins = ""
		for fk in foreign_keys:
			fk_table = fk[2:]
			fk_alias = fk_table[0:2]

			unique_columns = self.only_own_columns(self.get_columns(fk_table))
			for u in unique_columns:
				query += f" {fk_alias}.{u}"
				if u != unique_columns[-1] or fk != foreign_keys[-1]:
					query += ","
			
			joins += f" INNER JOIN {fk_table} {fk_alias} ON {table_alias}.{fk} = {fk_alias}.{fk}"
		query += f" FROM {table_name} {table_alias}{joins};" if len(foreign_keys) != 0 else f" FROM {table_name};"
		try:
			self.dbcursor.execute(query)
			if getcolumns:
				result = [i[0] for i in self.dbcursor.description]
				return result
			return self.dbcursor.fetchall()
		except Error as e:
			print(f"Error en MySQL: {e}")
		return []