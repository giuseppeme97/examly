from docx import Document
from docx.document import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, ns
from docx.shared import Pt, RGBColor, Cm
import docx
from docx.shared import Inches


class Word():
    def __init__(self, config: dict, questions: list, document_number: int, is_document_solution: bool) -> None:
        self.config = config
        self.questions = questions
        self.document_number = document_number
        self.is_document_solution = is_document_solution
        self.doc = Document()
        self.set_config()


    def set_config(self) -> None:
        self.set_font(self.config["word"]["font"])
        self.set_language(self.config["word"]["language"])
        self.set_margin(self.config["word"]["left_margin"], self.config["word"]["right_margin"])
        self.set_header(self.config["document_header"])                
        self.set_title(self.config["document_title"], self.config["word"]["title_size"], self.config["are_documents_numbered"], self.document_number)    
        if self.config["are_pages_numbered"]: self.set_number_page()                
        self.set_columns(self.config["word"]["columns_number"])
        self.write_questions(self.config["word"]["font"], self.config["word"]["questions_size"], self.questions, self.config["are_questions_numbered"], self.config["word"]["images_size"])
    

    def set_font(self, font: str) -> None:
        self.doc.styles['Normal'].font.name = font


    def set_language(self, language: str) -> None:
        self.doc.styles.element.xpath('./w:docDefaults/w:rPrDefault/w:rPr')[0].xpath('w:lang')[0].set(docx.oxml.shared.qn('w:val'), language)


    def set_title(self, document_title: str, title_size: int, is_document_numbered: bool, document_number: int) -> None:
        paragraph = self.doc.add_paragraph(document_title + f" - #{document_number}") if is_document_numbered else self.doc.add_paragraph(document_title)
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(title_size)
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER


    def set_margin(self, left_margin: int, right_margin: int) -> None:
        self.doc.sections[0].left_margin = Cm(left_margin)
        self.doc.sections[0].right_margin = Cm(right_margin)


    def set_number_page(self) -> None:
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(ns.qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.set(ns.qn('xml:space'), 'preserve')
        instrText.text = "PAGE"
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(ns.qn('w:fldCharType'), 'end')
        self.doc.sections[0].footer.paragraphs[0].add_run()._r.append(fldChar1)
        self.doc.sections[0].footer.paragraphs[0].add_run()._r.append(instrText)
        self.doc.sections[0].footer.paragraphs[0].add_run()._r.append(fldChar2)


    def set_header(self, document_header: str) -> None:
        self.doc.sections[0].header.paragraphs[0].text = document_header


    def set_columns(self, columns_number: int) -> None:
        self.doc.add_section(WD_SECTION.CONTINUOUS)
        self.doc.sections[1]._sectPr.xpath('./w:cols')[0].set(qn('w:num'), str(columns_number))


    def add_question_header(self, font: str, question_size: int, question_header: str, quesion_image: str, question_image_size: float) -> None: 
        text_header = f"{question_header}\n" if quesion_image else f"{question_header}"
        header = self.doc.add_heading(text_header, 3)
        if quesion_image:
            run_i = header.add_run()
            run_i.add_picture(quesion_image, width=Inches(question_image_size))

        for run in header.runs:
            run.font.color.rgb = RGBColor(0, 0, 0)
            run.bold = True
            run.font.name = font
            run.font.size = Pt(question_size)
        
        if not quesion_image:
            header.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY


    def add_question_option(self, option: dict) -> None:
        paragraph = self.doc.add_paragraph(option['text'], style='List Bullet')
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        if self.is_document_solution:
            for run in paragraph.runs:
                run.bold = option["correct"]
                run.underline = option["correct"]
        

    def write_questions(self, font: str, questions_size: int, questions: list, are_questions_numbered: bool, question_image_size: float) -> None:
        for index, question in enumerate(questions):
            question_header = (f"{index + 1}) " if are_questions_numbered else "") + question['question']
            question_image = question['image']
            
            self.add_question_header(font, questions_size, question_header, question_image, question_image_size)
            for option in question['options']:
                self.add_question_option(option)

                
    def save_document(self, document_path: str, document_filename: str, document_number: int) -> None: 
        suffix = "_solutions" if self.is_document_solution else ""
        self.doc.save(f"{document_path}/{document_filename}_{str(document_number)}{suffix}.docx")    


