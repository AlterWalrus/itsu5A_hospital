import ttkbootstrap as ttk

class TableViewer(ttk.Frame):
    def __init__(self, parent, controller, table_name):
        super().__init__(parent)
        self.selected = None
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        ttk.Label(self, text=table_name, font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=8, padx=10, pady=1, sticky='ew')
        
        #Contenedor de acciones
        fr_actions = ttk.LabelFrame(self, text='Acciones')
        fr_actions.grid(row=2, column=0, rowspan=2, padx=10, pady=10, sticky='w')
        fr_actions.grid_columnconfigure(0, weight=1)
        fr_actions.grid_columnconfigure(1, weight=1)
        
        #Agregar
        ttk.Button(fr_actions, width=10, text='Registrar', command=self.open_add).grid(row=0, column=0, padx=10, pady=5)
        
        #Editar, no se puede si selected es None
        self.btn_edit = ttk.Button(fr_actions, width=10, text='Editar', command=self.open_edit, state='disabled')
        self.btn_edit.grid(row=0, column=1, padx=10, pady=10)
        
        #Volver al menu principal
        ttk.Button(fr_actions, width=10, text='Volver', command=lambda: controller.back_to_main()).grid(row=1, column=0, padx=10, pady=10)
        
        #Borrar, no se puede si selected es None
        self.btn_delete = ttk.Button(fr_actions, width=10, text='Borrar', command=self.delete, state='disabled')
        self.btn_delete.grid(row=1, column=1, padx=10, pady=10)
        
        #Buscar
        fr_search = ttk.LabelFrame(self, text='Buscar')
        fr_search.grid(row=2, column=1, rowspan=2, padx=10, pady=10, sticky='w')
        fr_search.grid_columnconfigure(0, weight=1)
        fr_search.grid_columnconfigure(1, weight=1)
        
        self.search_entry = ttk.Entry(fr_search)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        ttk.Button(fr_search, text='Buscar', command=self.search).grid(row=0, column=1, padx=10, pady=10)
        
        self.search_result = ttk.Label(fr_search, text='Resultado', font=('Helvetica', 12, 'bold'))
        self.search_result.grid(row=1, column=0, columnspan=4, padx=10)
        
        #Tabla
        columns = ['CodigoRFID', 'Nombre', 'Apellido P', 'Apellido M', 'Fecha Nac.', 'Telefono', 'N. Casa', 'Calle', 'Colonia', 'CP', 'Email']
        columns_ID = ['Column' + str(i + 1) for i in range(len(columns))]
        
        self.tree = ttk.Treeview(self, columns=columns_ID, show='headings')
        for i in range(len(columns)):
            self.tree.column(columns_ID[i], width=70)
            self.tree.heading(columns_ID[i], text=columns[i])
        self.tree.grid(row=1, column=0, columnspan=12, sticky='nsew', padx=10, pady=5)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
    def open_add(self):
        pass
    
    def open_edit(self):
        pass
    
    def delete(self):
        pass
    
    def search(self):
        pass
