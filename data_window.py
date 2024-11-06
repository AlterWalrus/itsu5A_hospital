import ttkbootstrap as ttk
from tktimepicker import SpinTimePickerOld
from math import ceil

class DataWindow(ttk.Frame):
	def __init__(self, parent, table_name, fields, mode, selected=None):
		super().__init__(parent)
		self.pack(fill='x', expand=True)
		self.table_name = table_name

		if mode == 'add':
			self.master.title('Agregar registro')
		else:
			self.master.title('Editar registro')

		ttk.Label(self, text="Ingrese los datos cuidadosamente.", width=60, anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)

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

			if field == 'HorEntrada' or field == 'HorSalida':
				entry = SpinTimePickerOld(self)
				print("clock set in dude")
			if field == 'Fecha Nac.':
				entry = ttk.DateEntry(self)
			else:
				entry = ttk.Entry(self)
			entry.grid(row=i+1, column=col+1, padx=10, pady=5, sticky='ew')
			self.entries[field] = entry
			i += 1
		
		SpinTimePickerOld(self).grid(row=half+1)

		frame = ttk.Frame(self)
		frame.grid(row=half+1, column=3, padx=10, pady=10)
		ttk.Button(frame, text="Cancelar", command=self.close).grid(row=half+1, column=2, padx=10, pady=10, columnspan=1)
		ttk.Button(frame, text="Aceptar").grid(row=half+1, column=3, padx=10, pady=10, columnspan=1)

		for i in range(4):
			self.grid_columnconfigure(i, weight=1)
		self.grab_set()

	def close(self):
		self.master.destroy()
