import ttkbootstrap as ttk
from math import ceil

class DataWindow(ttk.Frame):
	def __init__(self, parent, origin, table_name, fields, mode, db, selected=None):
		super().__init__(parent)
		self.origin = origin
		self.db = db
		self.pack(fill='x', expand=True)
		self.table_name = table_name

		if mode == 'add':
			self.master.title("Agregar registro")
		else:
			self.master.title("Editar registro")

		ttk.Label(self, text="Ingrese los datos cuidadosamente.", width=60, anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=4, padx=10, pady=10)

		#Campos a llenar y otras weas
		self.entries = {}
		col = 0
		half = ceil(len(fields)/2)
		i = 0
		for field in fields:
			if i == half:
				i = 0
				col += 2
			lb = ttk.Label(self, text=field, width=10, anchor='e')
			lb.grid(row=i+1, column=col, padx=2, pady=5)

			entry = ttk.Entry(self)
			if field == 'horarioInicio' or field == 'horarioFin':
				entry.insert(0, 'HH:MM:SS')
			if field == 'fechaNacimiento':
				entry.insert(0, 'AAAA-MM-DD')
			
			entry.grid(row=i+1, column=col+1, padx=10, pady=5, sticky='ew')
			self.entries[field] = entry
			i += 1

		self.alert = ttk.Label(self, foreground='#ff5555', font=('Helvetica', 8, 'bold'))
		self.alert.grid(row=half+1, column=0, columnspan=3, padx=10)

		frame = ttk.Frame(self)
		frame.grid(row=half+1, column=3, padx=10, pady=10)
		ttk.Button(frame, text="Cancelar", command=self.close).grid(row=half+1, column=2, padx=10, pady=10, columnspan=1)
		ttk.Button(frame, text="Aceptar", command=self.accept).grid(row=half+1, column=3, padx=10, pady=10, columnspan=1)

		for i in range(4):
			self.grid_columnconfigure(i, weight=1)
		self.grab_set()
		
	def accept(self):
		values = []
		for e in self.entries.values():
			if e.get() == "":
				self.alert['text'] = "ERROR: Campos sin llenar."
				return
			values.append(e.get())

		self.db.insert_into(self.table_name, self.entries.keys(), values)
		self.origin.update_table()
		self.close()

	def close(self):
		self.master.destroy()
