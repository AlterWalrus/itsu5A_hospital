import ttkbootstrap as ttk

class LogIn(ttk.Frame):
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
		self.alert = ttk.Label(frame, foreground='red', font=('Helvetica', 10))
		self.alert.pack()
		ttk.Button(frame, width=12, text='Entrar', command=self.validate).pack(pady=10)

		frame.pack(anchor='center')
		ttk.Frame(self).pack(expand=True)

	def validate(self):
		pswd = self.entry_pswd.get()
		if pswd == '1234':
			self.alert.config(text="Bienvenid@", foreground='green')
			self.after(1000, self.controller.back_to_main)
		else:
			self.alert['text'] = "Contreaseña incorrecta"
