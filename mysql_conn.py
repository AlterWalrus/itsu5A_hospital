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

	#Sacar ID segun se provea ID del paciente o habitacion
	def get_id_from_room(self, id, get_room=True):
		result = []
		to_get = 'idHabitacion'
		id_field = 'idPaciente'
		if not get_room:
			to_get, id_field = id_field, to_get
		query = f"SELECT {to_get} FROM Estancia WHERE {id_field} = %s"
		try:
			self.dbcursor.execute(query, (id,))
			result = self.dbcursor.fetchall()
			if len(result) > 0:
				return result[0][0]
		except Error as e:
			print(f"Error en MySQL: {e}")
		return -1
	
	#Agregar valor a la tabla de estancias
	def insert_into_room(self, id_patient, id_room):
		query = "INSERT INTO Estancia (idPaciente, idHabitacion) VALUES(%s, %s);"
		try:
			self.dbcursor.execute(query, (id_patient, id_room))
			self.conn.commit()
		except Error as e:
			print(f"Error en MySQL: {e}")

	#Actualizar valor en la tabla de estancias
	def update_from_room(self, id_patient, id_room):
		query = "UPDATE Estancia SET idHabitacion = %s WHERE idPaciente = %s;"
		try:
			self.dbcursor.execute(query, (id_room, id_patient))
			self.conn.commit()
		except Error as e:
			print(f"Error en MySQL: {e}")
	
	#Eliminar valor de la tabla de estancias
	def delete_from_room(self, id_patient):
		query = "DELETE FROM Estancia WHERE idPaciente = %s;"
		try:
			self.dbcursor.execute(query, (id_patient,))
			self.conn.commit()
		except Error as e:
			print(f"Error en MySQL: {e}")

	#Agregar valor a la tabla
	def insert_into(self, table_name, args_names, args_values):
		columns = ', '.join(args_names)
		placeholders = ', '.join(['%s'] * len(args_values))
		query = f"INSERT INTO {table_name}({columns}) VALUES({placeholders});"
		try:
			self.dbcursor.execute(query, args_values)
			new_id = self.dbcursor._last_insert_id
			self.conn.commit()
			print(f"query exitosa: {query}: {args_values}")
			return new_id
		except Error as e:
			print(f"Error en MySQL: {e}")
		return -1
	
	#Editar valor a la tabla
	def update(self, table_name, id, args_names, args_values):
		changes_list = []
		for arg in args_names:
			changes_list.append(f" {arg} = %s")
		changes = ','.join(changes_list)
		query = f"UPDATE {table_name} SET{changes} WHERE id{table_name} = %s;"
		args_values.append(id)
		try:
			self.dbcursor.execute(query, args_values)
			self.conn.commit()
			print(f"query exitosa: {query}: {args_values}")
		except Error as e:
			print(f"Error en MySQL: {e}")

	#Eliminar (no borrar... o si? a mi que carajos me importa) valor de tabla
	def delete(self, table_name, ids):
		query = f"DELETE FROM {table_name} WHERE id{table_name} IN ("
		query += ','.join(["%s"] * len(ids))
		query += ');'
		print(query)
		try:
			self.dbcursor.execute(query, ids)
			self.conn.commit()
			print(f"query exitosa: {len(ids)} elemento(s) eliminado(s)")
		except Error as e:
			print(f"Error en MySQL: {e}")

	#Leer un registro tal como es
	def get_raw_data(self, table_name, id):
		query = f"SELECT * FROM {table_name} WHERE id{table_name} = %s;"
		try:
			self.dbcursor.execute(query, (id,))
			result = self.dbcursor.fetchall()
			return result[0]
		except Error as e:
			print(f"Error en MySQL: {e}")
		return -1

	#Leer tabla tal como es
	def get_raw_table(self, table_name):
		result = []
		query = f"SELECT * FROM {table_name};"
		try:
			self.dbcursor.execute(query)
			result = self.dbcursor.fetchall()
		except Error as e:
			print(f"Error en MySQL: {e}")
		return result

	#Nombres de las columnas
	def get_columns(self, table_name):
		result = []
		query = f"SELECT * FROM {table_name} LIMIT 1;"
		try:
			self.dbcursor.execute(query)
			result = [i[0] for i in self.dbcursor.description]
		except Error as e:
			print(f"Error en MySQL: {e}")
		return result
	
	#De una lista de columnas quitar los PKs y FKs
	#Probablemente es una guarrada, pero me vale roña xdxdxdxd
	def only_own_columns(self, columns):
		return [col for col in columns if not col.startswith('id')]

	def get_table(self, table_name, getcolumns=False, id=None):
		columns = self.get_columns(table_name)[1:]
		foreign_keys = [col for col in columns if col.startswith('id')]
		has_foreign_keys = len(foreign_keys) == 0
		table_alias = table_name[0:2]
		query = "SELECT"

		where = ""
		if id:
			where = f"WHERE id{table_name} = {id}"
		if getcolumns:
			where = "LIMIT 1"

		own_columns = self.only_own_columns(columns)
		if not has_foreign_keys:
			for u in own_columns:
				query += f" {table_alias}.{u},"
		else:
			query += ','.join([f" {u}" for u in own_columns])

		joins = ""
		for fk in foreign_keys:
			fk_table = fk[2:]
			fk_alias = fk_table[0:2]
			own_columns = self.only_own_columns(self.get_columns(fk_table))
			query += ','.join([f" {fk_alias}.{u}" for u in own_columns])
			if fk != foreign_keys[-1]:
				query += ','
			joins += f" INNER JOIN {fk_table} {fk_alias} ON {table_alias}.{fk} = {fk_alias}.{fk}"
		query += f" FROM {table_name} {table_alias}{joins} {where};" if not has_foreign_keys else f" FROM {table_name} {where};"
		try:
			self.dbcursor.execute(query)
			if getcolumns:
				return [i[0] for i in self.dbcursor.description]
			return self.dbcursor.fetchall()
		except Error as e:
			print(f"Error en MySQL: {e}")
		return []
	
	def get_id(self, table_name, field, value):
		query = f"SELECT id{table_name} FROM {table_name} WHERE {field} = %s;"
		try:
			self.dbcursor.execute(query, (value,))
			return self.dbcursor.fetchall()[0][0]
		except Error as e:
			print(f"Error en MySQL: {e}")
		return -1
	
	def get_ids(self, table_name):
		result = []
		query = f"SELECT id{table_name} FROM {table_name};"
		try:
			self.dbcursor.execute(query)
			result_tuples = self.dbcursor.fetchall()
			result = [i[0] for i in result_tuples]
		except Error as e:
			print(f"Error en MySQL: {e}")
		return result

	def get_rfid_owner(self, id_rfid):
		query = f'''
				SELECT 'medico' AS tipo, idMedico AS id FROM medico WHERE idCodigoRFID = {id_rfid} UNION
				SELECT 'enfermero' AS tipo, idEnfermero AS id FROM enfermero WHERE idCodigoRFID = {id_rfid} UNION
				SELECT 'visitante' AS tipo, idVisitante AS id FROM visitante WHERE idCodigoRFID = {id_rfid};
				'''
		try:
			self.dbcursor.execute(query)
			res = self.dbcursor.fetchall()
			table = res[0][0]
			id = res[0][1]
			fields = self.get_table(table, getcolumns=True)
			values = self.get_table(table, id=id)[0]
			d = {}
			for i in range(len(fields)):
				d[fields[i]] = values[i]
			return d
		except Error as e:
			print(f"Error en MySQL: {e}")
		return -1
