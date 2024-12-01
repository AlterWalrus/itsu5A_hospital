import ttkbootstrap as ttk
from difflib import get_close_matches
from PIL import Image, ImageTk
from data_window import DataWindow, ConfirmationWindow

class TableViewer(ttk.Frame):
	def __init__(self, parent, controller, frame_name):
		super().__init__(parent)
		self.controller = controller
		self.frame_name = frame_name

		self.grid_columnconfigure(1, weight=1)

		#Diccionario DISPLAY ---> NOMBRE REAL
		db_names = {
			'Médicos': 'medico',
			'Enfermeros': 'enfermero',
			'Visitantes': 'visitante',
			'Pacientes': 'paciente',
			'Visitas': 'visita',
			'Habitaciones': 'habitacion'
		}
		self.table_name = db_names[frame_name]

		db_fields = {
			'nombrePersona': 'Nombre',
			'apellidoPaterno': 'Apellido P.',
			'apellidoMaterno': 'Apellido M.',
			'cedula': 'Cédula',
			'horarioInicio': 'Hor. Entrada',
			'horarioFin': 'Hor. Salida',
			'fechaNacimiento': 'Fecha de Nac.',
			'telefono': 'Teléfono',
			'codigoRFID': 'Código RFID',
			'maxVisitas': 'Max. Visitas',
			'edadMin': 'Edad Min.',
			'edadMax': 'Edad Max.',
			'nombreHabitacion': 'Habitación',
			'estado': 'Estado'
		}

		#Filtrar (exclusivo de visitas!!!)
		if frame_name == 'Visitas':
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
		ttk.Label(fr, text=frame_name, anchor='w', font=('Helvetica', 16, 'bold')).grid(row=0, column=1, padx=10, pady=5, sticky='ew')
		self.lb_nrows = ttk.Label(fr, text="(45 registros)")
		self.lb_nrows.grid(row=0, column=2)

		#Contenedor de acciones
		fr_actions = ttk.LabelFrame(self, text='Acciones')
		fr_actions.grid(row=2, column=0, rowspan=2, padx=10, pady=10, sticky='w')
		fr_actions.grid_columnconfigure(0, weight=1)
		fr_actions.grid_columnconfigure(1, weight=1)
		fr_actions.grid_columnconfigure(2, weight=1)
        
		#Agregar
		if self.table_name != 'visita':
			self.img_add = ImageTk.PhotoImage(Image.open('images/add.png'))
			ttk.Button(fr_actions, image=self.img_add, compound='left', width=12, text='Registrar', command=self.open_add).grid(row=0, column=0, padx=10, pady=5)
        
		#Editar
		self.img_edit = ImageTk.PhotoImage(Image.open('images/edit.png'))
		self.btn_edit = ttk.Button(fr_actions, image=self.img_edit, compound='left', width=12, text='Editar', command=self.open_edit, state='disabled')
		self.btn_edit.grid(row=0, column=1, padx=10, pady=10)
        
		#Eliminar
		self.img_delete = ImageTk.PhotoImage(Image.open('images/delete.png'))
		self.btn_delete = ttk.Button(fr_actions, image=self.img_delete, compound='left', width=12, text='Eliminar', command=self.delete, state='disabled')
		self.btn_delete.grid(row=0, column=2, padx=10, pady=10)
        
		#Buscar
		fr_search = ttk.LabelFrame(self, text='Buscar por')

		self.search_menu = ttk.Menubutton(fr_search, width=12)
		self.search_menu.grid(row=0, column=0, padx=10, pady=5)
		menu = ttk.Menu(self.search_menu)

		options = ('Cualquier dato', 'Nombre completo')
		if frame_name == 'Visitas':
			options = ('Cualquier dato', 'Entrada', 'Salida', 'Visitante', 'Paciente')
		elif frame_name == 'Habitaciones':
			options = ('Cualquier dato',)

		for option in options:
			menu.add_radiobutton(label=option, value=option, command=lambda c=option: self.update_column_search(c))
		self.search_menu.config(menu=menu, text=options[0])

		fr_search.grid(row=2, column=1, rowspan=2, padx=10, pady=10, sticky='e')
        
		self.search_entry = ttk.Entry(fr_search)
		self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
		self.search_entry.bind('<Return>', self.search)

		self.img_search = ImageTk.PhotoImage(Image.open('images/search.png'))
		ttk.Button(fr_search, image=self.img_search, command=self.search).grid(row=0, column=2, padx=10, pady=10)
        
        #Tabla
		if self.table_name == 'visita':
			self.columns = self.controller.db.get_columns('view_visitas')
		elif self.table_name == 'paciente':
			self.columns = self.controller.db.get_columns('view_pacientes')
		else:
			self.columns = self.controller.db.get_table(self.table_name, getcolumns=True)
		
		#Tablas con los nombre humanizados de las columnas
		self.column_names = [db_fields[f] if f in db_fields.keys() else f for f in self.columns]
		
		columns_ID = ['Column' + str(i + 1) for i in range(len(self.columns))]
		self.table = ttk.Treeview(self, columns=columns_ID, show='headings')
		for i in range(len(self.columns)):
			self.table.column(columns_ID[i], width=80)
			col = self.column_names[i]
			self.table.heading(columns_ID[i], text=col)
		self.table.grid(row=1, column=0, columnspan=12, sticky='nsew', padx=10, pady=5)
		self.table.bind('<<TreeviewSelect>>', self.item_selected)

		self.update_table()

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

	def item_selected(self, event):
		selected_elements = len(self.table.selection())
		self.switch_btn_edit_active(selected_elements == 1)
		self.switch_btn_delete_active(selected_elements >= 1)		

	def update_table(self, items=None):
		for i in self.table.get_children():
			self.table.delete(i)
		
		#Si no hay items predefinidos actualizamos la lista de IDs completa (se usa en el filtrado de visitas)
		if not items:
			self.table_ids = self.controller.db.get_ids(self.table_name)
	
		if items:
			rows = items
		elif self.table_name == 'visita':
			rows = self.controller.db.get_raw_table('view_visitas')
		elif self.table_name == 'paciente':
			rows = self.controller.db.get_raw_table('view_pacientes')
		else:
			rows = self.controller.db.get_table(self.table_name)
		self.lb_nrows['text'] = f"({len(rows)} registros)"

		for r in rows:
			r = list(r)
			self.table.insert('', ttk.END, values=r)

	def open_add(self):
		columns = self.columns[:]
		if self.table_name == 'habitacion':
			columns.pop()

		nw = ttk.Toplevel(self)
		DataWindow(nw, self, self.controller.db, self.table_name, columns, self.column_names, 'add')
    
	def open_edit(self):
		curr_values = self.table.item(self.table.selection()[0])['values']
		columns = self.columns[:]
		if self.table_name == 'habitacion':
			columns.pop()

		nw = ttk.Toplevel(self)
		DataWindow(nw, self, self.controller.db, self.table_name, columns, self.column_names, 'edit', curr_values)
    
	def delete(self):
		table_rows = self.table.get_children()
		indexes = [table_rows.index(i) for i in self.table.selection()]
		ids = [self.table_ids[i] for i in indexes]

		nw = ttk.Toplevel(self)
		ConfirmationWindow(nw, self, self.controller.db, len(self.table.selection()), ids)
		
	def search(self, event=None):
		entry = self.search_entry.get()
		table_rows = self.table.get_children()
		indexes = []

		for i in table_rows:
			row = [str(r).lower() for r in self.table.item(i)['values']]
			match = None
			if self.search_menu['text'] == "Cualquier dato":
				match = get_close_matches(entry.lower(), row, n=1)
			elif self.search_menu['text'] == "Entrada":
				match = entry in row[0]

			if match:
				indexes.append(self.table.index(i))
		
		table_indexes = [table_rows[i] for i in indexes]
		self.table.selection_set(table_indexes)

	def update_filter(self, content):
		self.filter_menu['text'] = content
		
		self.update_table()
		rows = []
		all_rows = []
		for i in self.table.get_children():
			item = self.table.item(i)['values']
			all_rows.append(item)

		db_names = { 'Médicos': 'medico', 'Enfermeros': 'enfermero', 'Visitantes': 'visitante' }

		if content == 'Todos':
			rows = all_rows
		else:
			rows = []
			table_ids = []
			for i in range(len(all_rows)):
				#Comparar tipo y la seleccion en el MenuButton
				if all_rows[i][2] == db_names[content]:
					rows.append(all_rows[i])
					table_ids.append(self.table_ids[i])
			self.table_ids = table_ids
		self.update_table(items=rows)
	
	def switch_btn_edit_active(self, enabled):
		self.btn_edit['state'] = ttk.NORMAL if enabled else ttk.DISABLED
	
	def switch_btn_delete_active(self, enabled):
		self.btn_delete['state'] = ttk.NORMAL if enabled else ttk.DISABLED

	def update_column_search(self, col):
		self.search_menu['text'] = col
