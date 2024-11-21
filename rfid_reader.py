import serial
import threading
from datetime import datetime
from time import sleep
import serial.tools.list_ports

class RFID_Reader:
	def __init__(self, parent):
		self.parent = parent
		self.reader = None
		self.thread = None
		self.connected = False

		self.mode = 1
		self.target_window = None

		self.entrance_time = {}

		self.update_valid_codes()
		self.connect_reader()

	def update_valid_codes(self):
		rfid_codes = self.parent.db.get_table('codigorfid')
		self.valid_codes = [c[0] for c in rfid_codes]

	def connect_reader(self, comport=0):
		try:
			self.ports = [comport.device for comport in serial.tools.list_ports.comports()]
			self.ports.append('CUM')
			
			self.reader = serial.Serial(self.ports[comport], 9600)
			self.thread = threading.Thread(target=self.read_from_arduino, daemon=True)
			self.thread.start()
			self.parent.frames['MainMenu'].switch_btn_rfid_active(False)
			self.parent.frames['MainMenu'].rfid_state.config(text='Conectado', foreground='#00ff00')
			self.connected = True
		except serial.SerialException:
			if comport < len(self.ports)-1:
				self.connect_reader(comport+1)

	def validate_code(self, code):
		if code not in self.valid_codes:
			self.reader.write('0'.encode())
			return

		main = self.parent.frames['MainMenu']
		room = 'A1'
		
		if code in main.rooms[room].visitors:
			main.rooms[room].exit_visitor(code)
			now = datetime.today().replace(microsecond=0)
			id_code = self.parent.db.get_id_rfid(code)
			print(f"{self.entrance_time[code]} - {now} - {1} - {id_code}")
			self.parent.db.insert_into('visita', ('entrada', 'salida', 'idPaciente', 'idCodigoRFID'), (self.entrance_time[code], now, 1, id_code))
			self.parent.frames['Visitas'].update_table()
		else:
			main.rooms[room].enter_visitor(code)
			self.entrance_time[code] = datetime.today().replace(microsecond=0)

		self.reader.write('1'.encode())
		main.update_room_visits()

	def process_data(self, data):
		if self.mode == 1:
			self.validate_code(data)

		elif self.mode == 2:
			from ttkbootstrap import END as end
			self.target_window.entries['codigoRFID'].delete(0, end)
			self.target_window.entries['codigoRFID'].insert(0, data)
			self.target_window.switch_rfid_mode()
			self.mode = 1
		
		elif self.mode == 3:
			print(data)
			self.target_window.lb_rfid['text'] = f"Codigo RFID: {data}"
			if data in self.valid_codes:
				ids = self.parent.db.get_ids('codigoRFID')
				id = ids[self.valid_codes.index(data)]
				result: dict = self.parent.db.get_rfid_owner(id)
				self.target_window.lb_title['foreground'] = '#00ff00'
				self.target_window.lb_title['text'] = "Registro encontrado"
				for k in result.keys():
					self.target_window.lb_info['text'] += f"{k}: {result[k]}\n"
			else:
				self.target_window.lb_title['foreground'] = '#ff5555'
				self.target_window.lb_title['text'] = "Oops..."
				self.target_window.lb_info['text'] = "Tarjeta no registrada en el sistema."
			
			self.target_window.btn_ok['text'] = 'Ok'
			from data_window import center_window
			center_window(self.target_window)
			self.mode = 1

	def read_from_arduino(self):
		try:
			while True:
				data = self.reader.readline().decode('utf-8').strip()
				if data:
					self.process_data(data)
				sleep(0.01)
		except serial.SerialException:
			self.parent.frames['MainMenu'].switch_btn_rfid_active(True)
			self.parent.frames['MainMenu'].rfid_state.config(text='Desconectado', foreground='#ff5555')
			self.connected = False