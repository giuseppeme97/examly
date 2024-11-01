import wx
import threading
from examly import Examly
from configs import Configuration
import time

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.init_params()
        self.init_ui()
        self.examly = Examly(console=self.printer)


    def init_params(self):
        self.filters, self.options = Configuration.get_void_configs()


    def init_ui(self):
        # Pannello principale
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.content_sizer = wx.GridSizer(1, 2, 10, 10)        
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Pulsante source_file
        source_file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.source_file_label = wx.StaticText(self.panel, label="Nessuna sorgente selezionata")
        source_file_btn = wx.Button(self.panel, label="Sorgente domande...")
        source_file_btn.Bind(wx.EVT_BUTTON, self.on_select_source_file)
        source_file_sizer.Add(source_file_btn, 0, wx.ALL | wx.CENTER, 5)
        source_file_sizer.Add(self.source_file_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(source_file_sizer, 0, wx.EXPAND)

        # Pulsante images_directory
        images_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.images_directory_label = wx.StaticText(self.panel, label="Nessuna cartella immagini selezionata")
        images_directory_btn = wx.Button(self.panel, label="Sorgente immagini...")
        images_directory_btn.Bind(wx.EVT_BUTTON, self.on_select_images_directory)
        images_directory_sizer.Add(images_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        images_directory_sizer.Add(self.images_directory_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(images_directory_sizer, 0, wx.EXPAND)

        # Pulsante documents_directory
        documents_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.documents_directory_label = wx.StaticText(self.panel, label="Nessuna destinazione selezionata")
        documents_directory_btn = wx.Button(self.panel, label="Destinazione documenti...")
        documents_directory_btn.Bind(wx.EVT_BUTTON, self.on_select_documents_directory)
        documents_directory_sizer.Add(documents_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        documents_directory_sizer.Add(self.documents_directory_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(documents_directory_sizer, 0, wx.EXPAND)

        # Pulsante template
        template_sizer = wx.BoxSizer(wx.HORIZONTAL)
        template_btn = wx.Button(self.panel, label="Genera template...")
        template_btn.Bind(wx.EVT_BUTTON, self.on_select_template_directory)
        template_sizer.Add(template_btn, 0, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(template_sizer, 0, wx.EXPAND)

        # Inserimento document_filename
        self.document_filename_label = wx.StaticText(self.panel, label="Prefisso documenti:")
        self.document_filename_input = wx.TextCtrl(self.panel, value=Configuration.get_document_filename())
        self.document_filename_input.SetHint(Configuration.get_document_filename())
        self.left_sizer.Add(self.document_filename_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_filename_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento document_title
        self.document_title_label = wx.StaticText(self.panel, label="Titolo documenti:")
        self.document_title_input = wx.TextCtrl(self.panel, value=Configuration.get_document_title())
        self.document_title_input.SetHint(Configuration.get_document_title())
        self.left_sizer.Add(self.document_title_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_title_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento zip_filename
        self.zip_filename_label = wx.StaticText(self.panel, label="Nome file zip:")
        self.zip_filename_input = wx.TextCtrl(self.panel, value=Configuration.get_zip_filename())
        self.zip_filename_input.SetHint(Configuration.get_zip_filename())
        self.left_sizer.Add(self.zip_filename_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.zip_filename_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento documents_number
        self.documents_number_label = wx.StaticText(self.panel, label="Numero di documenti:")
        self.documents_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(Configuration.get_documents_number()))
        self.documents_number_input.Bind(wx.EVT_CHAR, self.only_integer)
        self.left_sizer.Add(self.documents_number_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.documents_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento questions_number
        self.questions_number_label = wx.StaticText(self.panel, label="Numero di domande:")
        self.questions_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(Configuration.get_questions_number()))
        self.questions_number_input.Bind(wx.EVT_CHAR, self.only_integer)
        self.left_sizer.Add(self.questions_number_label, 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.questions_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Checkbok filtri
        self.global_filters_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer.Add(self.global_filters_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        self.content_sizer.Add(self.left_sizer, 1, wx.ALL | wx.EXPAND, 10)        
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.AddStretchSpacer() 
        
        # Checkbox opzioni
        self.options_label = wx.StaticText(self.panel, label="Opzioni aggiuntive:")
        self.right_sizer.Add(self.options_label, 0, wx.ALL | wx.EXPAND, 5)
        for _, option in self.options.items():
            option["reference"] = wx.CheckBox(self.panel, label=f"{option['label']}")
            option["reference"].SetValue(option["default"])
            self.right_sizer.Add(option["reference"], 0, wx.ALL, 5)

        other_btn = wx.Button(self.panel, label="Opzioni di stile...")
        other_btn.Bind(wx.EVT_BUTTON, None)
        self.right_sizer.AddStretchSpacer()
        self.right_sizer.Add(other_btn, 0, wx.CENTER)

        self.right_sizer.AddStretchSpacer()
        self.content_sizer.Add(self.right_sizer, 1, wx.ALL | wx.EXPAND, 10)
        self.main_sizer.Add(self.content_sizer, 1, wx.EXPAND)

        # Pulsante avvio
        self.start_btn = wx.Button(self.panel, label="Avvia ➠")
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        self.main_sizer.Add(self.start_btn, 0, wx.ALL | wx.CENTER, 5)

        # Console
        self.console_output = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        self.main_sizer.Add(self.console_output, 0, wx.ALL | wx.EXPAND, 10)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self.panel)  
        self.Fit() 
        self.SetTitle(Configuration.get_app_name())
        self.Centre()
        self.Show()


    def on_select_source_file(self, e):
        with wx.FileDialog(self, "Seleziona un file", wildcard="Tutti i file (*.*)|*.xlsx|*.xls|*.csv", style=wx.FD_OPEN) as source_file_dialog:
            if source_file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            source_file = source_file_dialog.GetPath()
            self.source_file_label.SetLabel(source_file)
            Configuration.set_source_file(source_file) 
            self.printer(f"Sorgente selezionata: {source_file}")
            self.refresh_source()


    def on_select_images_directory(self, e):
        with wx.DirDialog(self, "Cartella immagini:", style=wx.DD_DEFAULT_STYLE) as images_directory_dialog:
            if images_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            images_directory = images_directory_dialog.GetPath()
            self.images_directory_label.SetLabel(images_directory)
            Configuration.set_images_directory(images_directory)
            self.printer(f"Cartella immagini: {images_directory}")
            self.refresh_source()


    def on_select_documents_directory(self, e):
        with wx.DirDialog(self, "Destinazione documenti:", style=wx.DD_DEFAULT_STYLE) as documents_directory_dialog:
            if documents_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            documents_directory = documents_directory_dialog.GetPath()
            self.documents_directory_label.SetLabel(documents_directory)
            Configuration.set_documents_directory(documents_directory)
            self.printer(f"Destinazione documenti: {documents_directory}")


    def on_select_template_directory(self, e):
        with wx.DirDialog(self, "Destinazione template:", style=wx.DD_DEFAULT_STYLE) as template_directory_dialog:
            if template_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            template_directory = template_directory_dialog.GetPath()
            Configuration.set_template_directory(template_directory)
            self.examly.new_template()
            self.printer(f"Template salvato in: {template_directory}")


    def on_start(self, e):
        # Params
        Configuration.set_document_filename(self.document_filename_input.GetValue())
        Configuration.set_zip_filename(self.zip_filename_input.GetValue())
        Configuration.set_documents_number(int(self.documents_number_input.GetValue()))
        Configuration.set_questions_number(int(self.questions_number_input.GetValue()))
        Configuration.set_document_title(self.document_title_input.GetValue())

        for key in self.filters:
            getattr(Configuration, f"set_{key}")([item["name"] for item in self.filters[key]["items"] if item["reference"].GetValue()])
        
        for key, option in self.options.items():
            getattr(Configuration, f"set_{key}")(option["reference"].GetValue())

        self.start_btn.Disable()
        self.worker_thread = threading.Thread(target=self.start)
        self.worker_thread.start()        
        # self.Bind(wx.EVT_TIMER, self.on_check_thread)
        # self.timer = wx.Timer(self)
        # self.timer.Start(100)


    def on_complete(self):
        if not self.worker_thread.is_alive():
            self.start_btn.Enable() 
         

    def start(self):
        self.examly.write_exams()
        time.sleep(2)
        wx.CallAfter(self.on_complete)


    def refresh_source(self):
        self.examly.load_source()
        self.refresh_filters()
        self.main_sizer.Fit(self.panel)  
        self.Fit() 
        self.Centre()


    def refresh_filters(self):
        self.global_filters_sizer.Clear(True)

        for key in self.filters:
            self.filters[key]["items"] = []
            for item in getattr(self.examly, f"get_{key}")():
                self.filters[key]["items"].append({
                    "name": item,
                    "label": item,
                    "reference": None
                })

        for _, filter_item in self.filters.items():
            filters_sizer = wx.BoxSizer(wx.VERTICAL)
            filter_label = wx.StaticText(self.panel, label=f"{filter_item['label']}")
            filters_sizer.Add(filter_label, 0, wx.TOP | wx.LEFT, 5)
            for element in filter_item["items"]:
                # element["name"] = f"{element['label']}"
                element["reference"] = wx.CheckBox(self.panel, label=str(element["label"]))
                filters_sizer.Add(element["reference"], 0, wx.ALL, 5)
            self.global_filters_sizer.Add(filters_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.global_filters_sizer.Layout()
        

    def only_integer(self, event):
        key_code = event.GetKeyCode()
        if not (ord('0') <= key_code <= ord('9')) and key_code != wx.WXK_BACK:
            return
        event.Skip()


    def printer(self, message):
        self.console_output.AppendText(message + "\n")


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    app.MainLoop()
