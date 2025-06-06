import json
import wx


class Configuration:
    # app = wx.App(False)
    # font_enum = wx.FontEnumerator()
    # font_enum.EnumerateFacenames()

    # ------------------------------- #

    default_app_name = "Examly"
    # TODO: rendere riservati i dati
    default_server = "mongodb://admin:password@localhost:27017/"
    default_db = "examly"
    default_fonts_list = ["Liberation Sans", "Liberation Serif"]
    default_languages_list = ["it-IT", "en-EN"]
    default_excel_formats_supported = [".xlsx", ".xls"]
    default_table_formats_supported = [".csv"]
    default_template_filename = "template.xlsx"
    default_include_denomination = "INCLUDERE"
    default_question_denomination = "DOMANDA"
    default_image_denomination = "IMMAGINE"
    default_solution_denomination = "CORRETTA"
    default_option_denomination = "OPZIONE"
    default_include_accept_denomination = "SI"
    default_document_header = "Cognome e Nome: ________________________________________________________"

    # ------------------------------- #

    web_mode = None
    source_file = None
    source_collection = None
    documents_directory = None
    images_directory = None
    template_directory = None

    # ------------------------------- #

    document_filename = None
    zip_filename = None
    filters = {}
    document_title = None
    document_subtitle = None
    documents_number = None
    start_number = None
    questions_number = None
    is_header_included = None
    is_subtitle_included = None
    are_pages_numbered = None
    are_documents_numbered = None
    are_questions_numbered = None
    are_questions_shuffled = None
    are_options_shuffled = None
    are_images_inserted = None
    are_solutions_exported = None
    are_raw_exported = None
    are_questions_single_included = None
    are_documents_included_to_zip = None
    exact_document_number = None
    font = None
    language = None
    title_size = None
    subtitle_size = None
    questions_size = None
    images_size = None
    columns_number = None
    left_margin = None
    right_margin = None

    # ------------------------------- #

    @classmethod
    def set_app_name(cls, value):
        cls.default_app_name = value

    @classmethod
    def get_app_name(cls):
        return cls.default_app_name

    @classmethod
    def set_is_web_mode(cls, value):
        cls.web_mode = value

    @classmethod
    def get_is_web_mode(cls):
        return cls.web_mode

    @classmethod
    def set_source_file(cls, value):
        cls.source_file = value

    @classmethod
    def get_source_file(cls):
        return cls.source_file

    @classmethod
    def set_server(cls, value):
        cls.default_server = value

    @classmethod
    def get_server(cls):
        return cls.default_server

    @classmethod
    def set_db(cls, value):
        cls.default_db = value

    @classmethod
    def get_db(cls):
        return cls.default_db

    @classmethod
    def set_source_collection(cls, value):
        cls.source_collection = value

    @classmethod
    def get_source_collection(cls):
        return cls.source_collection

    @classmethod
    def set_documents_directory(cls, value):
        cls.documents_directory = value

    @classmethod
    def get_documents_directory(cls):
        return cls.documents_directory

    @classmethod
    def set_images_directory(cls, value):
        cls.images_directory = value

    @classmethod
    def get_images_directory(cls):
        return cls.images_directory

    @classmethod
    def set_template_directory(cls, value):
        cls.template_directory = value

    @classmethod
    def get_template_directory(cls):
        return cls.template_directory

    @classmethod
    def set_template_filename(cls, value):
        cls.default_template_filename = value

    @classmethod
    def get_template_filename(cls):
        return cls.default_template_filename

    @classmethod
    def set_document_filename(cls, value):
        cls.document_filename = value

    @classmethod
    def get_document_filename(cls):
        return cls.document_filename

    @classmethod
    def set_zip_filename(cls, value):
        cls.zip_filename = value

    @classmethod
    def get_zip_filename(cls):
        return cls.zip_filename

    @classmethod
    def set_filter_values(cls, filter, values):
        cls.filters[filter] = values

    @classmethod
    def get_filter_values(cls, filter):
        return cls.filters[filter]

    @classmethod
    def set_document_title(cls, value):
        cls.document_title = value

    @classmethod
    def get_document_title(cls):
        return cls.document_title

    @classmethod
    def set_document_subtitle(cls, value):
        cls.document_subtitle = value

    @classmethod
    def get_document_subtitle(cls):
        return cls.document_subtitle

    @classmethod
    def set_document_header(cls, value):
        cls.default_document_header = value

    @classmethod
    def get_document_header(cls):
        return cls.default_document_header

    @classmethod
    def set_documents_number(cls, value):
        cls.documents_number = value

    @classmethod
    def get_documents_number(cls):
        return cls.documents_number

    @classmethod
    def set_start_number(cls, value):
        cls.start_number = value

    @classmethod
    def get_start_number(cls):
        return cls.start_number

    @classmethod
    def set_questions_number(cls, value):
        cls.questions_number = value

    @classmethod
    def get_questions_number(cls):
        return cls.questions_number

    @classmethod
    def set_is_header_included(cls, value):
        cls.is_header_included = value

    @classmethod
    def get_is_header_included(cls):
        return cls.is_header_included

    @classmethod
    def set_is_subtitle_included(cls, value):
        cls.is_subtitle_included = value

    @classmethod
    def get_is_subtitle_included(cls):
        return cls.is_subtitle_included

    @classmethod
    def set_are_pages_numbered(cls, value):
        cls.are_pages_numbered = value

    @classmethod
    def get_are_pages_numbered(cls):
        return cls.are_pages_numbered

    @classmethod
    def set_are_documents_numbered(cls, value):
        cls.are_documents_numbered = value

    @classmethod
    def get_are_documents_numbered(cls):
        return cls.are_documents_numbered

    @classmethod
    def set_are_questions_numbered(cls, value):
        cls.are_questions_numbered = value

    @classmethod
    def get_are_questions_numbered(cls):
        return cls.are_questions_numbered

    @classmethod
    def set_are_questions_shuffled(cls, value):
        cls.are_questions_shuffled = value

    @classmethod
    def get_are_questions_shuffled(cls):
        return cls.are_questions_shuffled

    @classmethod
    def set_are_options_shuffled(cls, value):
        cls.are_options_shuffled = value

    @classmethod
    def get_are_options_shuffled(cls):
        return cls.are_options_shuffled

    @classmethod
    def set_are_images_inserted(cls, value):
        cls.are_images_inserted = value

    @classmethod
    def get_are_images_inserted(cls):
        return cls.are_images_inserted

    @classmethod
    def set_are_solutions_exported(cls, value):
        cls.are_solutions_exported = value

    @classmethod
    def get_are_solutions_exported(cls):
        return cls.are_solutions_exported

    @classmethod
    def set_are_raw_exported(cls, value):
        cls.are_raw_exported = value

    @classmethod
    def get_are_raw_exported(cls):
        return cls.are_raw_exported

    @classmethod
    def set_are_questions_single_included(cls, value):
        cls.are_questions_single_included = value

    @classmethod
    def get_are_questions_single_included(cls):
        return cls.are_questions_single_included

    @classmethod
    def set_are_documents_included_to_zip(cls, value):
        cls.are_documents_included_to_zip = value

    @classmethod
    def get_are_documents_included_to_zip(cls):
        return cls.are_documents_included_to_zip

    @classmethod
    def set_exact_document_number(cls, value):
        cls.exact_document_number = value

    @classmethod
    def get_exact_document_number(cls):
        return cls.exact_document_number

    @classmethod
    def get_excel_formats_supported(cls):
        return cls.default_excel_formats_supported

    @classmethod
    def get_table_formats_supported(cls):
        return cls.default_table_formats_supported

    @classmethod
    def set_include_denomination(cls, value):
        cls.default_include_denomination = value

    @classmethod
    def get_include_denomination(cls):
        return cls.default_include_denomination

    @classmethod
    def set_question_denomination(cls, value):
        cls.default_question_denomination = value

    @classmethod
    def get_question_denomination(cls):
        return cls.default_question_denomination

    @classmethod
    def set_image_denomination(cls, value):
        cls.default_image_denomination = value

    @classmethod
    def get_image_denomination(cls):
        return cls.default_image_denomination

    @classmethod
    def set_solution_denomination(cls, value):
        cls.default_solution_denomination = value

    @classmethod
    def get_solution_denomination(cls):
        return cls.default_solution_denomination

    @classmethod
    def set_option_denomination(cls, value):
        cls.default_option_denomination = value

    @classmethod
    def get_option_denomination(cls):
        return cls.default_option_denomination

    @classmethod
    def set_include_accept_denomination(cls, value):
        cls.default_include_accept_denomination = value

    @classmethod
    def get_include_accept_denomination(cls):
        return cls.default_include_accept_denomination

    @classmethod
    def set_font(cls, value):
        cls.font = value

    @classmethod
    def get_font(cls):
        return cls.font

    @classmethod
    def set_language(cls, value):
        cls.language = value

    @classmethod
    def get_language(cls):
        return cls.language

    @classmethod
    def set_title_size(cls, value):
        cls.title_size = int(value)

    @classmethod
    def get_title_size(cls):
        return cls.title_size

    @classmethod
    def set_subtitle_size(cls, value):
        cls.subtitle_size = int(value)

    @classmethod
    def get_subtitle_size(cls):
        return cls.subtitle_size

    @classmethod
    def set_questions_size(cls, value):
        cls.questions_size = int(value)

    @classmethod
    def get_questions_size(cls):
        return cls.questions_size

    @classmethod
    def set_images_size(cls, value):
        cls.images_size = float(value)

    @classmethod
    def get_images_size(cls):
        return cls.images_size

    @classmethod
    def set_columns_number(cls, value):
        cls.columns_number = int(value)

    @classmethod
    def get_columns_number(cls):
        return cls.columns_number

    @classmethod
    def set_left_margin(cls, value):
        cls.left_margin = int(value)

    @classmethod
    def get_left_margin(cls):
        return cls.left_margin

    @classmethod
    def set_right_margin(cls, value):
        cls.right_margin = int(value)

    @classmethod
    def get_right_margin(cls):
        return cls.right_margin

    @classmethod
    def get_control_options(cls):
        return {
            Configuration.get_is_header_included.__name__.removeprefix("get_"): {
                "label": "Inserisci cognome nome",
                "reference": None,
                "default": Configuration.get_is_header_included(),
                "disabled": False
            },
            Configuration.get_is_subtitle_included.__name__.removeprefix("get_"): {
                "label": "Inserisci sottotitolo",
                "reference": None,
                "default": Configuration.get_is_subtitle_included(),
                "disabled": False
            },
            Configuration.get_are_pages_numbered.__name__.removeprefix("get_"): {
                "label": "Inserisci numero di pagina",
                "reference": None,
                "default": Configuration.get_are_pages_numbered(),
                "disabled": False
            },
            Configuration.get_are_documents_numbered.__name__.removeprefix("get_"): {
                "label": "Numera documenti",
                "reference": None,
                "default": Configuration.get_are_documents_numbered(),
                "disabled": False
            },
            Configuration.get_are_questions_numbered.__name__.removeprefix("get_"): {
                "label": "Numera domande",
                "reference": None,
                "default": Configuration.get_are_questions_numbered(),
                "disabled": False
            },
            Configuration.get_are_questions_shuffled.__name__.removeprefix("get_"): {
                "label": "Mescola domande",
                "reference": None,
                "default": Configuration.get_are_questions_shuffled(),
                "disabled": False
            },
            Configuration.get_are_options_shuffled.__name__.removeprefix("get_"): {
                "label": "Mescola risposte",
                "reference": None,
                "default": Configuration.get_are_options_shuffled(),
                "disabled": False
            },
            Configuration.get_are_images_inserted.__name__.removeprefix("get_"): {
                "label": "Inserisci immagini domande",
                "reference": None,
                "default": Configuration.get_are_images_inserted(),
                "disabled": False
            },
            Configuration.get_are_questions_single_included.__name__.removeprefix("get_"): {
                "label": "Includi domande singolarmente",
                "reference": None,
                "default": Configuration.get_are_questions_single_included(),
                "disabled": False
            },
            Configuration.get_are_solutions_exported.__name__.removeprefix("get_"): {
                "label": "Esporta soluzioni",
                "reference": None,
                "default": Configuration.get_are_solutions_exported(),
                "disabled": False
            },
            Configuration.get_are_raw_exported.__name__.removeprefix("get_"): {
                "label": "Esporta RAW",
                "reference": None,
                "default": Configuration.get_are_raw_exported(),
                "disabled": False
            },
            Configuration.get_are_documents_included_to_zip.__name__.removeprefix("get_"): {
                "label": "Esporta in ZIP",
                "reference": None,
                "default": Configuration.get_are_documents_included_to_zip(),
                "disabled": False
            }
        }

    @classmethod
    def get_selection_lists(cls):
        return cls.default_fonts_list, cls.default_languages_list

    @classmethod
    def export_config(cls, file_path):
        attributi = {k: v for k, v in cls.__dict__.items(
        ) if not k.startswith("__") and not callable(v)}

        with open(file_path, "w") as file:
            json.dump(attributi, file, indent=4)
        print(f"Configurazione esportata con successo in {file_path}")

    @classmethod
    def import_config(cls, file_path):
        try:
            with open(file_path, "r") as file:
                dati = json.load(file)

                for chiave, valore in dati.items():
                    if hasattr(cls, chiave):
                        setattr(cls, chiave, valore)
            print(f"Dati importati con successo da {file_path}")
        except FileNotFoundError:
            print(f"Errore: il file {file_path} non è stato trovato.")
        except json.JSONDecodeError:
            print(f"Errore: il file {file_path} non contiene un JSON valido.")
