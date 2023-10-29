import random
import re
import sys

import fitz
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QLabel, QMessageBox, QPushButton,
                             QRadioButton, QVBoxLayout, QWidget)


class PsychometricTest(QWidget):
    def __init__(self, pdf_path):
        super().__init()
        self.current_question = 0
        self.score = 0
        self.questions = self.extract_questions_from_pdf(pdf_path)
        random.shuffle(self.questions)

        self.initUI()

    def extract_questions_from_pdf(self, pdf_path):
        questions = []
        current_question = None

        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()

            for line in text.split('\n'):
                line = line.strip()
                if re.match(r'^\d+\.', line):
                    if current_question:
                        questions.append(current_question)
                    current_question = {"question": line, "answers": []}
                elif current_question:
                    if line:
                        current_question["answers"].append(line)

        # Add the last question if it exists
        if current_question:
            questions.append(current_question)

        # Strip question numbers from the questions
        for question_data in questions:
            question_data["question"] = re.sub(r'^\d+\.', '', question_data["question"]).strip()

        return questions[:45]

    def initUI(self):
        self.setWindowTitle('Psychometric Test')
        self.setGeometry(100, 100, 800, 600)

        self.question_label = QLabel(self)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.question_label)

        self.radio_buttons = []
        for i in range(5):
            rb = QRadioButton(self)
            self.layout.addWidget(rb)
            self.radio_buttons.append(rb)

        self.submit_button = QPushButton('Submit', self)
        self.layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.check_answer)

        self.display_question()

    def display_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question = question_data["question"]
            options = question_data["answers"]
            num_options = len(options)
            self.shuffle_options(options)

            self.question_label.setText(question)

            for i in range(5):
                if i < num_options:
                    self.radio_buttons[i].setText(options[i])
                    self.radio_buttons[i].show()
                else:
                    self.radio_buttons[i].hide()

            self.clear_selection()
        else:
            self.show_result()

    def shuffle_options(self, options):
        random.shuffle(options)

    def clear_selection(self):
        for rb in self.radio_buttons:
            rb.setChecked(False)

    def check_answer(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            selected_answer = None

            for i in range(5):
                if self.radio_buttons[i].isChecked():
                    selected_answer = self.radio_buttons[i].text()
                    break

            if selected_answer:
                if selected_answer in question_data["answers"]:
                    self.score += 1

            self.current_question += 1
            if self.current_question == len(self.questions):
                self.show_result()
            else:
                self.display_question()

    def show_result(self):
        message = f'You scored {self.score} out of {len(self.questions)}!'
        QMessageBox.information(self, 'Psychometric Test Result', message)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pdf_path = r"C:\Users\gokul\Downloads\Psychometric-test-sample-questions-2.pdf"  # Replace with your PDF file path
    test = PsychometricTest(pdf_path)
    test.show()
    sys.exit(app.exec())
