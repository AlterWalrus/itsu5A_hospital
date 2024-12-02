import ttkbootstrap as ttk
import threading
from data_window import DataWindow, ConfirmationWindow
from PIL import Image, ImageTk

class Login(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
		self.table_name = 'Admin'

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)

		ttk.Frame(self).pack(expand=True)
		frame = ttk.Frame(self)
        
		self.img_logo = ImageTk.PhotoImage(Image.open('images/patcheck_logo.png'))
		ttk.Label(frame, image=self.img_logo).pack()

		#Barra de carga (solo se ve bonita, pero no hace un carajo)
		self.bar = ttk.Progressbar(frame, style='Striped.TProgressbar', length=0, maximum=100)
		self.bar.pack(pady=10)

		self.admin_pswd = {}
		
		#Seccion para la contraseña
		fr = ttk.LabelFrame(frame, text="Ingresar como administrador")
		fr.pack()

		ttk.Label(fr, text='Usuario').pack(pady=5)

		self.btn_admin_selection = ttk.Menubutton(fr, width=20, style='info.Outline.TMenubutton')
		self.btn_admin_selection.pack(pady=1)

		#Cargar admins
		self.update_admin_list()

		ttk.Label(fr, text='Contraseña').pack(pady=5)

		self.entry_pswd = ttk.Entry(fr, width=25, show='*')
		self.entry_pswd.pack(pady=1, padx=40)
		self.entry_pswd.bind('<Return>', self.validate)

		#Mensaje de ta bien/ta mal
		self.alert = ttk.Label(fr, foreground='#ff5555', font=('Helvetica', 10))
		self.alert.pack()

		ttk.Button(fr, width=12, text='Entrar', command=self.validate).pack(pady=20)

		frame.pack(anchor='center')
		ttk.Frame(self).pack(expand=True)
	
	def update_admin_list(self):
		admin_table = self.controller.db.get_table('admin')
		for i in admin_table:
			self.admin_pswd[i[0]] = i[1]
		
		menu = ttk.Menu(self.btn_admin_selection)
		for admin in self.admin_pswd:
			menu.add_radiobutton(label=admin, value=admin, command=lambda c=admin: self.update_admin_btn(c))
		self.btn_admin_selection.config(menu=menu, text=list(self.admin_pswd)[0])
	
	def admin_add(self):
		nw = ttk.Toplevel(self)
		DataWindow(nw, self, self.controller.db, 'Admin', ('nombreAdmin', 'contrasenia'), ('Nombre', 'Contraseña'), 'add')
	
	def admin_edit(self):
		admin = self.btn_admin_selection['text']
		pswd = self.admin_pswd[self.btn_admin_selection['text']]
		nw = ttk.Toplevel(self)
		DataWindow(nw, self, self.controller.db, 'Admin', ('nombreAdmin', 'contrasenia'), ('Nombre', 'Contraseña'), 'edit', (admin, pswd))
	
	def admin_delete(self):
		id = self.controller.db.get_id('admin', 'nombre', self.btn_admin_selection['text'])
		nw = ttk.Toplevel(self)
		ConfirmationWindow(nw, self, self.controller.db, 1, (id,))

	def update_admin_btn(self, a):
		self.btn_admin_selection['text'] = a

	def validate(self, event=None):
		tried_pswd = self.entry_pswd.get()
		pswd = self.admin_pswd[self.btn_admin_selection['text']]

		if tried_pswd == pswd:
			self.alert.config(text="Datos verificados", foreground='#00ff00')

			#Actualiza la etiqueta de la sesion actual en el menu principal (no crei que funcionaria lmao)
			self.controller.frames['MainMenu'].admin_curr['text'] = self.btn_admin_selection['text']
			
			#Animacion bonita wuuu
			self.bar['length'] = 400
			self.pbar_animation = threading.Thread(target=self.fill_bar, daemon=True)
			self.pbar_animation.start()
		else:
			self.alert['text'] = "Contraseña incorrecta"
			self.alert['foreground'] = 'red'
		self.entry_pswd.delete(0, ttk.END)

	def reset(self):
		self.bar['length'] = 0
		self.bar['value'] = 0
		self.alert['text'] = ""

	def fill_bar(self):
		if self.bar['value'] < 100:
			self.bar['value'] += 2
			self.after(10, self.fill_bar)
		else:
			self.after(500, lambda f='MainMenu': self.controller.show_frame(f))
			self.after(1000, self.reset)