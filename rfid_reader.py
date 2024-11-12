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
			self.parent.switch_btn_rfid_active(False)
			self.parent.rfid_state.config(text='Conectado', foreground='#00ff00')
		except serial.SerialException as e:
			if comport < len(self.ports)-1:
				self.connect_arduino(comport+1)

	def validate_code(self, code):
		if code in valid_codes:
			self.arduino.write('1'.encode())
		else:
			self.arduino.write('0'.encode())

	def read_from_arduino(self):
		try:
			while True:
				data = self.arduino.readline().decode('utf-8').strip()
				if data:
					self.validate_code(data)
				sleep(0.01)
		except serial.SerialException as e:
			self.parent.switch_btn_rfid_active(True)
			self.parent.rfid_state.config(text='Desconectado', foreground='#ff0000')