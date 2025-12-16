import wx
from threading import Thread
from examly import Examly
from configs import Configuration
from datetime import datetime
from utils import Utils
from wxutils import LoadingWindow, StyleOptionsWindow

class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)
        self.control_options = Configuration.get_control_options()
        self.init_ui()
        self.worker_thread = None
        self.examly = Examly(console=self.printer)        

    def init_ui(self):
        # Pannello principale
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.content_sizer = wx.GridSizer(1, 2, 10, 10)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Pulsante source_file
        source_file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.source_file_label = wx.StaticText(self.panel, label="Nessuna sorgente selezionata")
        self.source_file_btn = wx.Button(self.panel, label="Sorgente domande...")
        self.source_file_btn.Bind(wx.EVT_BUTTON, self.on_select_source_file)
        source_file_sizer.Add(self.source_file_btn, 0, wx.ALL | wx.CENTER, 5)
        source_file_sizer.Add(self.source_file_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(source_file_sizer, 0, wx.EXPAND)

        # Pulsante documents_directory
        documents_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.documents_directory_label = wx.StaticText(self.panel, label="Nessuna destinazione selezionata")
        self.documents_directory_btn = wx.Button(self.panel, label="Destinazione documenti...")
        self.documents_directory_btn.Bind(wx.EVT_BUTTON, self.on_select_documents_directory)
        documents_directory_sizer.Add(self.documents_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        documents_directory_sizer.Add(self.documents_directory_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(documents_directory_sizer, 0, wx.EXPAND)

        # Pulsante images_directory
        images_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.images_directory_btn = wx.Button(self.panel, label="Sorgente immagini...")
        self.images_directory_btn.Bind(wx.EVT_BUTTON, self.on_select_images_directory)
        images_directory_sizer.Add(self.images_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(images_directory_sizer, 0, wx.EXPAND)
        self.images_directory_btn.Enable(Configuration.get_are_images_inserted())

        # Pulsante template
        template_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.template_btn = wx.Button(self.panel, label="Genera template...")
        self.template_btn.Bind(wx.EVT_BUTTON, self.on_select_template_directory)
        template_sizer.Add(self.template_btn, 0, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(template_sizer, 0, wx.EXPAND)

        # Inserimento document_filename
        self.document_filename_input = wx.TextCtrl(self.panel, value=Configuration.get_document_filename())
        self.document_filename_input.SetHint("Inserire nome dei file...")
        self.left_sizer.Add(wx.StaticText(self.panel, label="Prefisso dei documenti:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_filename_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento document_title
        self.document_title_input = wx.TextCtrl(self.panel, value=Configuration.get_document_title())
        self.document_title_input.SetHint("Inserire un titolo...")
        self.left_sizer.Add(wx.StaticText(self.panel, label="Titolo dei documenti:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_title_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento document_subtitle
        self.document_subtitle_input = wx.TextCtrl(self.panel, value=Configuration.get_document_subtitle())
        self.document_subtitle_input.SetHint("Inserire un sottotitolo...")
        self.left_sizer.Add(wx.StaticText(self.panel, label="Sottotitolo dei documenti:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_subtitle_input, 0, wx.ALL | wx.EXPAND, 5)
        self.document_subtitle_input.Enable(Configuration.get_is_subtitle_included())

        # Inserimento zip_filename
        self.zip_filename_input = wx.TextCtrl(self.panel, value=Configuration.get_zip_filename())
        self.zip_filename_input.SetHint("Inserire nome dello zip...")
        self.left_sizer.Add(wx.StaticText(self.panel, label="Nome file ZIP:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.zip_filename_input, 0, wx.ALL | wx.EXPAND, 5)
        self.zip_filename_input.Enable(Configuration.get_are_documents_included_to_zip())

        # Inserimento documents_number
        self.documents_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(Configuration.get_documents_number()))
        self.documents_number_input.SetHint("Inserire numero di documenti...")
        self.documents_number_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        self.left_sizer.Add(wx.StaticText(self.panel, label="Numero di documenti:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.documents_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento start_number
        self.start_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(Configuration.get_start_number()))
        self.start_number_input.SetHint("Inserire numero di inizio...")
        self.start_number_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        self.left_sizer.Add(wx.StaticText(self.panel, label="Numero di inizio:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.start_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento questions_number
        self.questions_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(Configuration.get_questions_number()))
        self.questions_number_input.SetHint("Inserire numero di domande...")
        self.questions_number_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        self.left_sizer.Add(wx.StaticText(self.panel, label="Numero di domande per documento:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.questions_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Checkbok filtri
        self.global_filters_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer.Add(wx.StaticText(self.panel, label="Filtri:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.global_filters_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.filtered_questions_label = wx.StaticText(self.panel, label="Nessuna domanda filtrata.")
        Utils.set_label(label=self.filtered_questions_label, text="Nessuna domanda filtrata.", bold=True, color=(255, 0, 0))
        self.left_sizer.Add(self.filtered_questions_label, 0, wx.ALL | wx.EXPAND, 5)

        # Aggiunta della sezione sinistra
        self.content_sizer.Add(self.left_sizer, 1, wx.ALL | wx.EXPAND, 10)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.AddStretchSpacer()

        # Checkbox opzioni
        self.right_sizer.Add(wx.StaticText(self.panel, label="Opzioni di controllo:"), 0, wx.ALL | wx.EXPAND, 5)
        for option, properties in self.control_options.items():
            properties["reference"] = wx.CheckBox(self.panel, label=f"{properties['label']}")
            properties["reference"].SetValue(properties["default"])
            properties["reference"].Bind(wx.EVT_CHECKBOX, self.on_change_options_checkbox)                
            if properties["disabled"]:
                properties["reference"].Disable()
            self.right_sizer.Add(properties["reference"], 0, wx.ALL, 5)

        # Opzioni di stile
        other_btn = wx.Button(self.panel, label="Opzioni di stile...")
        other_btn.Bind(wx.EVT_BUTTON, self.on_open_style_options)
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
            Utils.set_label(label=self.source_file_label, text="OK", bold=True, color=(0, 255, 0))
            Configuration.set_source_file(source_file)
            self.printer(f"📝 Sorgente selezionata: {source_file}")
            self.refresh_source()

    def on_select_images_directory(self, e):
        with wx.DirDialog(self, "Cartella immagini:", style=wx.DD_DEFAULT_STYLE) as images_directory_dialog:
            if images_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            images_directory = images_directory_dialog.GetPath()
            Utils.set_label(label=self.images_directory_label, text="OK", bold=True, color=(0, 255, 0))
            Configuration.set_images_directory(images_directory)
            self.printer(f"Cartella immagini: {images_directory}")
            self.refresh_source()

    def on_select_documents_directory(self, e):
        with wx.DirDialog(self, "Destinazione documenti:", style=wx.DD_DEFAULT_STYLE) as documents_directory_dialog:
            if documents_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            documents_directory = documents_directory_dialog.GetPath()
            Utils.set_label(label=self.documents_directory_label, text="OK", bold=True, color=(0, 255, 0))
            Configuration.set_documents_directory(documents_directory)
            self.printer(f"📁 Destinazione documenti: {documents_directory}")

    def on_select_template_directory(self, e):
        with wx.DirDialog(self, "Destinazione template:", style=wx.DD_DEFAULT_STYLE) as template_directory_dialog:
            if template_directory_dialog.ShowModal() == wx.ID_CANCEL:
                return
            template_directory = template_directory_dialog.GetPath()
            Configuration.set_template_directory(template_directory)
            self.examly.new_template()
            self.printer(f"Template salvato in: {template_directory}")

    def on_change_filter_value(self, e):
        for filter, filter_items in self.checkboxes_filters.items():
            Configuration.set_filter_values(filter, [item["name"] for item in filter_items if item["reference"].GetValue()])
        self.refresh_cardinality()

    def on_change_options_checkbox(self, e):
        for option, properties in self.control_options.items():
            getattr(Configuration, f"set_{option}")(properties["reference"].GetValue())
        self.images_directory_btn.Enable(Configuration.get_are_images_inserted())
        self.document_subtitle_input.Enable(Configuration.get_is_subtitle_included())
        self.zip_filename_input.Enable(Configuration.get_are_documents_included_to_zip())
        self.refresh_cardinality()

    def on_open_style_options(self, e):
        fonts, languages = Configuration.get_selection_lists()
        dialog = StyleOptionsWindow(self, title="Opzioni di stile")
        if dialog.ShowModal() == wx.ID_OK:
            Configuration.set_font(fonts[dialog.font_selection.GetSelection()])
            # Configuration.set_language(languages[dialog.language_selection.GetSelection()])
            Configuration.set_title_size(dialog.title_size_input.GetValue())
            Configuration.set_questions_size(dialog.questions_size_input.GetValue())
            Configuration.set_images_size(dialog.images_size_input.GetValue())
            Configuration.set_columns_number(dialog.columns_number_input.GetValue())
            Configuration.set_left_margin(dialog.left_margin_input.GetValue())
            Configuration.set_right_margin(dialog.right_margin_input.GetValue())
        dialog.Destroy()

    def on_start(self, e):
        # CHECK
        document_filename_value = self.document_filename_input.GetValue()
        document_title_value = self.document_title_input.GetValue()
        document_subtitle_value = self.document_subtitle_input.GetValue()
        zip_filename_value = self.zip_filename_input.GetValue()
        documents_number_value = self.documents_number_input.GetValue()
        start_number_value = self.start_number_input.GetValue()
        questions_number_value = self.questions_number_input.GetValue()
        source_file_value = Configuration.get_source_file()
        documents_directory_value = Configuration.get_documents_directory()

        if not source_file_value:
            wx.MessageBox("Non è stata caricata alcuna sorgente.", "Attenzione!", wx.OK | wx.ICON_INFORMATION)
            return
        
        if not self.examly.is_ready():
            wx.MessageBox("La sorgente non è stata caricata correttamente o validata.", "Attenzione!", wx.OK | wx.ICON_INFORMATION)
            return
        
        if not documents_directory_value:
            wx.MessageBox("Non è stata scelta la cartella di destinazione dei documenti.", "Attenzione!", wx.OK | wx.ICON_INFORMATION)
            return
        
        #TODO: inserire i controlli doppi
        if document_filename_value and document_title_value and documents_number_value.isdigit() and start_number_value.isdigit() and questions_number_value.isdigit():
            Configuration.set_document_filename(document_filename_value)
            Configuration.set_document_title(document_title_value)
            Configuration.set_document_subtitle(document_subtitle_value) ###
            Configuration.set_zip_filename(zip_filename_value) ###
            Configuration.set_documents_number(int(documents_number_value)) 
            Configuration.set_start_number(int(start_number_value))
            Configuration.set_questions_number(int(questions_number_value))
        else:
            wx.MessageBox("Uno o più campi obbligatori mancanti.", "Attenzione!", wx.OK | wx.ICON_INFORMATION)
            return
        # END CHECK

        for filter, filter_items in self.checkboxes_filters.items():
            Configuration.set_filter_values(filter, [item["name"] for item in filter_items if item["reference"].GetValue()])

        for option, properties in self.control_options.items():
            getattr(Configuration, f"set_{option}")(properties["reference"].GetValue())
        
        self.start_btn.Disable()
        dialog = LoadingWindow(frame)
        worker_thread = Thread(target=lambda: dialog.process(self.examly))
        worker_thread.start()
        if dialog.ShowModal() == wx.ID_OK:
            self.start_btn.Enable()
            dialog.Destroy()

    def on_complete(self, *e):
        if not self.worker_thread.is_alive():
            self.start_btn.Enable()

    def run_examly(self):
        if self.examly.is_ready():
            self.examly.write_exams()
            wx.CallAfter(self.on_complete)

    def refresh_cardinality(self):
        if self.examly.is_ready():
            Utils.set_label(label=self.filtered_questions_label, text=f"Domande filtrate: {str(self.examly.get_questions_cardinality())}", bold=True, color=(0, 0, 0))
        else:
            Utils.set_label(label=self.filtered_questions_label, text="Nessuna domanda filtrata.", bold=True, color=(255, 0, 0))

    def refresh_source(self):
        self.examly.connect_source(web_mode=False, source=Configuration.get_source_file())
        self.refresh_filters()
        self.refresh_cardinality()
        
        if not self.examly.is_ready():
            wx.MessageBox("Errore nel caricamento o nella validazione della sorgente.", "Attenzione!", wx.OK | wx.ICON_INFORMATION)
            
    def refresh_filters(self):
        self.printer("🔄 Aggiorno filtri...")
        self.global_filters_sizer.Clear(True)
        self.filters = self.examly.get_filters()
        self.checkboxes_filters = {}
        
        for filter, filter_items in self.filters.items():
            self.checkboxes_filters[filter] = []
            for value in filter_items:
                self.checkboxes_filters[filter].append({
                    "name": value,
                    "label": value,
                    "reference": None
                })

        for filter, filter_items in self.checkboxes_filters.items():
            filters_sizer = wx.BoxSizer(wx.VERTICAL)
            filter_label = wx.StaticText(self.panel, label=f"{filter}:")
            Utils.set_label(label=filter_label, text=f"{filter}:", bold=True, color=(0, 0, 255))
            filters_sizer.Add(filter_label, 0, wx.TOP | wx.LEFT, 5)
            for item in filter_items:
                item["reference"] = wx.CheckBox(self.panel, label=str(item["label"]))
                item["reference"].Bind(wx.EVT_CHECKBOX, self.on_change_filter_value)
                filters_sizer.Add(item["reference"], 0, wx.ALL, 5)
            self.global_filters_sizer.Add(filters_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.global_filters_sizer.Layout()
        self.main_sizer.Fit(self.panel)
        self.Fit()
        self.Centre()
        self.on_change_filter_value(None)

    def printer(self, message):
        self.console_output.AppendText(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}' + "\n")


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None)
    app.MainLoop()