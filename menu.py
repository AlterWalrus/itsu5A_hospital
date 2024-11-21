import ttkbootstrap as ttk
import datetime
from PIL import Image, ImageTk
from data_window import AnalysisWindow
from room import Room

class MainMenu(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
        
		self.img_logo = ImageTk.PhotoImage(Image.open('images/patcheck_logo_small.png'))
		ttk.Label(self, image=self.img_logo).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
		
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
		ttk.Button(fr, image=self.img_analyze, compound='left', width=12, text='Analizar tarjeta', command=self.analyze_card).pack(padx=10, pady=10)

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
		fr = ttk.Frame(self)
		fr.grid(row=1, column=1, padx=10, pady=10, sticky='nsew', rowspan=2)

		fr_sub = ttk.LabelFrame(fr, text="Visitas esta semana")
		fr_sub.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

		self.cnv_week = ttk.Canvas(fr_sub, height=200, width=280)
		self.cnv_week.grid(row=0, column=0, padx=10, pady=10)
		week_data = [12, 32, 42, 13, 11, 14, 23]
		self.draw_week_stats(self.cnv_week, week_data)

		fr_sub = ttk.LabelFrame(fr, text="Visitas en tiempo real")
		fr_sub.grid(row=0, column=1, padx=10, pady=10, sticky='nsew', rowspan=2)

		room_names = [i[0] for i in controller.db.get_table('habitacion')]
		patient_data = controller.db.get_table('paciente')
		self.rooms = {}
		self.room_rows = {}
		for rn in room_names:
			self.rooms[rn] = Room()
			self.room_rows[rn] = ttk.Label(fr_sub, image=self.img_room, compound='left', anchor='w', text="")
			self.room_rows[rn].pack(padx=10, pady=2, expand=True, fill='x')

		for pd in patient_data:
			room = pd[10]
			self.rooms[room].put_patient(pd)
		self.update_room_visits()

	def update_room_visits(self):
		room_names = [i[0] for i in self.controller.db.get_table('habitacion')]
		for rn in room_names:
			if self.rooms[rn].occupied:
				r: Room = self.rooms[rn]
				self.room_rows[rn]['text'] = f"{rn} - {r.fname} {r.lname}\t\t{r.get_visitor_number()}/{r.max_visitors}"
			else:
				self.room_rows[rn]['text'] = f"{rn} - No ocupada"
		
	def draw_week_stats(self, cnv_week, week_data):
		max_day = max(week_data)
		days = "LMXJVSD"
		cnv_week.delete(ttk.ALL)
		for i in range(7):
			pc = week_data[i] / max_day
			color = '#87d1dc' if i == datetime.datetime.today().weekday() else 'white'
			cnv_week.create_rectangle(i*40, 160, i*40+32, 150-(pc*120), fill=color)
			cnv_week.create_text(i*40+16, 180, text=days[i], fill=color)
			cnv_week.create_text(i*40+16, 140-(pc*120), text=week_data[i], fill=color)

	def analyze_card(self):
		nw = ttk.Toplevel(self)
		AnalysisWindow(nw, self)

	def back_to_login(self):
		self.controller.show_frame('Login')

	def retry_rfid_conn(self):
		self.controller.reader.connect_reader()

	def switch_btn_rfid_active(self, enabled):
		self.btn_rfid_conn['state'] = ttk.NORMAL if enabled else ttk.DISABLED
