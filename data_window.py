import ttkbootstrap as ttk
from datetime import datetime
from math import ceil

#"A shitty structure causes shitty problems, which require shitty solutions"

def center_window(w):
	w.master.update_idletasks()
	x_center = w.origin.controller.winfo_x() + (w.origin.controller.winfo_width()//2) - (w.master.winfo_reqwidth()//2)
	y_center = w.origin.controller.winfo_y() + (w.origin.controller.winfo_height()//2) - (w.master.winfo_reqheight()//2)
	w.master.geometry(f"+{x_center}+{y_center}")

class DataWindow(ttk.Frame):
	def __init__(self, parent, origin, db, table_name, fields, field_names, mode, id=0, curr_values=None):
		super().__init__(parent)
		self.master.iconbitmap("images/icon_dark.ico")
		self.origin = origin
		self.db = db
		self.pack(fill='x', expand=True)
		self.table_name = table_name
		self.fields = fields
		self.id = id
		self.field_names = field_names
		self.mode = mode

		self.btn_rfid = None

		self.master.title("Agregar registro" if mode == 'add' else "Editar registro")
		ttk.Label(self, text="Ingrese los datos cuidadosamente.", width=60, anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=4, padx=10, pady=10)

		#Campos a llenar y otras weas
		self.entries = {}
		col = 0
		half = ceil(len(fields)/2)
		i = 0
		j = 0
		for field in fields:
			if i == half:
				i = 0
				col += 2
			lb = ttk.Label(self, text=field_names[fields.index(field)], width=10, anchor='e')
			lb.grid(row=i+1, column=col, padx=2, pady=5)

			if field == 'codigoRFID' and self.origin.controller.reader.connected:
				self.btn_rfid = ttk.Button(self, width=10, text='Código RFID', command=self.switch_rfid_mode, style='Outline.info.TButton')
				self.btn_rfid.grid(row=i+1, column=col, padx=2, pady=5)
			
			entry = ttk.Entry(self)
			if field == 'horarioInicio' or field == 'horarioFin':
				entry.insert(0, 'HH:MM:SS')

			elif field == 'fechaNacimiento':
				entry.insert(0, 'AAAA-MM-DD')

			elif field == 'estado' and table_name == 'paciente':
				entry = ttk.Combobox(self)
				entry['values'] = db.get_table('estadopaciente')
				if curr_values:
					entry.insert(0, curr_values[j])
				entry['state'] = 'readonly'
				entry.bind("<<ComboboxSelected>>", self.after_state_selection)

			elif field == 'nombreHabitacion' and table_name == 'paciente':
				entry = ttk.Combobox(self)
				entry['values'] = [h[0] for h in db.get_table('habitacion') if h[1] == 'SI']
				if curr_values:
					entry.insert(0, curr_values[j])
				entry['state'] = 'readonly' if self.entries['estado'].get() != 'ALTA' else 'disabled'

			if curr_values:
				entry.delete(0, ttk.END)
				entry.insert(0, curr_values[j])
			
			entry.grid(row=i+1, column=col+1, padx=10, pady=5, sticky='ew')
			self.entries[field] = entry
			i += 1
			j += 1

		self.alert = ttk.Label(self, foreground='#ff5555', font=('Helvetica', 8, 'bold'))
		self.alert.grid(row=half+1, column=0, columnspan=3, padx=10)

		frame = ttk.Frame(self)
		frame.grid(row=half+1, column=3, padx=10, pady=10)
		com = self.confirm_insert if mode == 'add' else self.confirm_update
		ttk.Button(frame, text="Cancelar", command=self.close, style='Outline.TButton').grid(row=half+1, column=2, padx=10, pady=10, columnspan=1)
		ttk.Button(frame, text="Aceptar", command=com, style='success.TButton').grid(row=half+1, column=3, padx=10, pady=10, columnspan=1)

		for i in range(4):
			self.grid_columnconfigure(i, weight=1)
		self.grab_set()

		center_window(self)
	
	def after_state_selection(self, event):
		if self.entries['estado'].get() == 'ALTA':
			self.entries['nombreHabitacion'].set('')
			self.entries['nombreHabitacion']['state'] = 'disabled'
		else:
			self.entries['nombreHabitacion']['state'] = 'readonly'
	
	def switch_rfid_mode(self):
		rfid = self.origin.controller.reader
		if self.btn_rfid['text'] == "Esperando...":
			self.btn_rfid['text'] = "Código RFID"
			rfid.target_window = None
			rfid.mode = 1
		else:
			self.btn_rfid['text'] = "Esperando..."
			rfid.target_window = self
			rfid.mode = 2
		
	def data_is_valid(self):
		values = [v.get() for v in self.entries.values()]
		for i in range(len(self.fields)):
			field = self.fields[i]
			value = values[i]

			#Si el paciente esta de alta entonces habitacion estara vacio (es el unico campo que tiene permitido estar vacio)
			if field == 'estado' and value == "ALTA":
				break

			if value == "":
				self.alert['text'] = "Todavía hay campos sin llenar."
				return False
			
			if field == 'codigoRFID':
				if self.mode == 'add':
					codes = [c[0] for c in self.db.get_table('codigoRFID')]
					if value in codes:
						self.alert['text'] = "Código RFID ya registrado."
						return False
				else:
					code_in_db = self.db.get_table(self.table_name, id=self.id)[0][-1]
					codes = [c[0] for c in self.db.get_table('codigoRFID')]
					if value in codes and value != code_in_db:
						self.alert['text'] = "Código RFID ya registrado."
						return False
			
			if field in ('maxVisitas', 'edadMin', 'edadMax'):
				try:
					int(value)
				except:
					self.alert['text'] = f"{self.field_names[i]} debe ser un número."
					return False
				
			if field == 'maxVisitas':
				if int(value) < 1:
					self.alert['text'] = f"Máximo de visitas inválido."
					return False

			if field == 'fechaNacimiento':
				try:
					datetime.fromisoformat(value)
				except ValueError:
					self.alert['text'] = "Fecha inválida."
					return False
			
			if field == 'horarioInicio' or field == 'horarioFin':
				try:
					datetime.strptime(value, '%H:%M:%S')
				except ValueError:
					self.alert['text'] = "Horario inválido."
					return False
		return True
	
	def confirm_insert(self):
		if not self.data_is_valid():
			return
		
		state = { 'ALTA': 1, 'INTERNADO': 2 }

		#Separar columnas propias y FKs
		fks = []
		own_fields = []
		for col in self.db.get_columns(self.table_name)[1:]:
			if col.startswith('id') and col != 'idEstadoPaciente':
				fks.append(col)
			else:
				own_fields.append(col)
		
		#Aqui tambien se quita el campo de disponible para el insert into 
		if self.table_name == 'habitacion':
			own_fields.pop()

		#Obtener valores para Fks
		fks_dict = {}
		for fk in fks:
			table = fk[2:]
			fields = self.db.get_columns(table)[1:]
			values = [self.entries[f].get() for f in self.entries.keys() if f in fields]
			fks_dict[fk] = self.db.insert_into(table, fields, values)

		#Obtener valores para columnas propias
		values = []
		for f in own_fields:
			if f == 'idEstadoPaciente':
				values.append(state[self.entries['estado'].get()])
				continue
			values.append(self.entries[f].get())

		own_fields.extend(fks_dict.keys())
		values.extend(fks_dict.values())

		last_id = self.db.insert_into(self.table_name, own_fields, values)

		#Añadir la estancia si es que se trata de un paciente
		if 'estado' in self.entries.keys():
			if self.entries['estado'].get() == 'INTERNADO':
				room_id = self.db.get_id('Habitacion', 'nombreHabitacion', self.entries['nombreHabitacion'].get())
				self.db.insert_into_room(last_id, room_id)

		self.close()

	def confirm_update(self):
		if not self.data_is_valid():
			return
		
		state = { 'ALTA': 1, 'INTERNADO': 2 }
		
		#Separar columnas propias y FKs
		fks = []
		own_fields = []
		for col in self.db.get_columns(self.table_name)[1:]:
			if col.startswith('id') and col != 'idEstadoPaciente':
				fks.append(col)
			else:
				own_fields.append(col)

		patient_in_room = self.db.get_id_from_room(self.id)
		if 'estado' in self.entries.keys():
			if self.entries['estado'].get() == 'INTERNADO':
				room_id = self.db.get_id('Habitacion', 'nombreHabitacion', self.entries['nombreHabitacion'].get())
				if patient_in_room != -1:
					self.db.update_from_room(self.id, room_id)
				else:
					self.db.insert_into_room(self.id, room_id)
			else:
				if patient_in_room != -1:
					self.db.delete_from_room(self.id)
		
		#Obtener valores para columnas propias
		if self.table_name == 'habitacion':
			own_fields.pop()
		values = []
		for f in own_fields:
			if f == 'idEstadoPaciente':
				values.append(state[self.entries['estado'].get()])
				continue
			values.append(self.entries[f].get())

		#Actualizar datos propios, si es q los hay
		if len(own_fields) > 0:
			self.db.update(self.table_name, self.id, own_fields, values)

		#Conseguir los IDs de las FKs de las weas a actualizar
		if self.table_name == 'paciente':
			#Este esta hardcoded porque tengo frio, sueño y no hay tiempo de pensar una mejor solucion
			#Solo toma el ID de la tabla datos personales en la posicion 6
			fks_ids = self.db.get_raw_data(self.table_name, self.id)[6:7]
		else:
			#Se le quita el numero de campos propios + 1 para quitar tambien la columna de ID
			fks_ids = self.db.get_raw_data(self.table_name, self.id)[len(own_fields)+1:]

		#Actualizar valores con FKs
		i = 0
		for f in fks:
			#A f le quitamos los primeros 2 chars por el prefijo de 'id', luego de las columnas omitimos el id (lmao nadie qiere al ID)
			table_name = f[2:]
			cols = self.db.get_columns(table_name)[1:]
			values = []
			for c in cols:
				values.append(self.entries[c].get())
			self.db.update(table_name, fks_ids[i], cols, values)
			i += 1
		self.close()

	def close(self):
		if hasattr(self.origin, 'update_table'):
			self.origin.update_table()
		if hasattr(self.origin, 'update_admin_list'):
			self.origin.update_admin_list()

		if self.btn_rfid:
			if self.btn_rfid['text'] == "Esperando...":
				self.switch_rfid_mode()

		self.master.destroy()

class ConfirmationWindow(ttk.Frame):
	def __init__(self, parent, origin, db, n_rows, ids):
		super().__init__(parent)
		self.master.iconbitmap("images/icon_dark.ico")
		self.origin = origin
		self.db = db
		self.ids = ids

		word = "registro" if n_rows == 1 else "registros"

		self.pack(fill='x', expand=True)
		self.master.title(f"Eliminar {word}")

		ttk.Label(self, text=f"Esta acción eliminará {n_rows} {word}.\n¿Desea continuar?", anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
		ttk.Button(self, text="Cancelar", command=self.close, style='Outline.TButton').grid(row=1, column=0, padx=10, pady=10, columnspan=1)
		ttk.Button(self, text="Aceptar", command=self.accept, style='danger.TButton').grid(row=1, column=1, padx=10, pady=10, columnspan=1)

		center_window(self)
	
	def accept(self):
		self.db.delete(self.origin.table_name, self.ids)
		self.origin.update_table()
		self.close()

	def close(self):
		self.master.destroy()

class AnalysisWindow(ttk.Frame):
	def __init__(self, parent, origin):
		super().__init__(parent)
		self.master.iconbitmap("images/icon_dark.ico")
		self.origin = origin
		self.rfid = origin.controller.reader
		self.db = origin.controller.db

		self.rfid.mode = 3
		self.rfid.target_window = self

		self.lb_title = ttk.Label(self, text="Esperando...", font=('Helvetica', 16, 'bold'))
		self.lb_title.pack(padx=60, pady=10)
		
		self.lb_rfid = ttk.Label(self, text="", font=('Helvetica', 12, 'bold'))
		self.lb_rfid.pack(padx=10, pady=10)

		self.lb_info = ttk.Label(self, text="", font=('Helvetica', 12))
		self.lb_info.pack(padx=10, pady=10)

		self.pack(fill='x', expand=True)
		self.master.title(f"Analisis de tarjeta RFID")
		self.btn_ok = ttk.Button(self, width=10, text="Cancelar", command=self.close)
		self.btn_ok.pack(padx=10, pady=10)

		self.grab_set()
		center_window(self)

	def close(self):
		self.rfid.mode = 1
		self.master.destroy()