import ttkbootstrap as ttk
from PIL import Image, ImageTk
from rfid_reader import RFID_Reader

class MainMenu(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
        
		ttk.Label(self, text='SecureRoom', font=('Helvetica', 20, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
		
		#Administracion de tablas
		fr = ttk.LabelFrame(self, text='Registros', width=80)
		fr.grid(row=1, column=0, padx=10, pady=1, sticky='n')

		self.img_person = ImageTk.PhotoImage(Image.open('images/person_wfile.png'))
		self.img_visits = ImageTk.PhotoImage(Image.open('images/visits.png'))
		self.img_room = ImageTk.PhotoImage(Image.open('images/room.png'))
		for button_text in ('Visitas', 'Médicos', 'Enfermeros', 'Visitantes', 'Pacientes', 'Habitaciones'):
			img = self.img_person
			if button_text == 'Visitas':
				img = self.img_visits
			elif button_text == 'Habitaciones':
				img = self.img_room
			btn = ttk.Button(fr, image=img, compound='left', width=12, text=button_text, command=lambda t=button_text: controller.show_frame(t))
			btn.pack(padx=10, pady=10)
		
		#Opciones de LectorRFID
		fr = ttk.LabelFrame(self, text='Lector RFID')
		fr.grid(row=2, column=0, padx=10, pady=10, sticky='s')
		
		self.rfid_state = ttk.Label(fr, text='Desconectado', foreground='#ff5555')
		self.rfid_state.pack(pady=5)

		self.img_reconn = ImageTk.PhotoImage(Image.open('images/re_connect.png'))
		self.btn_rfid_conn = ttk.Button(fr, image=self.img_reconn, compound='left', width=12, text='Re-conectar', command=self.retry_rfid_conn)
		self.btn_rfid_conn.pack(padx=10, pady=5)

		self.img_analyze = ImageTk.PhotoImage(Image.open('images/analyze.png'))
		ttk.Button(fr, image=self.img_analyze, compound='left', width=12, text='Analizar Tarjeta').pack(padx=10, pady=10)

		#Opciones para administradores
		fr = ttk.Frame(self)
		fr.grid(row=0, column=1, padx=10, pady=10, sticky='e')

		ttk.Label(fr, text="Admin", anchor='s').pack(side='left')
		self.admin_curr = ttk.Label(fr, text="Isra", anchor='s', font=('Helvetica', 12, 'bold'))
		self.admin_curr.pack(padx=5, side='left')

		self.img_admin = ImageTk.PhotoImage(Image.open('images/admin_settings.png'))
		self.img_admin_add = ImageTk.PhotoImage(Image.open('images/add.png'))
		self.img_admin_edt = ImageTk.PhotoImage(Image.open('images/edit.png'))
		self.img_admin_del = ImageTk.PhotoImage(Image.open('images/delete.png'))
		self.img_admin_cls = ImageTk.PhotoImage(Image.open('images/exit_admin.png'))
		self.btn_session = ttk.Menubutton(fr, image=self.img_admin, compound='left', text='Opciones', style='Outline.TMenuButton')
		self.btn_session.pack(padx=10, pady=5, side='right')
		menu = ttk.Menu(self.btn_session)
		for option in ('Agregar Admin', 'Editar Admin', 'Eliminar Admin', 'Cerrar Sesión'):
			match option:
				case 'Agregar Admin':
					img = self.img_admin_add
					comm = self.controller.frames['Login'].admin_add
				case 'Editar Admin':
					img = self.img_admin_edt
					comm = self.controller.frames['Login'].admin_edit
				case 'Eliminar Admin':
					img = self.img_admin_del
					comm = self.controller.frames['Login'].admin_delete
				case 'Cerrar Sesión':
					img = self.img_admin_cls
					comm = lambda f='Login': self.controller.show_frame(f)
			menu.add_command(image=img, compound='left', label=option, command=comm)
		self.btn_session['menu'] = menu

		#Panel de informacion general
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		fr = ttk.LabelFrame(self, text="Información General")
		fr.grid(row=1, column=1, padx=10, pady=10, sticky='nsew', rowspan=2)

		ttk.Label(fr, text="Total de visitas hoy").grid(row=1, column=0, padx=10, pady=2)
		self.stat_visits_today = ttk.Label(fr, text=0, font=('Helvetica', 12, 'bold'))
		self.stat_visits_today.grid(row=2, column=0, padx=10, pady=2)

		ttk.Label(fr, text="Total de visitas este mes").grid(row=1, column=1, padx=10, pady=2)
		self.stat_visits_tweek = ttk.Label(fr, text=0, font=('Helvetica', 12, 'bold'))
		self.stat_visits_tweek.grid(row=2, column=1, padx=10, pady=2)

		ttk.Label(fr, text="Total de visitas este año").grid(row=1, column=2, padx=10, pady=2)
		self.stat_visits_tyear = ttk.Label(fr, text=0, font=('Helvetica', 12, 'bold'))
		self.stat_visits_tyear.grid(row=2, column=2, padx=10, pady=2)

		#Conexion con el arduino
		self.reader = RFID_Reader(self)

	def back_to_login(self):
		self.controller.show_frame('Login')

	def retry_rfid_conn(self):
		self.reader.connect_arduino()

	def switch_btn_rfid_active(self, enabled):
		self.btn_rfid_conn['state'] = ttk.NORMAL if enabled else ttk.DISABLED
