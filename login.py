import ttkbootstrap as ttk
import threading

class Login(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)

		ttk.Frame(self).pack(expand=True)
		frame = ttk.Frame(self)
        
		ttk.Label(frame, text='SecureRoom', font=('Helvetica', 32, 'bold')).pack()
		ttk.Label(frame, text="Escriba la contraseña para ingresar como administrador.", font=('Helvetica', 12)).pack(pady=20)
		self.entry_pswd = ttk.Entry(frame, width=20, show='*')
		self.entry_pswd.pack()

		self.entry_pswd.bind('<Return>', self.validate)

		self.alert = ttk.Label(frame, foreground='red', font=('Helvetica', 10))
		self.alert.pack()

		self.bar = ttk.Progressbar(frame, style='Striped.TProgressbar', length=0, maximum=100)
		self.bar.pack(pady=2)

		ttk.Button(frame, width=12, text='Entrar', command=self.validate).pack(pady=10)

		frame.pack(anchor='center')
		ttk.Frame(self).pack(expand=True)

	def validate(self, event=None):
		pswd = self.entry_pswd.get()
		if pswd == '1234':
			self.alert.config(text="Bienvenid@", foreground='#00ff00')
			self.bar['length'] = 400
			self.thread = threading.Thread(target=self.fill_bar, daemon=True)
			self.thread.start()
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
			self.after(500, self.controller.back_to_main)
			self.after(1000, self.reset)
