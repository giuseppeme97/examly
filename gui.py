import wx
from threading import Thread
from examly import Examly
from configs import Configuration
from datetime import datetime
from utils import Utils


class ExamlyWorker(Thread):
    def __init__(self, functor, callback):
        super(ExamlyWorker, self).__init__()
        self.functor = functor
        self.callback = callback

    def run(self):
        self.functor()
        wx.CallAfter(self.callback, 0)


class StyleOptionsWindow(wx.Dialog):
    def __init__(self, parent, title):
        super(StyleOptionsWindow, self).__init__(
            parent, title=title)
        
        _, _, fonts, languages = Configuration.get_configs()

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridSizer(cols=2, vgap=10, hgap=10)

        # Selection per "font"
        grid_sizer.Add(wx.StaticText(panel, label="Font:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.font_selection = wx.Choice(panel, choices=fonts)
        self.font_selection.SetSelection(0)
        grid_sizer.Add(self.font_selection, 1, wx.EXPAND)

        # Selection per "linguaggio"
        grid_sizer.Add(wx.StaticText(panel, label="Linguaggio:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.language_selection = wx.Choice(panel, choices=languages)
        self.language_selection.SetSelection(0)
        grid_sizer.Add(self.language_selection, 1, wx.EXPAND)

        # Text control per "dimensione titolo"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione titolo:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.title_size_input = wx.TextCtrl(panel, value=str(Configuration.get_title_size()))
        self.title_size_input.SetHint(str(Configuration.get_title_size()))
        self.title_size_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        grid_sizer.Add(self.title_size_input, 1, wx.EXPAND)

        # Text control per "dimensione domande"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione domande:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.questions_size_input = wx.TextCtrl(panel, value=str(Configuration.get_questions_size()))
        self.questions_size_input.SetHint(str(Configuration.get_questions_size()))
        self.questions_size_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        grid_sizer.Add(self.questions_size_input, 1, wx.EXPAND)

        # Text control per "dimensione immagini"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione immagini:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.images_size_input = wx.TextCtrl(panel, value=str(Configuration.get_images_size()))
        self.images_size_input.SetHint(str(Configuration.get_images_size()))
        self.images_size_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        grid_sizer.Add(self.images_size_input, 1, wx.EXPAND)

        # Text control per "Distanza fra domande"
        # grid_sizer.Add(wx.StaticText(panel, label="Distanza fra domande:"), 0, wx.ALIGN_CENTER_VERTICAL)
        # self.questions_distance_input = wx.TextCtrl(panel, value=str(Configuration.get_questions_distance()))
        # self.questions_distance_input.SetHint(str(Configuration.get_questions_distance()))
        # self.questions_distance_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        # grid_sizer.Add(self.questions_distance_input, 1, wx.EXPAND)

        # Text control per "Numero di colonne della sezione"
        grid_sizer.Add(wx.StaticText(panel, label="Numero di colonne della sezione:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.columns_number_input = wx.TextCtrl(panel, value=str(Configuration.get_columns_number()))
        self.columns_number_input.SetHint(str(Configuration.get_columns_number()))
        self.columns_number_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        grid_sizer.Add(self.columns_number_input, 1, wx.EXPAND)

        # Text control per "Dimensione margine sinistro"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione margine sinistro:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.left_margin_input = wx.TextCtrl(panel, value=str(Configuration.get_left_margin()))
        self.left_margin_input.SetHint(str(Configuration.get_left_margin()))
        self.left_margin_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        grid_sizer.Add(self.left_margin_input, 1, wx.EXPAND)

        # Text control per "Dimensione margine destro"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione margine destro:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.right_margin_input = wx.TextCtrl(panel, value=str(Configuration.get_right_margin()))
        self.right_margin_input.SetHint(str(Configuration.get_right_margin()))
        self.right_margin_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        grid_sizer.Add(self.right_margin_input, 1, wx.EXPAND)

        # Aggiunta pulsanti OK e Annulla
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, wx.ID_OK, label="OK")
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label="Annulla")
        button_sizer.Add(ok_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL | wx.CENTER, 5)

        # Aggiungiamo il pulsante alla griglia
        grid_sizer.Add(button_sizer, 1, wx.EXPAND)
        main_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 15)
        panel.SetSizer(main_sizer)
        main_sizer.Fit(panel)
        self.Fit()
        self.Centre()


class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)
        self.init_params()
        self.init_ui()
        self.examly = Examly(console=self.printer)

    def init_params(self):
        self.filters, self.control_options, _, _ = Configuration.get_configs()

    def init_ui(self):
        # Pannello principale
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.content_sizer = wx.GridSizer(1, 2, 10, 10)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Pulsante source_file
        source_file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.source_file_label = wx.StaticText(
            self.panel, label="Nessuna sorgente selezionata")
        source_file_btn = wx.Button(self.panel, label="Sorgente domande...")
        source_file_btn.Bind(wx.EVT_BUTTON, self.on_select_source_file)
        source_file_sizer.Add(source_file_btn, 0, wx.ALL | wx.CENTER, 5)
        source_file_sizer.Add(self.source_file_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(source_file_sizer, 0, wx.EXPAND)

        # Pulsante images_directory
        images_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.images_directory_label = wx.StaticText(
            self.panel, label="Nessuna cartella immagini selezionata")
        images_directory_btn = wx.Button(
            self.panel, label="Sorgente immagini...")
        images_directory_btn.Bind(
            wx.EVT_BUTTON, self.on_select_images_directory)
        images_directory_sizer.Add(
            images_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        images_directory_sizer.Add(
            self.images_directory_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(images_directory_sizer, 0, wx.EXPAND)

        # Pulsante documents_directory
        documents_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.documents_directory_label = wx.StaticText(
            self.panel, label="Nessuna destinazione selezionata")
        documents_directory_btn = wx.Button(
            self.panel, label="Destinazione documenti...")
        documents_directory_btn.Bind(
            wx.EVT_BUTTON, self.on_select_documents_directory)
        documents_directory_sizer.Add(
            documents_directory_btn, 0, wx.ALL | wx.CENTER, 5)
        documents_directory_sizer.Add(
            self.documents_directory_label, 1, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(documents_directory_sizer, 0, wx.EXPAND)

        # Pulsante template
        template_sizer = wx.BoxSizer(wx.HORIZONTAL)
        template_btn = wx.Button(self.panel, label="Genera template...")
        template_btn.Bind(wx.EVT_BUTTON, self.on_select_template_directory)
        template_sizer.Add(template_btn, 0, wx.ALL | wx.CENTER, 5)
        self.left_sizer.Add(template_sizer, 0, wx.EXPAND)

        # Inserimento document_filename
        self.document_filename_input = wx.TextCtrl(self.panel, value=Configuration.get_document_filename())
        self.document_filename_input.SetHint(Configuration.get_document_filename())
        self.left_sizer.Add(wx.StaticText(self.panel, label="Prefisso dei documenti:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_filename_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento document_title
        self.document_title_input = wx.TextCtrl(self.panel, value=Configuration.get_document_title())
        self.document_title_input.SetHint(Configuration.get_document_title())
        self.left_sizer.Add(wx.StaticText(self.panel, label="Titolo dei documenti:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.document_title_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento zip_filename
        self.zip_filename_input = wx.TextCtrl(self.panel, value=Configuration.get_zip_filename())
        self.zip_filename_input.SetHint(Configuration.get_zip_filename())
        self.left_sizer.Add(wx.StaticText(self.panel, label="Nome file ZIP:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.zip_filename_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento documents_number
        self.documents_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(Configuration.get_documents_number()))
        self.documents_number_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        self.left_sizer.Add(wx.StaticText(self.panel, label="Numero di documenti:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.documents_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Inserimento questions_number
        self.questions_number_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=str(Configuration.get_questions_number()))
        self.questions_number_input.Bind(wx.EVT_CHAR, Utils.only_integer)
        self.left_sizer.Add(wx.StaticText(self.panel, label="Numero di domande per documento:"), 0, wx.ALL | wx.EXPAND, 5)
        self.left_sizer.Add(self.questions_number_input, 0, wx.ALL | wx.EXPAND, 5)

        # Checkbok filtri
        self.global_filters_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer.Add(self.global_filters_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.content_sizer.Add(self.left_sizer, 1, wx.ALL | wx.EXPAND, 10)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.AddStretchSpacer()

        # Checkbox opzioni
        self.right_sizer.Add(wx.StaticText(self.panel, label="Opzioni di controllo:"), 0, wx.ALL | wx.EXPAND, 5)
        
        for _, option in self.control_options.items():
            option["reference"] = wx.CheckBox(self.panel, label=f"{option['label']}")
            option["reference"].SetValue(option["default"])
            self.right_sizer.Add(option["reference"], 0, wx.ALL, 5)

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
        self.console_output = wx.TextCtrl(
            self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
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

    def on_open_style_options(self, e):
        _, _, fonts, languages = Configuration.get_configs()
        dialog = StyleOptionsWindow(self, title="Opzioni di stile")
        if dialog.ShowModal() == wx.ID_OK:
            Configuration.set_font(fonts[dialog.font_selection.GetSelection()])
            Configuration.set_language(languages[dialog.language_selection.GetSelection()])
            Configuration.set_title_size(dialog.title_size_input.GetValue())
            Configuration.set_questions_size(dialog.questions_size_input.GetValue())
            Configuration.set_images_size(dialog.images_size_input.GetValue())
            # Configuration.set_questions_distance(dialog.questions_distance_input.GetValue())
            Configuration.set_columns_number(dialog.columns_number_input.GetValue())
            Configuration.set_left_margin(dialog.left_margin_input.GetValue())
            Configuration.set_right_margin(dialog.right_margin_input.GetValue())
        dialog.Destroy()

    def on_start(self, e):
        Configuration.set_document_filename(
            self.document_filename_input.GetValue())
        Configuration.set_zip_filename(self.zip_filename_input.GetValue())
        Configuration.set_documents_number(
            int(self.documents_number_input.GetValue()))
        Configuration.set_questions_number(
            int(self.questions_number_input.GetValue()))
        Configuration.set_document_title(self.document_title_input.GetValue())

        for key in self.filters:
            getattr(Configuration, f"set_{key}")(
                [item["name"] for item in self.filters[key]["items"] if item["reference"].GetValue()])

        for key, option in self.control_options.items():
            getattr(Configuration, f"set_{key}")(
                option["reference"].GetValue())

        self.start_btn.Disable()
        self.worker_thread = ExamlyWorker(self.run_examly, self.on_complete)
        self.worker_thread.start()

    def on_complete(self, *e):
        if not self.worker_thread.is_alive():
            self.start_btn.Enable()

    def run_examly(self):
        if self.examly.is_source_validated():
            self.examly.write_exams()
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
            filter_label = wx.StaticText(
                self.panel, label=f"{filter_item['label']}")
            filters_sizer.Add(filter_label, 0, wx.TOP | wx.LEFT, 5)
            for element in filter_item["items"]:
                element["reference"] = wx.CheckBox(
                    self.panel, label=str(element["label"]))
                filters_sizer.Add(element["reference"], 0, wx.ALL, 5)
            self.global_filters_sizer.Add(
                filters_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.global_filters_sizer.Layout()

    def printer(self, message):
        self.console_output.AppendText(
            f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}' + "\n")


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None)
    app.MainLoop()
