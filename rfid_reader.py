import serial
import threading
from datetime import datetime
from time import sleep

valid_codes = ['D3210225']

class RFID_Reader:
	def __init__(self, parent):
		self.parent = parent
		self.arduino = None
		self.thread = None
		self.connect_arduino()

	def connect_arduino(self):
		try:
			self.arduino = serial.Serial('COM6', 9600)
			self.thread = threading.Thread(target=self.read_from_arduino, daemon=True)
			self.thread.start()
			self.parent.log_print("Conexión establecida correctamente.\n", 'ok')
			self.parent.switch_rfid_btn_active(False)
		except serial.SerialException as e:
			self.parent.log_print(f"No se pudo conectar con el lector RFID.\n", 'error')
			self.parent.log_print(f"Error: {e}\n", 'error')
			self.parent.switch_rfid_btn_active(True)

	def validate_code(self, code):
		if code in valid_codes:
			self.arduino.write('1'.encode())
			self.parent.log_print(f"Acceso CONCEDIDO para {code}. {datetime.now()}\n")
		else:
			self.arduino.write('0'.encode())
			self.parent.log_print(f"Acceso DENEGADO para {code}. {datetime.now()}\n")

	def read_from_arduino(self):
		try:
			while True:
				data = self.arduino.readline().decode('utf-8').strip()
				if data:
					self.validate_code(data)
				sleep(0.01)
		except serial.SerialException as e:
			self.parent.log_print(f"Desconexion con el lector RFID.\n", 'error')
			self.parent.log_print(f"Error: {e}\n", 'error')
			self.parent.switch_rfid_btn_active(True)