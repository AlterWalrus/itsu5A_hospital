import ttkbootstrap as ttk
import tkinter.scrolledtext as st
from PIL import ImageTk, Image
from table_viewer import TableViewer
from datetime import date

import serial
import threading

class tkinterApp(ttk.Window):
	def __init__(self, *args, **kwargs): 
		ttk.Window.__init__(self, 'SecureRoom', 'superhero', *args, **kwargs)
        
		container = ttk.Frame(self) 
		container.pack(side='top', fill='both', expand=True) 

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		self.frames['MainMenu'] = MainMenu(container, self)
		self.frames['MainMenu'].grid(row=0, column=0, sticky='nsew')

		self.tables = ['Médicos', 'Enfermeros', 'Visitantes', 'Pacientes', 'Visitas']
		for t in self.tables:
			self.frames[t] = TableViewer(container, self, table_name=t)
			self.frames[t].grid(row=0, column=0, sticky='nsew')

		self.show_frame('MainMenu')
        
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
	
	def back_to_main(self):
		self.show_frame('MainMenu')

class MainMenu(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
        
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
        
		ttk.Label(self, text='SecureRoom', font=('Helvetica', 20, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
		#Log
		self.log = st.ScrolledText(self)

		self.log.tag_configure('normal', font=('Consolas', 10))
		self.log.tag_configure('error', font=('Consolas', 10), foreground='#ff0000')
		self.log.tag_configure('ok', font=('Consolas', 10), foreground='#00ff00')

		self.log.grid(row=1, column=1, rowspan=8, columnspan=8, padx=10, pady=10, sticky='nsew')
		self.log.insert(ttk.INSERT, "Bienvenido al sistema de administración SecureRoom.\n", 'normal')
		self.log.insert(ttk.INSERT, f"Sesión del {date.today()}.\n", 'normal')
		self.log.configure(state='disabled')
		
		#Administracion de tablas
		fr = ttk.LabelFrame(self, text='Administrar')
		fr.grid(row=1, column=0, padx=10, pady=1, sticky='n')
		buttons = ['Médicos', 'Enfermeros', 'Visitantes', 'Pacientes', 'Visitas']
		for i, button_text in enumerate(buttons):
			btn = ttk.Button(fr, text=button_text, command=lambda t=button_text: controller.show_frame(t))
			btn.grid(row=i, column=0, padx=10, pady=10, sticky='ew')
		
		#Opciones del log
		fr = ttk.LabelFrame(self, text='Otras opciones')
		fr.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
		ttk.Button(fr, text='Limpiar Log', command=self.log_clear).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
		ttk.Button(fr, text='Exportar Log', command=self.log_export).grid(row=1, column=0, padx=10, pady=10, sticky='ew')

		#Recibir info del arduino
		self.arduino = None
		self.connect_arduino()
	
	def connect_arduino(self):
		try:
			self.arduino = serial.Serial('COM6', 9600)
			self.log_print("Conexion establecida correctamente.\n", 'ok')
			thread = threading.Thread(target=self.read_from_arduino, daemon=True)
			thread.start()
		except serial.SerialException as e:
			self.log_print(f"No se pudo conectar con el lector RFID.\n", 'error')
			self.log_print(f"Error: {e}\n", 'error')

	def log_print(self, msg, tag='normal'):
		self.log.configure(state='normal')
		self.log.insert(ttk.INSERT, msg, tag)
		self.log.configure(state='disabled')
	
	def log_clear(self):
		self.log.configure(state='normal')
		self.log.delete('1.0', ttk.END)
		self.log.configure(state='disabled')

	def log_export(self):
		try:
			with open(f'logs/SRlog{date.today()}.txt', 'w') as file:
				file.write(self.log.get('1.0', ttk.END))
				self.log_print("Exportado correctamente.", 'ok')
		except FileNotFoundError as e:
			self.log_print("Error al exportar.\n", 'error')
			self.log_print(f"Error: {e}\n", 'error')

	def read_from_arduino(self):
		try:
			while True:
				data = self.arduino.readline().decode('utf-8')
				if data:
					self.log_print(data)
		except serial.SerialException as e:
			self.log_print(f"Desconexion con el lector RFID.\n", 'error')
			self.log_print(f"Error: {e}\n", 'error')

#Driver Code
app = tkinterApp()
app.mainloop()