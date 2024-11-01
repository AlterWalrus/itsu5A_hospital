import mysql.connector
from mysql.connector import Error

#Conexion con MySQL
#Recuerda encender el servicio de MySQL, si no, no sirve esta jalada
try:
	conn = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="taqueinge"
	)

	if conn.is_connected():
		print("Conectado con MySQL :)")
	
	dbcursor = conn.cursor()
except Error as e:
	print(f"Error en MySQL: {e}")
