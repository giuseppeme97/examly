from core.word import Word

class Exam():
    def __init__(self, questions, exam_number, document_title, document_header, number_on_document, number_on_questions, number_of_options, destination_path, file_name, has_corrector) -> None:
        self.questions = questions
        self.exam_number = exam_number
        self.document_title = document_title
        self.document_header = document_header
        self.number_on_document = number_on_document
        self.number_on_questions = number_on_questions
        self.number_of_options = number_of_options
        self.destination_path = destination_path
        self.file_name = file_name
        self.has_corrector = has_corrector


    def _write_word(self, is_corrector: bool) -> None:
        Word(
            self.document_title,
            self.document_header,
            self.number_on_document,
            self.exam_number,
            self.questions,
            self.number_on_questions,
            is_corrector,
            self.number_of_options,
            self.destination_path,
            self.file_name
        )        


    def write(self) -> None:
        self._write_word(is_corrector=False)
        
        if self.has_corrector:
            self._write_word(is_corrector=True)


            

    