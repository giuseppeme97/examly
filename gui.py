import wx
from examly import Examly
from config import config as cf

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.init_params()
        self.init_ui()
        self.e = Examly(config=cf, console=self.append_to_console)


    def init_params(self):
        self.filters = {
            "subjects": {
                "label": "Materie:",
                "items": []
            },
            "classrooms": {
                "label": "Classi:",
                "items": []
            },
            "periods": {
                "label": "Periodi:",
                "items": []
            },
            "sectors": {
                "label": "Settori:",
                "items": []
            },
        }

        self.options = [
            {
                "id": "are_pages_numbered",
                "label": "Pagine numerate",
                "reference": None,
                "default": True
            },
            {
                "id": "are_documents_numbered",
                "label": "Documenti numerati",
                "reference": None,
                "default": True
            },
            {
                "id": "are_questions_numbered",
                "label": "Domande numerate",
                "reference": None,
                "default": False
            },
            {
                "id": "are_questions_shuffled",
                "label": "Domande mescolate",
                "reference": None,
                "default": True
            },
            {
                "id": "are_options_shuffled",
                "label": "Opzioni mescolate",
                "reference": None,
                "default": True
            },
            {
                "id": "are_solutions_exported",
                "label": "Esporta correttori",
                "reference": None,
                "default": True
            },
            {
                "id": "are_questions_single_included",
                "label": "Inclusione singola",
                "reference": None,
                "default": True
            },
            {
                "id": "are_documents_exported_to_pdf",
                "label": "Esporta in PDF",
                "reference": None,
                "default": False
            },
            {
                "id": "are_documents_included_to_zip",
                "label": "Includi in ZIP",
                "reference": None,
                "default": False
            },
        ]
        

    def init_ui(self):
        # Pannello principale
        self.panel = wx.Panel(self)
        
        # Usare un GridSizer con 1 riga e 2 colonne per i widget principali e checkbox, più un BoxSizer per la console sotto
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Sizer per il contenuto principale (disposto in due colonne)
        self.content_sizer = wx.GridSizer(1, 2, 10, 10)
        
        # Sizer per la colonna sinistra (widget principali)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Pulsante per selezione file e etichetta per il percorso
        source_file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.source_file_label = wx.StaticText(self.panel, label="Nessuna sorgente selezionata")
        source_file_btn = wx.Button(self.panel, label="Sorgente domande...")
        source_file_btn.Bind(wx.EVT_BUTTON, self.on_select_source_file)
        source_file_sizer.Add(source_file_btn, 0, wx.ALL | wx.CENTER, 5)
        source_file_sizer.Add(self.source_file_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(source_file_sizer, 0, wx.EXPAND)

        images_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.images_directory_label = wx.StaticText(self.panel, label="Nessuna cartella immagini selezionata")
        images_directory_btn = wx.Button(self.panel, label="Sorgente immagini...")
        images_directory_btn.Bind(wx.EVT_BUTTON, self.on_select_images_directory)
        images_directory_sizer.Add(images_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        images_directory_sizer.Add(self.images_directory_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(images_directory_sizer, 0, wx.EXPAND)

        # Pulsante per selezione cartella e etichetta per il percorso
        documents_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.documents_directory_label = wx.StaticText(self.panel, label="Nessuna destinazione selezionata")
        documents_directory_btn = wx.Button(self.panel, label="Destinazione documenti...")
        documents_directory_btn.Bind(wx.EVT_BUTTON, self.on_select_documents_directory)
        documents_directory_sizer.Add(documents_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        documents_directory_sizer.Add(self.documents_directory_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(documents_directory_sizer, 0, wx.EXPAND)

        template_sizer = wx.BoxSizer(wx.HORIZONTAL)
        template_btn = wx.Button(self.panel, label="Genera template...")
        template_btn.Bind(wx.EVT_BUTTON, None)
        template_sizer.Add(template_btn, 0, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(template_sizer, 0, wx.EXPAND)

        # Inserimento prefisso documenti
        self.document_filename_label = wx.StaticText(self.panel, label="Prefisso documenti:")
        self.document_filename_input = wx.TextCtrl(self.panel, value="Esame")
        self.document_filename_input.SetHint("Esame")
        self.left_sizer.Add(self.document_filename_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_filename_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento nome file zip
        self.zip_filename_label = wx.StaticText(self.panel, label="Nome file zip:")
        self.zip_filename_input = wx.TextCtrl(self.panel, value="Esami")
        self.zip_filename_input.SetHint("Esami")
        self.left_sizer.Add(self.zip_filename_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.zip_filename_input, 0, wx.ALL | wx.EXPAND, 5)

        # Due campi di input solo numeri interi
        self.documents_number_label = wx.StaticText(self.panel, label="Numero di documenti:")
        self.documents_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(1))
        self.documents_number_input.Bind(wx.EVT_CHAR, self.only_integer)
        self.questions_number_label = wx.StaticText(self.panel, label="Numero di domande:")
        self.questions_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(30))
        self.questions_number_input.Bind(wx.EVT_CHAR, self.only_integer)
        self.left_sizer.Add(self.documents_number_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.documents_number_input, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.questions_number_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.questions_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Gruppi di checkbox dinamici
        self.global_filters_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer.Add(self.global_filters_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # Aggiungere il left_sizer alla prima colonna del content_sizer
        self.content_sizer.Add(self.left_sizer, 1, wx.ALL | wx.EXPAND, 10)
        
        # Sizer per la colonna destra (checkbox finali)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.AddStretchSpacer() 
        
        # Checkbox finali (10 checkbox)
        self.options_label = wx.StaticText(self.panel, label="Opzioni aggiuntive:")
        self.right_sizer.Add(self.options_label, 0, wx.ALL | wx.EXPAND, 5)
        for element in self.options:
            element["reference"] = wx.CheckBox(self.panel, label=f"{element['label']}")
            element["reference"].SetValue(element["default"])
            self.right_sizer.Add(element["reference"], 0, wx.ALL, 5)

        self.right_sizer.AddStretchSpacer()
        self.content_sizer.Add(self.right_sizer, 1, wx.ALL | wx.EXPAND, 10)

        # Aggiungere il contenuto principale al main_sizer
        self.main_sizer.Add(self.content_sizer, 1, wx.EXPAND)

        start_btn = wx.Button(self.panel, label="Avvia")
        start_btn.Bind(wx.EVT_BUTTON, self.show_config)
        self.main_sizer.Add(start_btn, 0, wx.ALL | wx.CENTER, 5)

        # Aggiungere un widget TextCtrl come console di output
        self.console_output = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        self.main_sizer.Add(self.console_output, 0, wx.ALL | wx.EXPAND, 10)

        # Configurazione e visualizzazione del pannello
        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self.panel)  
        self.Fit() 
        self.SetTitle("Examly")
        self.Centre()
        self.Show()


    def on_select_source_file(self, e):
        with wx.FileDialog(self, "Seleziona un file", wildcard="Tutti i file (*.*)|*.xlsx|*.xls|*.csv", style=wx.FD_OPEN) as source_file_dialog:
            if source_file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            source_file = source_file_dialog.GetPath()
            self.source_file_label.SetLabel(source_file)
            cf["source_file"] = source_file
            self.append_to_console(f"Sorgente selezionata: {source_file}")
            self.refresh_source()


    def on_select_images_directory(self, e):
        with wx.DirDialog(self, "Cartella immagini:", style=wx.DD_DEFAULT_STYLE) as images_directory_dialog:
            if images_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            images_directory = images_directory_dialog.GetPath()
            self.images_directory_label.SetLabel(images_directory)
            cf["images_directory"] = images_directory
            self.append_to_console(f"Cartella immagini: {images_directory}")
            self.refresh_source()


    def on_select_documents_directory(self, e):
        with wx.DirDialog(self, "Destinazione documenti:", style=wx.DD_DEFAULT_STYLE) as documents_directory_dialog:
            if documents_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            documents_directory = documents_directory_dialog.GetPath()
            self.documents_directory_label.SetLabel(documents_directory)
            cf["documents_directory"] = documents_directory
            self.append_to_console(f"Destinazione documenti: {documents_directory}")


    def show_config(self, e):
        subjects = [subject["id"] for subject in self.filters["subjects"]["items"] if subject["reference"].GetValue()]
        classrooms = [classroom["id"] for classroom in self.filters["classrooms"]["items"] if classroom["reference"].GetValue()]
        periods = [period["id"] for period in self.filters["periods"]["items"] if period["reference"].GetValue()]
        sectors = [sector["id"] for sector in self.filters["sectors"]["items"] if sector["reference"].GetValue()]


    def refresh_source(self):
        self.e.set_config(config=cf)
        self.e.load_source()
        self.refresh_filters()
        self.main_sizer.Fit(self.panel)  
        self.Fit() 
        self.Centre()


    def refresh_filters(self):
        self.global_filters_sizer.Clear(True)
        
        for _, filter_item in self.filters.items():
            filter_item["items"] = []

        for subject in self.e.get_subjects():
            self.filters["subjects"]["items"].append({
                    "id": subject,
                    "label": subject,
                    "reference": None
                })

        for classroom in self.e.get_classrooms():
            self.filters["classrooms"]["items"].append({
                    "id": classroom,
                    "label": classroom,
                    "reference": None
                })

        for period in self.e.get_periods():
            self.filters["periods"]["items"].append({
                    "id": period,
                    "label": period,
                    "reference": None
                })

        for sector in self.e.get_sectors():
            self.filters["sectors"]["items"].append({
                    "id": sector,
                    "label": sector,
                    "reference": None
                })

    
        for _, filter_item in self.filters.items():
            filters_sizer = wx.BoxSizer(wx.VERTICAL)
            filter_label = wx.StaticText(self.panel, label=f"{filter_item['label']}")
            filters_sizer.Add(filter_label, 0, wx.TOP | wx.LEFT, 5)
            for element in filter_item["items"]:
                element["id"] = f"{element['label']}"
                element["reference"] = wx.CheckBox(self.panel, label=str(element["label"]))
                filters_sizer.Add(element["reference"], 0, wx.ALL, 5)
            self.global_filters_sizer.Add(filters_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.global_filters_sizer.Layout()
        

    def only_integer(self, event):
        key_code = event.GetKeyCode()
        if not (ord('0') <= key_code <= ord('9')) and key_code != wx.WXK_BACK:
            return
        event.Skip()


    def append_to_console(self, message):
        self.console_output.AppendText(message + "\n")


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    app.MainLoop()
