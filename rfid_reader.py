import serial
import threading
from datetime import datetime
from time import sleep
import serial.tools.list_ports

valid_codes = ['D3210225']

class RFID_Reader:
	def __init__(self, parent):
		self.com_port = 'COM6'
		self.parent = parent
		self.arduino = None
		self.thread = None

		self.connect_arduino()

	def connect_arduino(self, comport=0):
		try:
			self.ports = [comport.device for comport in serial.tools.list_ports.comports()]
			self.ports.append('CUM')
			
			self.arduino = serial.Serial(self.ports[comport], 9600)
			self.thread = threading.Thread(target=self.read_from_arduino, daemon=True)
			self.thread.start()

			self.parent.log_print(f"Conexión establecida correctamente con el {self.ports[comport]}.\n", 'ok')
			self.parent.switch_rfid_btn_active(False)
			
		except serial.SerialException as e:
			if comport < len(self.ports)-1:
				self.connect_arduino(comport+1)
			else:
				self.parent.log_print(f"No se pudo conectar con el lector RFID. {comport+1} intento(s).\n", 'error')
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