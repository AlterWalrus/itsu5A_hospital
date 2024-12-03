import ttkbootstrap as ttk
import datetime
from PIL import Image, ImageTk
from data_window import AnalysisWindow
import random

class MainMenu(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
        
		self.img_logo = ImageTk.PhotoImage(Image.open('images/patcheck_logo_small.png'))
		ttk.Label(self, image=self.img_logo).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		
		#Administracion de tablas
		fr = ttk.LabelFrame(self, text='Registros', width=80)
		fr.grid(row=1, column=0, padx=10, pady=1, sticky='nsew')

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
			btn.pack(padx=10, pady=10, expand=True, fill='both')
		
		#Opciones de LectorRFID
		fr = ttk.LabelFrame(self, text='Lector RFID')
		fr.grid(row=2, column=0, padx=10, pady=10, sticky='sew')
		
		self.rfid_state = ttk.Label(fr, text='Desconectado', foreground='#ff5555')
		self.rfid_state.pack(pady=5)

		self.img_reconn = ImageTk.PhotoImage(Image.open('images/re_connect.png'))
		self.btn_rfid_conn = ttk.Button(fr, image=self.img_reconn, compound='left', width=12, text='Re-conectar', command=self.retry_rfid_conn)
		self.btn_rfid_conn.pack(padx=10, pady=5, expand=True, fill='both')

		self.img_analyze = ImageTk.PhotoImage(Image.open('images/analyze.png'))
		ttk.Button(fr, image=self.img_analyze, compound='left', width=12, text='Analizar tarjeta', command=self.analyze_card).pack(padx=10, pady=10, expand=True, fill='both')

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
		fr = ttk.Frame(self)
		fr.grid(row=1, column=1, padx=10, pady=10, sticky='nsew', rowspan=2)

		#Grafica de la semana
		fr_sub = ttk.LabelFrame(fr, text="Actividad últimos siete días")
		fr_sub.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

		self.cnv_week = ttk.Canvas(fr_sub, height=240, width=360)
		self.cnv_week.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
		self.week_data = [random.randint(0, 20) for i in range(7)]
		self.draw_week_stats(360, 240)

		#Grafica de hoy
		fr_sub = ttk.LabelFrame(fr, text="Actividad hoy")
		fr_sub.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

		self.cnv_today = ttk.Canvas(fr_sub, height=240, width=400)
		self.cnv_today.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
		self.today_data = [random.randint(0, i//2) for i in range(datetime.datetime.today().hour+1)]
		print(self.today_data)
		self.draw_today_stats(400, 240)

		#Vistas de habitaciones
		fr_sub = ttk.LabelFrame(fr, text="Visitas en tiempo real")
		fr_sub.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2, rowspan=2)

		self.cnv_rooms = ttk.Canvas(fr_sub, height=180, width=760)
		self.cnv_rooms.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
		self.room_visitors = {}
		rooms_data = self.controller.db.get_table('habitacion')
		for r in rooms_data:
			self.room_visitors[r[0]] = 0
		self.draw_rooms_state(760, 180)

		self.controller.bind('<Configure>', self.resizing)

	def draw_rooms_state(self, w, h):
		self.cnv_rooms.delete(ttk.ALL)
		self.cnv_rooms.config(width=w, height=h)
		margin = 20

		rooms_oc = self.controller.db.get_raw_table('estancia')
		for i in range(len(rooms_oc)):
			patient_data = self.controller.db.get_table('paciente', id=rooms_oc[i][0])[0]
			patient_name = ' '.join(patient_data[5:8])
			room_data = self.controller.db.get_table('habitacion', id=rooms_oc[i][1])[0]

			self.cnv_rooms.create_image(margin, i*32+margin-4, image=self.img_room)
			self.cnv_rooms.create_text(margin+32, i*32+margin, text=room_data[0], fill='white', justify='left', font=('Helvetica', 10, 'bold'))
			self.cnv_rooms.create_text(margin+64, i*32+margin, text=patient_name, fill='white', justify='left', anchor='w')
			self.cnv_rooms.create_text(margin+320, i*32+margin, text=f"{self.room_visitors[room_data[0]]}/{patient_data[0]}", fill='white', justify='left', anchor='w', font=('Helvetica', 10, 'bold'))
		
	def draw_today_stats(self, w, h):
		self.cnv_today.delete(ttk.ALL)
		self.cnv_today.config(width=w, height=h)

		curr_hour = len(self.today_data)
		lnw = round(w*0.04)		#16, la multiplicacion de 400 * 0.04 debe dar 16, eso significan los numeros
		lnh = round(h*0.833)	#200 si, fueron calculados a mano... perdon isra del futuro
		tdy_max = max(max(self.today_data), 1)
		margin = 20

		self.cnv_today.create_line(margin, 20, w, 20, fill='white')
		self.cnv_today.create_line(margin, lnh, w, lnh, fill='white')
		
		self.cnv_today.create_text(14, 20, text=tdy_max, fill='white', justify='left', font=('Helvetica', 8, 'bold'))
		mid_y = (lnh+20)/2
		if tdy_max % 2 != 0:
			mid_y += (lnh/tdy_max)/2
		self.cnv_today.create_text(14, mid_y, text=tdy_max//2, fill='white', justify='left', font=('Helvetica', 8, 'bold'))
		self.cnv_today.create_line(margin, mid_y, w, mid_y, fill='gray')

		for i in range(1, curr_hour):
			y1 = lnh - (self.today_data[i-1]/tdy_max) * (lnh*0.9)
			y2 = lnh - (self.today_data[i]/tdy_max) * (lnh*0.9)
			self.cnv_today.create_line((i-1)*lnw+margin, y1, i*lnw+margin, y2, fill='white', width=3)

		for i in range(24):
			if (i) % 2 == 0:
				self.cnv_today.create_line((i)*lnw+margin, lnh, (i)*lnw+margin, lnh+12, fill='white')
				self.cnv_today.create_text((i)*lnw+margin, lnh+20, text=f"{i}:00", fill='white', justify='center', font=('Helvetica', round(w*0.013)))
			else:
				self.cnv_today.create_line((i)*lnw+margin, lnh, (i)*lnw+margin, lnh+8, fill='gray')
			
	def draw_week_stats(self, w, h,):
		self.cnv_week.delete(ttk.ALL)
		self.cnv_week.config(width=w, height=h)

		max_day = max(max(self.week_data), 1)
		curr_day = datetime.datetime.today().weekday()+1
		days = "LMXJVSDLMXJVSD"
		bar_w = round(w*0.14)	#50
		bar_h = round(h*0.833)	#200

		for i in range(7):
			percent = self.week_data[i] / max_day
			color = '#87d1dc' if i == 6 else 'white'
			self.cnv_week.create_text(i*bar_w+(bar_w*0.4), (bar_h-25)-(percent*(bar_h-40)), text=self.week_data[i], fill=color, font=('Helvetica', 12, 'bold'))
			self.cnv_week.create_rectangle(i*bar_w, bar_h, i*bar_w+(bar_w-8), (bar_h-10)-(percent*(bar_h-40)), fill=color)
			self.cnv_week.create_text(i*bar_w+(bar_w*0.4), bar_h+20, text=days[i+curr_day], fill=color, font=('Helvetica', 12, 'bold'))
	
	def after_resize(self):
		w = self.controller.winfo_width()
		h = self.controller.winfo_height()
		self.draw_week_stats(round(w*0.323), round(h*0.363))
		self.draw_today_stats(round(w*0.359), round(h*0.363))
		self.draw_rooms_state(round(w*0.6822), round(h*0.273))

	def resizing(self, event):
		if event.widget == self.controller:
			if getattr(self, "_after_id", None):
				self.controller.after_cancel(self._after_id)
			self._after_id = self.controller.after(100, self.after_resize)

	def analyze_card(self):
		nw = ttk.Toplevel(self)
		AnalysisWindow(nw, self)

	def back_to_login(self):
		self.controller.show_frame('Login')

	def retry_rfid_conn(self):
		self.controller.reader.connect_reader()

	def switch_btn_rfid_active(self, enabled):
		self.btn_rfid_conn['state'] = ttk.NORMAL if enabled else ttk.DISABLED
