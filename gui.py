import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        # Pannello principale
        panel = wx.Panel(self)
        
        # Usare un GridSizer con 1 riga e 2 colonne per i widget principali e checkbox, più un BoxSizer per la console sotto
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Sizer per il contenuto principale (disposto in due colonne)
        content_sizer = wx.GridSizer(1, 2, 10, 10)
        
        # Sizer per la colonna sinistra (widget principali)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # 1. Pulsante per selezione file e etichetta per il percorso
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.file_path_label = wx.StaticText(panel, label="Nessuna sorgente selezionata")
        file_btn = wx.Button(panel, label="Sorgente domande...")
        file_btn.Bind(wx.EVT_BUTTON, self.on_select_file)
        file_sizer.Add(file_btn, 0, wx.ALL | wx.CENTER, 5)
        file_sizer.Add(self.file_path_label, 1, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(file_sizer, 0, wx.EXPAND)

        # 2. Pulsante per selezione cartella e etichetta per il percorso
        folder_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.folder_path_label = wx.StaticText(panel, label="Nessuna destinazione selezionata")
        folder_btn = wx.Button(panel, label="Destinazione documenti...")
        folder_btn.Bind(wx.EVT_BUTTON, self.on_select_folder)
        folder_sizer.Add(folder_btn, 0, wx.ALL | wx.CENTER, 5)
        folder_sizer.Add(self.folder_path_label, 1, wx.ALL | wx.CENTER, 5)
        left_sizer.Add(folder_sizer, 0, wx.EXPAND)

        # Inserimento prefisso documenti
        self.text_input1_label = wx.StaticText(panel, label="Prefisso documenti:")
        self.text_input1 = wx.TextCtrl(panel)
        left_sizer.Add(self.text_input1_label, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.text_input1, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento nome file zip
        self.text_input2_label = wx.StaticText(panel, label="Nome file zip:")
        self.text_input2 = wx.TextCtrl(panel)
        left_sizer.Add(self.text_input2_label, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.text_input2, 0, wx.ALL | wx.EXPAND, 5)

        # Due campi di input solo numeri interi
        self.int_input1_label = wx.StaticText(panel, label="Numero di documenti:")
        self.int_input1 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.int_input1.Bind(wx.EVT_CHAR, self.only_integer)
        self.int_input2_label = wx.StaticText(panel, label="Numero di domande:")
        self.int_input2 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.int_input2.Bind(wx.EVT_CHAR, self.only_integer)
        left_sizer.Add(self.int_input1_label, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.int_input1, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.int_input2_label, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.int_input2, 0, wx.ALL | wx.EXPAND, 5)

        # Gruppi di checkbox dinamici
        checkbox_groups = {
            "Materie": ["Opzione 1", "Opzione 2", "Opzione 3"],
            "Classi": ["Scelta A", "Scelta B", "Scelta C"],
            "Periodi": ["Elem X", "Elem Y", "Elem Z"],
            "Settori": ["Valore 1", "Valore 2", "Valore 3"]
        }

        for type, elements in checkbox_groups.items():
            group_sizer = wx.BoxSizer(wx.VERTICAL)
            group_label = wx.StaticText(panel, label=f"{type}")
            group_sizer.Add(group_label, 0, wx.TOP | wx.LEFT, 5)
            for element in elements:
                chk = wx.CheckBox(panel, label=element)
                group_sizer.Add(chk, 0, wx.ALL, 5)
            left_sizer.Add(group_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Aggiungere il left_sizer alla prima colonna del content_sizer
        content_sizer.Add(left_sizer, 1, wx.ALL | wx.EXPAND, 10)
        
        # Sizer per la colonna destra (checkbox finali)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        # right_sizer.AddStretchSpacer() !!!!!

        options_labels = [
            "Numeri di pagina",
            "Documenti numerati",
            "Domande numerate",
            "Domande mescolate",
            "Opzioni mescolate",
            "Esporta correttori",
            "Inclusione singola",
            "Esporta in PDF",
            "Includi in ZIP"
        ]

        # Checkbox finali (10 checkbox)
        self.options_label = wx.StaticText(panel, label="Opzioni aggiuntive:")
        right_sizer.Add(self.options_label, 0, wx.ALL | wx.EXPAND, 5)
        for label in options_labels:
            chk = wx.CheckBox(panel, label=f"{label}")
            right_sizer.Add(chk, 0, wx.ALL, 5)

        right_sizer.AddStretchSpacer()
        content_sizer.Add(right_sizer, 1, wx.ALL | wx.EXPAND, 10)

        # Aggiungere il contenuto principale al main_sizer
        main_sizer.Add(content_sizer, 1, wx.EXPAND)

        # Aggiungere un widget TextCtrl come console di output
        self.console_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        main_sizer.Add(self.console_output, 0, wx.ALL | wx.EXPAND, 10)

        # Configurazione e visualizzazione del pannello
        panel.SetSizer(main_sizer)
        main_sizer.Fit(panel)  # Adatta il pannello in base al contenuto
        self.Fit()              # Adatta il frame in base al pannello

        self.SetTitle("EXAMLY")
        self.Centre()
        self.Show()

    def on_select_file(self, event):
        with wx.FileDialog(self, "Seleziona un file", wildcard="Tutti i file (*.*)|*.xlsx|*.xls|*.csv", style=wx.FD_OPEN) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = file_dialog.GetPath()
            self.file_path_label.SetLabel(path)
            self.append_to_console(f"File selezionato: {path}")

    def on_select_folder(self, event):
        with wx.DirDialog(self, "Seleziona una cartella", style=wx.DD_DEFAULT_STYLE) as dir_dialog:
            if dir_dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dir_dialog.GetPath()
            self.folder_path_label.SetLabel(path)
            self.append_to_console(f"Cartella selezionata: {path}")

    def only_integer(self, event):
        key_code = event.GetKeyCode()
        if not (ord('0') <= key_code <= ord('9')) and key_code != wx.WXK_BACK:
            return
        event.Skip()

    def append_to_console(self, message):
        """Funzione per aggiungere testo alla console di output."""
        self.console_output.AppendText(message + "\n")

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    app.MainLoop()
