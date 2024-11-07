import ttkbootstrap as ttk
import tkinter.scrolledtext as st
from datetime import date
from rfid_reader import RFID_Reader

class MainMenu(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
        
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
        
		ttk.Label(self, text='SecureRoom', font=('Helvetica', 20, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
		#Log o historial, como quieras llamarle
		self.log = st.ScrolledText(self)

		self.log.tag_configure('normal', font=('Consolas', 10))
		self.log.tag_configure('error', font=('Consolas', 10), foreground='#ff0000')
		self.log.tag_configure('ok', font=('Consolas', 10), foreground='#00ff00')

		self.log.grid(row=1, column=1, rowspan=8, columnspan=1, padx=10, pady=10, sticky='nsew')
		self.log.insert(ttk.INSERT, "Te damos la bienvenida al sistema de administración SecureRoom (nombre provisional).\n", 'normal')
		self.log.insert(ttk.INSERT, f"Fecha: {date.today()}.\n", 'normal')
		self.log.configure(state='disabled')
		
		#Administracion de tablas
		fr = ttk.LabelFrame(self, text='Registros', width=80)
		fr.grid(row=1, column=0, padx=10, pady=1, sticky='n')

		buttons = ['Médicos', 'Enfermeros', 'Visitantes', 'Pacientes', 'Visitas']
		for i, button_text in enumerate(buttons):
			btn = ttk.Button(fr, width=12, text=button_text, command=lambda t=button_text: controller.show_frame(t))
			#btn.grid(row=i, column=0, padx=10, pady=10, sticky='ew')
			btn.pack(padx=10, pady=10)
		
		#Otras opciones
		fr = ttk.LabelFrame(self, text='Otras opciones')
		fr.grid(row=2, column=0, padx=10, pady=10, sticky='n')

		self.btn_rfid_conn = ttk.Button(fr, width=12, text='Re-conectar', command=self.retry_rfid_conn)
		self.btn_rfid_conn.pack(padx=10, pady=10)
		ttk.Button(fr, width=12, text='Limpiar Log', command=self.log_clear).pack(padx=10, pady=10)
		ttk.Button(fr, width=12, text='Exportar Log', command=self.log_export).pack(padx=10, pady=10)

		#Opciones para administradores
		fr = ttk.LabelFrame(self, text='Administración')
		fr.grid(row=1, column=2, padx=10, pady=10, sticky='n')

		ttk.Label(fr, text="Sesión de").pack(padx=10)
		self.admin_curr = ttk.Label(fr, text="Isra", font=('Helvetica', 12, 'bold'))
		self.admin_curr.pack(padx=10)

		ttk.Button(fr, width=12, text='Bloquear App', command=self.back_to_login).pack(padx=10, pady=10)
		ttk.Button(fr, width=12, text='Agregar Admin.').pack(padx=10, pady=10)
		ttk.Button(fr, width=12, text='Editar Admin.').pack(padx=10, pady=10)
		ttk.Button(fr, width=12, text='Eliminar Admin.').pack(padx=10, pady=10)
		
		#Conexion con el arduino
		self.reader = RFID_Reader(self)

	def back_to_login(self):
		self.controller.show_frame('Login')

	def retry_rfid_conn(self):
		self.reader.connect_arduino()

	def switch_rfid_btn_active(self, enabled):
		self.btn_rfid_conn['state'] = ttk.NORMAL if enabled else ttk.DISABLED

	def log_print(self, msg, tag='normal'):
		self.log.configure(state='normal')
		#self.log.mark_set('insert', "999.0") fix this shit bro
		self.log.insert(ttk.INSERT, msg, tag)
		self.log.configure(state='disabled')
	
	def log_clear(self):
		self.log.configure(state='normal')
		self.log.delete('1.0', ttk.END)
		self.log.configure(state='disabled')

	def log_export(self):
		try:
			with open(f'logs/SRlog{date.today()}.txt', 'w', encoding='utf-8') as file:
				file.write(self.log.get('1.0', ttk.END))
				self.log_print("Exportado correctamente.\n", 'ok')
		except FileNotFoundError as e:
			self.log_print("Error al exportar.\n", 'error')
			self.log_print(f"Error: {e}\n", 'error')
