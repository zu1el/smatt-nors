from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from file_helper import *


notes = read_from_file()
app = QApplication([])

window = QWidget()
window.setWindowTitle('Розумні замітки')
window.resize(900, 600)

list_notes = QListWidget()
list_notes.addItems(notes)
list_notes_label = QLabel('Список заміток')

button_note_create = QPushButton('Створити замітку ')
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавити до змітки')
button_tag_del = QPushButton('Відкріпити від змітки')
button_tag_search = QPushButton('Шукати замітку по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
window.setLayout(layout_notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])


def save_note():
    #отримуємо ключ замітки
    key = list_notes.selectedItems()[0].text()
    notes[key]['текст'] = field_text.toPlainText()
    write_in_file(notes)


def new_note():
    note_name, ok = QInputDialog.getText(window,"Створення замітки", "Назва замітки")
    if ok == True:
        notes[note_name] = {
            "текст": "",
            "теги":[]
        }
    list_notes.clear()
    list_notes.addItems(notes)
    write_in_file(notes)


def delete_note():
    key = list_notes.selectedItems()[0].text()
    notes.pop(key)
    list_notes.clear()
    list_notes.addItems(notes)
    write_in_file(notes)

def add_tag():
    note_key = list_notes.selectedItems()[0].text()
    tag_name, ok = QInputDialog.getText(window, "Створення тегу", "Назва тегу")
    if ok == True:
        notes[note_key]["теги"].append(tag_name)
        list_tags.clear()
        list_tags.addItems(notes[note_key]["теги"])
        write_in_file(notes)

def delete_tag():
    note_key = list_notes.selectedItems()[0].text()
    tag_key = list_tags.selectedItems()[0].text()
    notes[note_key]["теги"].remove(tag_key)
    list_tags.clear()
    list_tags.addItems(notes[note_key]["теги"])
    write_in_file(notes)


def search():
    tag_name = field_tag.text()
    filtered_notes = {}
    if tag_name == "":
        list_notes.clear()
        list_notes.addItems(notes)
    else:
        for element in notes:
            if tag_name in notes[element]["теги"]:
                filtered_notes[element] = notes[element]

        list_notes.clear()
        list_notes.addItems(filtered_notes)
button_tag_search.clicked.connect(search)


button_tag_del.clicked.connect(delete_tag)
button_tag_add.clicked.connect(add_tag)
button_note_del.clicked.connect(delete_note)
button_note_create.clicked.connect(new_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
window.show()
app.exec_()
