import ttkbootstrap as ttk
from datetime import datetime
from math import ceil

def center_window(w):
	w.master.update_idletasks()
	x_center = w.origin.controller.winfo_x() + (w.origin.controller.winfo_width()//2) - (w.master.winfo_reqwidth()//2)
	y_center = w.origin.controller.winfo_y() + (w.origin.controller.winfo_height()//2) - (w.master.winfo_reqheight()//2)
	w.master.geometry(f"+{x_center}+{y_center}")

class DataWindow(ttk.Frame):
	def __init__(self, parent, origin, db, table_name, fields, mode, curr_values=None):
		super().__init__(parent)
		self.master.iconbitmap("images/icon_dark.ico")
		self.origin = origin
		self.db = db
		self.pack(fill='x', expand=True)
		self.table_name = table_name
		self.fields = fields

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
			lb = ttk.Label(self, text=field, width=10, anchor='e')
			lb.grid(row=i+1, column=col, padx=2, pady=5)

			if field == 'codigoRFID' and self.origin.controller.reader.connected:
				self.btn_rfid = ttk.Button(self, width=10, text='codigoRFID', command=self.switch_rfid_mode, style='Outline.info.TButton')
				self.btn_rfid.grid(row=i+1, column=col, padx=2, pady=5)
			
			entry = ttk.Entry(self)
			if field == 'horarioInicio' or field == 'horarioFin':
				entry.insert(0, 'HH:MM:SS')
			elif field == 'fechaNacimiento':
				entry.insert(0, 'AAAA-MM-DD')
			elif field == 'nombreHabitacion' and table_name == 'paciente':
				entry = ttk.Combobox(self)
				entry['values'] = [h[0] for h in db.get_table('habitacion') if h[1] == 'SI']
				entry['state'] = 'readonly'

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
	
	def switch_rfid_mode(self):
		rfid = self.origin.controller.reader
		if self.btn_rfid['text'] == "Esperando...":
			self.btn_rfid['text'] = "codigoRFID"
			rfid.target_window = None
			rfid.mode = 1
		else:
			self.btn_rfid['text'] = "Esperando..."
			rfid.target_window = self
			rfid.mode = 2
		
	def data_is_valid(self):
		values = [v.get() for v in self.entries.values()]
		for i in range(len(self.fields)):
			if values[i] == "":
				self.alert['text'] = "Todavía hay campos sin llenar."
				return False
			
			if self.fields[i] == 'fechaNacimiento':
				try:
					datetime.fromisoformat(values[i])
				except ValueError:
					self.alert['text'] = "Fecha inválida."
					return False
			
			if self.fields[i] == 'horarioInicio' or self.fields[i] == 'horarioFin':
				try:
					datetime.strptime(values[i], '%H:%M:%S')
				except ValueError:
					self.alert['text'] = "Horario inválido."
					return False
		return True
	
	def confirm_insert(self):
		if not self.data_is_valid():
			return

		#Separar columnas propias y FKs
		fks = []
		own_fields = []
		for col in self.db.get_columns(self.table_name)[1:]:
			if col.startswith('id'):
				fks.append(col)
			else:
				own_fields.append(col)
		
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
			values.append(self.entries[f].get())

		own_fields.extend(fks_dict.keys())
		values.extend(fks_dict.values())

		self.db.insert_into(self.table_name, own_fields, values)
		if hasattr(self.origin, 'update_table'):
			self.origin.update_table()
		self.close()

	def confirm_update(self):
		pass

	def close(self):
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