import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5 import QtCore
from main_window import Ui_Form
from error_window import Ui_widget


class MyException(Exception):
    text = None

    def __init__(self, text):
        super().__init__()
        self.text = text


class ErrorWindow(QWidget, Ui_widget):
    def __init__(self, text):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Ошибка')
        self.error_label.setText(text)


class MainWindow(QWidget, Ui_Form):
    error_window = None
    short_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
                      'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    full_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
                      'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    alphabet_en = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Шифр Виженера')
        self.code_text.clicked.connect(self.code_text_vigenere)
        self.save_code_text.clicked.connect(self.save_code_file)
        self.load_text_for_code.clicked.connect(self.load_code_file)
        self.load_text_for_decode.clicked.connect(self.load_decode_file)
        self.save_decode_text.clicked.connect(self.save_decode_file)
        self.decode_text.clicked.connect(self.decode_text_vigenere)

    @staticmethod
    def next_symbol(alphabet, pointer, count) -> str:
        for x in range(count):
            char = alphabet[pointer]
            if (len(alphabet) - 1) == pointer:
                pointer = 0
            else:
                pointer += 1
            yield char

    @QtCore.pyqtSlot()
    def code_text_vigenere(self) -> None:
        self.code_end.clear()
        text = self.code_start.toPlainText()
        key = self.code_key.text()
        if len(text) == 0:
            self.error_window = ErrorWindow('Текст для кодирования отсутствует.')
            self.error_window.show()
            return
        if len(key) == 0:
            self.error_window = ErrorWindow('Ключ не введён.')
            self.error_window.show()
            return
        left_border_lower = None
        right_border_lower = None
        if self.code_rus.isChecked() or self.code_rus_short.isChecked():
            left_border_lower = 1072
            right_border_lower = 1103
        elif self.code_en.isChecked():
            left_border_lower = 97
            right_border_lower = 122
        counter = 0
        key = key.lower()
        text = text.lower()
        code_text = ''
        alphabets = []
        need_alphabet = None
        if self.code_rus_short.isChecked():
            need_alphabet = self.short_alphabet
        elif self.code_rus.isChecked():
            need_alphabet = self.full_alphabet
        elif self.code_en.isChecked():
            need_alphabet = self.alphabet_en
        for elem in key:
            mydict = {}
            shift = need_alphabet.index(elem)
            for x, next_symbol in enumerate(self.next_symbol(need_alphabet, shift, len(need_alphabet))):
                mydict[need_alphabet[x]] = next_symbol
            alphabets.append(mydict)
        for char in text:
            if ord(char) < left_border_lower or ord(char) > right_border_lower:
                code_text += char
                continue
            code_text += alphabets[counter][char]
            if (len(key) - 1) == counter:
                counter = 0
            else:
                counter += 1
        self.code_end.setText(code_text)

    @QtCore.pyqtSlot()
    def decode_text_vigenere(self) -> None:
        self.decode_end.clear()
        text = self.decode_start.toPlainText()
        key = self.decode_key.text()
        if len(text) == 0:
            self.error_window = ErrorWindow('Текст для декодирования отсутствует.')
            self.error_window.show()
            return
        if len(key) == 0:
            self.error_window = ErrorWindow('Ключ не введён.')
            self.error_window.show()
            return
        left_border_lower = None
        right_border_lower = None
        if self.decode_rus.isChecked() or self.decode_rus_short.isChecked():
            left_border_lower = 1072
            right_border_lower = 1103
        elif self.decode_en.isChecked():
            left_border_lower = 97
            right_border_lower = 122
        counter = 0
        key = key.lower()
        text = text.lower()
        code_text = ''
        alphabets = []
        need_alphabet = None
        if self.decode_rus_short.isChecked():
            need_alphabet = self.short_alphabet
        elif self.decode_rus.isChecked():
            need_alphabet = self.full_alphabet
        elif self.decode_en.isChecked():
            need_alphabet = self.alphabet_en
        for elem in key:
            mydict = {}
            shift = need_alphabet.index(elem)
            for x, next_symbol in enumerate(self.next_symbol(need_alphabet, shift, len(need_alphabet))):
                mydict[need_alphabet[x]] = next_symbol
            mydict = {v: k for k, v in mydict.items()}
            alphabets.append(mydict)
        for char in text:
            if (ord(char) < left_border_lower or ord(char) > right_border_lower) and char != 'ё':
                code_text += char
                continue
            code_text += alphabets[counter][char]
            if (len(key) - 1) == counter:
                counter = 0
            else:
                counter += 1
        self.decode_end.setText(code_text)

    @QtCore.pyqtSlot()
    def load_code_file(self) -> None:
        filegialog = QFileDialog.getOpenFileUrl(self, 'Загрузка',
                                                filter=str("Текстовый файл (*.txt)"))
        if filegialog[0]:
            file_path = filegialog[0].toLocalFile()
            if file_path == '':
                return
            file = open(file_path, 'r')
            text = file.read()
            self.code_start.setText(text)

    @QtCore.pyqtSlot()
    def load_decode_file(self) -> None:
        filegialog = QFileDialog.getOpenFileUrl(self, 'Загрузка',
                                                filter=str("Текстовый файл (*.txt)"))
        if filegialog[0]:
            file_path = filegialog[0].toLocalFile()
            if file_path == '':
                return
            file = open(file_path, 'r')
            text = file.read()
            self.decode_start.setText(text)

    @QtCore.pyqtSlot()
    def save_code_file(self) -> None:
        text = self.code_end.toPlainText()
        if len(text) == 0:
            self.error_window = ErrorWindow('Нет закодированных данных')
            self.error_window.show()
            return
        filegialog = QFileDialog.getSaveFileUrl(self, 'Сохранение',
                                                filter=str("Текстовый файл (*.txt)"))
        if filegialog[0]:
            file_path = filegialog[0].toLocalFile()
            if file_path == '':
                return
            file = open(file_path, 'w')
            file.write(text)

    @QtCore.pyqtSlot()
    def save_decode_file(self) -> None:
        text = self.decode_end.toPlainText()
        if len(text) == 0:
            self.error_window = ErrorWindow('Нет декодированных данных')
            self.error_window.show()
            return
        filegialog = QFileDialog.getSaveFileUrl(self, 'Сохранение',
                                                filter=str("Текстовый файл (*.txt)"))
        if filegialog[0]:
            file_path = filegialog[0].toLocalFile()
            if file_path == '':
                return
            file = open(file_path, 'w')
            file.write(text)


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qapp.exec())
