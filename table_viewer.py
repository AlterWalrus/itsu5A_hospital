import ttkbootstrap as ttk
from data_window import DataWindow

class TableViewer(ttk.Frame):
	def __init__(self, parent, controller, table_name):
		super().__init__(parent)

		self.table_name = table_name
		self.selected = None

		#Tabla
		self.db = {
			'Médicos': ['CodigoRFID', 'Cedula', 'HorEntrada', 'HorSalida', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Enfermeros': ['CodigoRFID', 'Licencia', 'HorEntrada', 'HorSalida', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Visitantes': ['CodigoRFID', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Pacientes': ['CodigoHEX', 'MaxVisitas', 'Habitacion', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Visitas': ['Entrada', 'Salida', 'Visitante', 'Paciente']
		}
		
		self.corner_frame = ttk.Frame(self)
		self.corner_frame.grid(row=0, column=0, sticky='w')
  
        #Regresar al menu principal
		ttk.Button(self.corner_frame, width=16, text='Menú anterior', command=lambda: controller.back_to_main(), style='Outline.TButton').grid(row=0, column=0, padx=10, pady=10)
		ttk.Label(self.corner_frame, text=table_name, anchor='w', font=('Helvetica', 16, 'bold')).grid(row=0, column=1, columnspan=8, padx=10, pady=1, sticky='ew')

		#Contenedor de acciones
		fr_actions = ttk.LabelFrame(self, text='Acciones')
		fr_actions.grid(row=2, column=0, rowspan=2, padx=10, pady=10, sticky='w')
		fr_actions.grid_columnconfigure(0, weight=1)
		fr_actions.grid_columnconfigure(1, weight=1)
        
		#Agregar
		ttk.Button(fr_actions, width=12, text='Registrar', command=self.open_add).grid(row=0, column=0, padx=10, pady=5)
        
		#Editar, no se puede si selected es None
		self.btn_edit = ttk.Button(fr_actions, width=12, text='Editar', command=self.open_edit, state='disabled')
		self.btn_edit.grid(row=0, column=1, padx=10, pady=10)
        
		#Eliminar, no se puede si selected es None
		self.btn_delete = ttk.Button(fr_actions, width=12, text='Eliminar', command=self.delete, state='disabled')
		self.btn_delete.grid(row=0, column=2, padx=10, pady=10)
        
		#Buscar
		fr_search = ttk.LabelFrame(self, text='Buscar por')

		self.search_menu = ttk.Menubutton(fr_search, width=12)
		self.search_menu.grid(row=0, column=0, padx=10, pady=5)
		menu = ttk.Menu(self.search_menu)
		for option in self.db[table_name]:
			menu.add_radiobutton(label=option, value=option, command=lambda c=option: self.update_column_search(c))
		self.search_menu.config(menu=menu, text=self.db[table_name][0])

		fr_search.grid(row=2, column=1, rowspan=2, padx=10, pady=10, sticky='w')
		fr_search.grid_columnconfigure(0, weight=1)
		fr_search.grid_columnconfigure(1, weight=1)
        
		self.search_entry = ttk.Entry(fr_search)
		self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
		ttk.Button(fr_search, text='Buscar', command=self.search).grid(row=0, column=2, padx=10, pady=10)
        

        #Tabla
		#columns = ['CodigoRFID', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email']
		columns = self.db[table_name]
		columns_ID = ['Column' + str(i + 1) for i in range(len(columns))]
        
		self.tree = ttk.Treeview(self, columns=columns_ID, show='headings')
		for i in range(len(columns)):
			self.tree.column(columns_ID[i], width=70)
			self.tree.heading(columns_ID[i], text=columns[i])
		self.tree.grid(row=1, column=0, columnspan=12, sticky='nsew', padx=10, pady=5)
        
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)
    
	def update_column_search(self, col):
		self.search_menu['text'] = col

	def open_add(self):
		nw = ttk.Toplevel(self)
		DataWindow(nw, self.table_name, self.db[self.table_name], 'add')
    
	def open_edit(self):
		nw = ttk.Toplevel(self)
		DataWindow(nw, self.table_name, self.db[self.table_name], 'edit', self.selected)
    
	def delete(self):
		pass
    
	def search(self):
		pass
