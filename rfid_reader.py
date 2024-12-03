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
		#Revisar si el codico esta en la base de datos
		if code not in self.valid_codes:
			self.reader.write('0'.encode())
			self.reader.write("Codigo no registrado".encode())
			return

		#Revisar si hay alguien en la habitacion hospedado en primer lugar
		room = 'A1'
		room_id = self.parent.db.get_id('Habitacion', 'nombreHabitacion', room)
		patient_id = self.parent.db.get_id_from_room(room_id, get_room=False)
		
		if patient_id == -1:
			self.reader.write('0'.encode())
			self.reader.write("Habitacionvacia".encode())
			return
		
		#Si se es medico las demas validaciones son burladas
		rfid_id = self.parent.db.get_id('CodigoRFID', 'codigoRFID', code)
		rfid_owner = self.parent.db.get_rfid_owner(rfid_id)
		if 'cedula' in rfid_owner:
			self.checkin(room_id, patient_id, code)
			return

		#Se hace el check in
		self.checkin(room_id, patient_id, code)

	def checkin(self, room_id, patient_id, code):
		if code in self.entrance_time.keys():
			now = datetime.today().replace(microsecond=0)
			id_code = self.parent.db.get_id('CodigoRFID', 'codigoRFID', code)
			print(f"{self.entrance_time[code]} - {now} - {1} - {id_code}")
			self.parent.db.insert_into('visita', ('entrada', 'salida', 'idHabitacion', 'idPaciente', 'idCodigoRFID'), (self.entrance_time[code], now, room_id, patient_id, id_code))
			self.parent.frames['Visitas'].update_table()
			self.entrance_time.pop(code, None)
			self.reader.write('3'.encode())

			self.parent.frames['MainMenu'].week_data[-1] += 1
			self.parent.frames['MainMenu'].today_data[-1] += 1
			self.parent.frames['MainMenu'].after_resize()
		else:
			self.entrance_time[code] = datetime.today().replace(microsecond=0)
			self.reader.write('1'.encode())

	def process_data(self, data):
		if self.mode == 1:
			self.validate_code(data)

		elif self.mode == 2:
			from ttkbootstrap import END as end
			self.target_window.entries['codigoRFID'].delete(0, end)
			self.target_window.entries['codigoRFID'].insert(0, data)
			self.target_window.switch_rfid_mode()
			self.mode = 1
			self.reader.write('2'.encode())
			print("BEEP")
		
		elif self.mode == 3:
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
			
			self.reader.write('2'.encode())
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