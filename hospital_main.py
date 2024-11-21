import ttkbootstrap as ttk
from table_viewer import TableViewer
from menu import MainMenu
from login import Login
from mysql_conn import MySQL_Conn
from rfid_reader import RFID_Reader

class tkinterApp(ttk.Window):
	def __init__(self, *args, **kwargs): 
		ttk.Window.__init__(self, 'PatCheck', 'superhero', *args, **kwargs)
		self.iconbitmap("images/icon_dark.ico")
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
			self.frames[t] = TableViewer(container, self, frame_name=t)
			self.frames[t].grid(row=0, column=0, sticky='nsew')

		self.reader = RFID_Reader(self)

		#self.show_frame('Login')
		self.show_frame('MainMenu')
        
	def show_frame(self, cont):
		self.reader.update_valid_codes()
		frame = self.frames[cont]
		if hasattr(frame, 'update_table'):
			frame.update_table()
		frame.tkraise()

app = tkinterApp()
app.mainloop()