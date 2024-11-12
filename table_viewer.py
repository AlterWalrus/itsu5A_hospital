import ttkbootstrap as ttk
from PIL import Image, ImageTk
from data_window import DataWindow
import mysql_conn

class TableViewer(ttk.Frame):
	def __init__(self, parent, controller, table_name):
		super().__init__(parent)
		self.controller = controller
		self.table_name = table_name
		self.selected = None

		self.columnconfigure(1, weight=1)

		#Tabla
		self.db = {
			'Médicos': ['CodigoRFID', 'Cedula', 'HorEntrada', 'HorSalida', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Enfermeros': ['CodigoRFID', 'Licencia', 'HorEntrada', 'HorSalida', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Visitantes': ['CodigoRFID', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Pacientes': ['MaxVisitas', 'Habitacion', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email'],
			'Visitas': ['Entrada', 'Salida', 'Visitante', 'Paciente'],
			'Habitaciones': ['Nombre']
		}

		#Diccionario DISPLAY ---> NOMBRE REAL
		db_names = {
			'Médicos': 'medico',
			'Enfermeros': 'enfermero',
			'Visitantes': 'visitante',
			'Pacientes': 'paciente',
			'Visitas': 'visita',
			'Habitaciones': 'habitacion'
		}
		self.real_table_name = db_names[table_name]

		#Filtrar (exclusivo de visitas!!!)
		if table_name == 'Visitas':
			fltr = ttk.Frame(self)
			fltr.grid(row=0, column=1, sticky='e', padx=10)

			ttk.Label(fltr, text='Mostrar visitas de').grid(row=0, column=0, padx=10, pady=5)

			self.filter_menu = ttk.Menubutton(fltr, width=12, text='Todos')
			self.filter_menu.grid(row=0, column=1, padx=10, pady=5)
			menu = ttk.Menu(self.filter_menu)
			for option in ('Todos', 'Médicos', 'Enfermeros', 'Visitantes'):
				menu.add_radiobutton(label=option, value=option, command=lambda c=option: self.update_filter(c))
			self.filter_menu['menu'] = menu

		#Regresar al menu principal
		fr = ttk.Frame(self)
		fr.grid(row=0, column=0, sticky='w')
        
		self.img_goback = ImageTk.PhotoImage(Image.open('images/go_back.png'))
		ttk.Button(fr, image=self.img_goback, compound='left', width=16, text='Menú anterior', command=lambda f='MainMenu': controller.show_frame(f), style='Outline.TButton').grid(row=0, column=0, padx=10, pady=5, sticky='ns')
		ttk.Label(fr, text=table_name, anchor='w', font=('Helvetica', 16, 'bold')).grid(row=0, column=1, columnspan=8, padx=10, pady=5, sticky='ew')

		#Contenedor de acciones
		fr_actions = ttk.LabelFrame(self, text='Acciones')
		fr_actions.grid(row=2, column=0, rowspan=2, padx=10, pady=10, sticky='w')
		fr_actions.grid_columnconfigure(0, weight=1)
		fr_actions.grid_columnconfigure(1, weight=1)
		fr_actions.grid_columnconfigure(2, weight=1)
        
		#Agregar
		self.img_add = ImageTk.PhotoImage(Image.open('images/add.png'))
		ttk.Button(fr_actions, image=self.img_add, compound='left', width=12, text='Registrar', command=self.open_add).grid(row=0, column=0, padx=10, pady=5)
        
		#Editar, no se puede si selected es None
		self.img_edit = ImageTk.PhotoImage(Image.open('images/edit.png'))
		self.btn_edit = ttk.Button(fr_actions, image=self.img_edit, compound='left', width=12, text='Editar', command=self.open_edit, state='disabled')
		self.btn_edit.grid(row=0, column=1, padx=10, pady=10)
        
		#Eliminar, no se puede si selected es None
		self.img_delete = ImageTk.PhotoImage(Image.open('images/delete.png'))
		self.btn_delete = ttk.Button(fr_actions, image=self.img_delete, compound='left', width=12, text='Eliminar', command=self.delete, state='disabled')
		self.btn_delete.grid(row=0, column=2, padx=10, pady=10)
        
		#Buscar
		fr_search = ttk.LabelFrame(self, text='Buscar por')

		self.search_menu = ttk.Menubutton(fr_search, width=12)
		self.search_menu.grid(row=0, column=0, padx=10, pady=5)
		menu = ttk.Menu(self.search_menu)

		options = ('Nombre', 'Apellido Paterno', 'Apellido Materno')
		if table_name == 'Visitas':
			options = ('Entrada', 'Salida', 'Visitante', 'Paciente')
		elif table_name == 'Habitaciones':
			options = ('Nombre',)

		for option in options:
			menu.add_radiobutton(label=option, value=option, command=lambda c=option: self.update_column_search(c))
		self.search_menu.config(menu=menu, text=options[0])

		fr_search.grid(row=2, column=1, rowspan=2, padx=10, pady=10, sticky='e')
        
		self.search_entry = ttk.Entry(fr_search)
		self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
		self.img_search = ImageTk.PhotoImage(Image.open('images/search.png'))
		ttk.Button(fr_search, image=self.img_search, command=self.search).grid(row=0, column=2, padx=10, pady=10)
        
        #Tabla
		self.columns = self.controller.db.get_table(self.real_table_name, getcolumns=True)
		columns_ID = ['Column' + str(i + 1) for i in range(len(self.columns))]
        
		self.table = ttk.Treeview(self, columns=columns_ID, show='headings')
		for i in range(len(self.columns)):
			self.table.column(columns_ID[i], width=70)
			self.table.heading(columns_ID[i], text=self.columns[i])
		self.table.grid(row=1, column=0, columnspan=12, sticky='nsew', padx=10, pady=5)

		self.update_table()

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

	def update_table(self):
		for i in self.table.get_children():
			self.table.delete(i)
		
		rows = self.controller.db.get_table(self.real_table_name)
		for r in rows:
			r = list(r)
			self.table.insert('', ttk.END, values=r)

	def open_add(self):
		nw = ttk.Toplevel(self)
		DataWindow(nw, self, self.real_table_name, self.columns, 'add', self.controller.db)
    
	def open_edit(self):
		nw = ttk.Toplevel(self)
		DataWindow(nw, self, self.real_table_name, self.columns, 'edit', self.controller.db, self.selected)
    
	def delete(self):
		print("delete lmao")
    
	def search(self):
		pass

	def switch_btn_edit_active(self, enabled):
		self.btn_edit['state'] = ttk.NORMAL if enabled else ttk.DISABLED
	
	def switch_btn_delete_active(self, enabled):
		self.btn_delete['state'] = ttk.NORMAL if enabled else ttk.DISABLED

	def update_filter(self, content):
		self.filter_menu['text'] = content

	def update_column_search(self, col):
		self.search_menu['text'] = col
