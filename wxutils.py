import wx
from configs import Configuration
from utils import Utils


class NumericValidator(wx.Validator):
    def __init__(self):
        super().__init__()

    def Clone(self):
        return NumericValidator()

    def Validate(self, win):
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()
        return text == "" or text.replace('.', '', 1).isdigit()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
    

class LoadingWindow(wx.Dialog):
    def __init__(self, parent, title="Examly"):
        super().__init__(parent, title=title, style=wx.CAPTION | wx.STAY_ON_TOP | wx.CENTER)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        message = wx.StaticText(panel, label="Generazione dei documenti in corso...")
        sizer.Add(message, 0, wx.ALL | wx.CENTER, 20)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        self.Fit()
        self.Centre()
        
    def process(self, examly):
        try:
            examly.write_exams()
        except Exception:
            print(Exception)
        finally:
            wx.CallAfter(self.EndModal, wx.ID_OK)


class StyleOptionsWindow(wx.Dialog):
    def __init__(self, parent, title):
        super(StyleOptionsWindow, self).__init__(parent, title=title)
        
        fonts, languages = Configuration.get_selection_lists()

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridSizer(cols=2, vgap=10, hgap=10)

        # Selection per "font"
        grid_sizer.Add(wx.StaticText(panel, label="Font:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.font_selection = wx.Choice(panel, choices=fonts)
        self.font_selection.SetSelection(fonts.index(Configuration.get_font()))
        grid_sizer.Add(self.font_selection, 1, wx.EXPAND)

        # Selection per "linguaggio"
        # grid_sizer.Add(wx.StaticText(panel, label="Linguaggio:"), 0, wx.ALIGN_CENTER_VERTICAL)
        # self.language_selection = wx.Choice(panel, choices=languages)
        # self.language_selection.SetSelection(0)
        # grid_sizer.Add(self.language_selection, 1, wx.EXPAND)

        # Text control per "dimensione titolo"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione titolo:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.title_size_input = wx.TextCtrl(panel, value=str(Configuration.get_title_size()), validator=NumericValidator())
        self.title_size_input.SetHint(str(Configuration.get_title_size()))
        grid_sizer.Add(self.title_size_input, 1, wx.EXPAND)

        # Text control per "dimensione domande"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione domande:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.questions_size_input = wx.TextCtrl(panel, value=str(Configuration.get_questions_size()), validator=NumericValidator())
        self.questions_size_input.SetHint(str(Configuration.get_questions_size()))
        grid_sizer.Add(self.questions_size_input, 1, wx.EXPAND)

        # Text control per "dimensione immagini"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione immagini:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.images_size_input = wx.TextCtrl(panel, value=str(Configuration.get_images_size()), validator=NumericValidator())
        self.images_size_input.SetHint(str(Configuration.get_images_size()))
        grid_sizer.Add(self.images_size_input, 1, wx.EXPAND)

        # Text control per "Numero di colonne della sezione"
        grid_sizer.Add(wx.StaticText(panel, label="Numero di colonne della sezione:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.columns_number_input = wx.TextCtrl(panel, value=str(Configuration.get_columns_number()), validator=NumericValidator())
        self.columns_number_input.SetHint(str(Configuration.get_columns_number()))
        grid_sizer.Add(self.columns_number_input, 1, wx.EXPAND)

        # Text control per "Dimensione margine sinistro"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione margine sinistro:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.left_margin_input = wx.TextCtrl(panel, value=str(Configuration.get_left_margin()), validator=NumericValidator())
        self.left_margin_input.SetHint(str(Configuration.get_left_margin()))
        grid_sizer.Add(self.left_margin_input, 1, wx.EXPAND)

        # Text control per "Dimensione margine destro"
        grid_sizer.Add(wx.StaticText(panel, label="Dimensione margine destro:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.right_margin_input = wx.TextCtrl(panel, value=str(Configuration.get_right_margin()), validator=NumericValidator())
        self.right_margin_input.SetHint(str(Configuration.get_right_margin()))
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