import ttkbootstrap as ttk
from table_viewer import TableViewer
from menu import MainMenu
from login import Login

from mysql_conn import MySQL_Conn

class tkinterApp(ttk.Window):
	def __init__(self, *args, **kwargs): 
		ttk.Window.__init__(self, 'SecureRoom', 'superhero', *args, **kwargs)
		container = ttk.Frame(self)
		container.pack(side='top', fill='both', expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		self.db = MySQL_Conn()

		self.frames['Login'] = Login(container, self)
		self.frames['Login'].grid(row=0, column=0, sticky='nsew')
		self.frames['MainMenu'] = MainMenu(container, self)
		self.frames['MainMenu'].grid(row=0, column=0, sticky='nsew')

		self.tables = ['Visitas', 'Médicos', 'Enfermeros', 'Visitantes', 'Pacientes', 'Habitaciones']
		for t in self.tables:
			self.frames[t] = TableViewer(container, self, table_name=t)
			self.frames[t].grid(row=0, column=0, sticky='nsew')

		#self.show_frame('Login')
		self.show_frame('MainMenu')
        
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

app = tkinterApp()
app.mainloop()