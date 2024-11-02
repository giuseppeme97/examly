import json

class Configuration:
    app_name = "Examly"
    working_path = "/Users/giuseppe/Documents/examly"
    soffice_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    source_file = "/Users/giuseppe/Documents/examly/Domande.xlsx"
    session_file = "/Users/giuseppe/Documents/examly/sessione.json"
    documents_directory = "/Users/giuseppe/Documents/examly/output"
    images_directory = "/Users/giuseppe/Documents/examly/images"
    template_directory = "/Users/giuseppe/Documents/examly/template"
    template_filename = "template.xlsx"
    document_filename = "esame"
    zip_filename = "compito"
    subjects = ["INFORMATICA"]
    classrooms = [4]
    periods = [1]
    sectors = []
    document_title = "Prova comune di Informatica - A.S. 2024/2025 - Classi 3F 3G 3H 3I"
    document_header = "Cognome e Nome: ________________________________________________________"
    documents_number = 1
    questions_number = 20
    from_session = False
    are_pages_numbered = True
    are_documents_numbered = True
    are_questions_numbered = True
    are_questions_shuffled = True
    are_options_shuffled = True
    are_solutions_exported = True
    are_questions_single_included = True
    are_documents_exported_to_pdf = False
    are_documents_included_to_zip = False
    export_session = False
    exact_document_number = None
    excel_formats_supported = [".xlsx", ".xls"]
    table_formats_supported = [".csv"]
    subject_denomination = "MATERIA"
    classroom_denomination = "CLASSE"
    period_denomination = "PERIODO"
    sector_denomination = "SETTORE"
    include_denomination = "INCLUDERE"
    question_denomination = "DOMANDA"
    image_denomination = "IMMAGINE"
    solution_denomination = "CORRETTA"
    option_denomination = "OPZIONE"
    include_accept_denomination = "SI"
    font = "Liberation Sans"
    language  = "it-IT"
    title_size = 15
    questions_size = 11
    images_size = 3.5
    questions_distance = 5
    questions_RGB_color = [0, 0, 0]
    columns_number = 2
    left_margin = 1
    right_margin = 1
    DSA = False

    @classmethod
    def set_app_name(cls, value):
        cls.app_name = value

    @classmethod
    def get_app_name(cls):
        return cls.app_name

    @classmethod
    def set_working_path(cls, value):
        cls.working_path = value

    @classmethod
    def get_working_path(cls):
        return cls.working_path

    @classmethod
    def set_soffice_path(cls, value):
        cls.soffice_path = value

    @classmethod
    def get_soffice_path(cls):
        return cls.soffice_path

    @classmethod
    def set_source_file(cls, value):
        cls.source_file = value

    @classmethod
    def get_source_file(cls):
        return cls.source_file

    @classmethod
    def set_session_file(cls, value):
        cls.session_file = value

    @classmethod
    def get_session_file(cls):
        return cls.session_file

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
        cls.template_filename = value

    @classmethod
    def get_template_filename(cls):
        return cls.template_filename

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
    def set_subjects(cls, value):
        cls.subjects = value

    @classmethod
    def get_subjects(cls):
        return cls.subjects

    @classmethod
    def set_classrooms(cls, value):
        cls.classrooms = [int(classroom) for classroom in value]

    @classmethod
    def get_classrooms(cls):
        return cls.classrooms

    @classmethod
    def set_periods(cls, value):
        cls.periods = [int(period) for period in value]

    @classmethod
    def get_periods(cls):
        return cls.periods

    @classmethod
    def set_sectors(cls, value):
        cls.sectors = value

    @classmethod
    def get_sectors(cls):
        return cls.sectors

    @classmethod
    def set_document_title(cls, value):
        cls.document_title = value

    @classmethod
    def get_document_title(cls):
        return cls.document_title

    @classmethod
    def set_document_header(cls, value):
        cls.document_header = value

    @classmethod
    def get_document_header(cls):
        return cls.document_header

    @classmethod
    def set_documents_number(cls, value):
        cls.documents_number = value

    @classmethod
    def get_documents_number(cls):
        return cls.documents_number

    @classmethod
    def set_questions_number(cls, value):
        cls.questions_number = value

    @classmethod
    def get_questions_number(cls):
        return cls.questions_number

    @classmethod
    def set_from_session(cls, value):
        cls.from_session = value

    @classmethod
    def get_from_session(cls):
        return cls.from_session

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
    def set_are_solutions_exported(cls, value):
        cls.are_solutions_exported = value

    @classmethod
    def get_are_solutions_exported(cls):
        return cls.are_solutions_exported

    @classmethod
    def set_are_questions_single_included(cls, value):
        cls.are_questions_single_included = value

    @classmethod
    def get_are_questions_single_included(cls):
        return cls.are_questions_single_included

    @classmethod
    def set_are_documents_exported_to_pdf(cls, value):
        cls.are_documents_exported_to_pdf = value

    @classmethod
    def get_are_documents_exported_to_pdf(cls):
        return cls.are_documents_exported_to_pdf

    @classmethod
    def set_are_documents_included_to_zip(cls, value):
        cls.are_documents_included_to_zip = value

    @classmethod
    def get_are_documents_included_to_zip(cls):
        return cls.are_documents_included_to_zip

    @classmethod
    def set_export_session(cls, value):
        cls.export_session = value

    @classmethod
    def get_export_session(cls):
        return cls.export_session

    @classmethod
    def set_exact_document_number(cls, value):
        cls.exact_document_number = value

    @classmethod
    def get_exact_document_number(cls):
        return cls.exact_document_number

    @classmethod
    def set_excel_formats_supported(cls, value):
        cls.excel_formats_supported = value

    @classmethod
    def get_excel_formats_supported(cls):
        return cls.excel_formats_supported

    @classmethod
    def set_table_formats_supported(cls, value):
        cls.table_formats_supported = value

    @classmethod
    def get_table_formats_supported(cls):
        return cls.table_formats_supported

    @classmethod
    def set_subject_denomination(cls, value):
        cls.subject_denomination = value

    @classmethod
    def get_subject_denomination(cls):
        return cls.subject_denomination
    
    @classmethod
    def set_classroom_denomination(cls, value):
        cls.classroom_denomination = value

    @classmethod
    def get_classroom_denomination(cls):
        return cls.classroom_denomination

    # period_denomination
    @classmethod
    def set_period_denomination(cls, value):
        cls.period_denomination = value

    @classmethod
    def get_period_denomination(cls):
        return cls.period_denomination

    @classmethod
    def set_sector_denomination(cls, value):
        cls.sector_denomination = value

    @classmethod
    def get_sector_denomination(cls):
        return cls.sector_denomination

    @classmethod
    def set_include_denomination(cls, value):
        cls.include_denomination = value

    @classmethod
    def get_include_denomination(cls):
        return cls.include_denomination

    @classmethod
    def set_question_denomination(cls, value):
        cls.question_denomination = value

    @classmethod
    def get_question_denomination(cls):
        return cls.question_denomination

    @classmethod
    def set_image_denomination(cls, value):
        cls.image_denomination = value

    @classmethod
    def get_image_denomination(cls):
        return cls.image_denomination

    @classmethod
    def set_solution_denomination(cls, value):
        cls.solution_denomination = value

    @classmethod
    def get_solution_denomination(cls):
        return cls.solution_denomination

    @classmethod
    def set_option_denomination(cls, value):
        cls.option_denomination = value

    @classmethod
    def get_option_denomination(cls):
        return cls.option_denomination

    @classmethod
    def set_include_accept_denomination(cls, value):
        cls.include_accept_denomination = value

    @classmethod
    def get_include_accept_denomination(cls):
        return cls.include_accept_denomination

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
        cls.title_size = value

    @classmethod
    def get_title_size(cls):
        return cls.title_size

    @classmethod
    def set_questions_size(cls, value):
        cls.questions_size = value

    @classmethod
    def get_questions_size(cls):
        return cls.questions_size
    
    @classmethod
    def set_images_size(cls, value):
        cls.images_size = value

    @classmethod
    def get_images_size(cls):
        return cls.images_size
    
    @classmethod
    def set_questions_distance(cls, value):
        cls.questions_distance = value

    @classmethod
    def get_questions_distance(cls):
        return cls.questions_distance

    @classmethod
    def set_questions_RGB_color(cls, value):
        cls.questions_RGB_color = value

    @classmethod
    def get_questions_RGB_color(cls):
        return cls.questions_RGB_color

    @classmethod
    def set_columns_number(cls, value):
        cls.columns_number = value

    @classmethod
    def get_columns_number(cls):
        return cls.columns_number

    @classmethod
    def set_left_margin(cls, value):
        cls.left_margin = value

    @classmethod
    def get_left_margin(cls):
        return cls.left_margin

    @classmethod
    def set_right_margin(cls, value):
        cls.right_margin = value

    @classmethod
    def get_right_margin(cls):
        return cls.right_margin
    
    @classmethod
    def get_configs(cls):
        filters = {
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

        control_options = {
            Configuration.get_are_pages_numbered.__name__.removeprefix("get_"): {
                "label": "Inserisci numero di pagina",
                "reference": None,
                "default": Configuration.get_are_pages_numbered()
            },
            Configuration.get_are_documents_numbered.__name__.removeprefix("get_"): {
                "label": "Numera documenti",
                "reference": None,
                "default": Configuration.get_are_documents_numbered()
            },
            Configuration.get_are_questions_numbered.__name__.removeprefix("get_"): {
                "label": "Numera domande",
                "reference": None,
                "default": Configuration.get_are_questions_numbered()
            },
            Configuration.get_are_questions_shuffled.__name__.removeprefix("get_"): {
                "label": "Mescola domande",
                "reference": None,
                "default": Configuration.get_are_questions_shuffled()
            },
            Configuration.get_are_options_shuffled.__name__.removeprefix("get_"): {
                "label": "Mescola risposte",
                "reference": None,
                "default": Configuration.get_are_options_shuffled()
            },
            Configuration.get_are_solutions_exported.__name__.removeprefix("get_"): {
                "label": "Esporta correttori",
                "reference": None,
                "default": Configuration.get_are_solutions_exported()
            },
            Configuration.get_are_questions_single_included.__name__.removeprefix("get_"): {
                "label": "Includi domande singolarmente",
                "reference": None,
                "default": Configuration.get_are_questions_single_included()
            },
            Configuration.get_are_documents_exported_to_pdf.__name__.removeprefix("get_"): {
                "label": "Esporta in PDF",
                "reference": None,
                "default": Configuration.get_are_documents_exported_to_pdf()
            },
            Configuration.get_are_documents_included_to_zip.__name__.removeprefix("get_"): {
                "label": "Esporta in ZIP (beta)",
                "reference": None,
                "default": Configuration.get_are_documents_included_to_zip()
            },
            Configuration.get_export_session.__name__.removeprefix("get_"): {
                "label": "Esporta sessione (non implementata)",
                "reference": None,
                "default": Configuration.get_export_session()
            }
        }



        fonts = [Configuration.get_font(), "Arial", "Courier", "Times New Roman"]
        languages = [Configuration.get_language(), "en-EN"]
        return filters, control_options, fonts, languages

    @classmethod
    def export_config(cls, file_path):
        attributi = {k: v for k, v in cls.__dict__.items() if not k.startswith("__") and not callable(v)}
        
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

