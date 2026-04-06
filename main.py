from PIL import Image
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit,
                             QFileDialog)
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):#Класс окна
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Приложение")
        self.setGeometry(400, 400, 1300, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.label = QLabel("Ваша картинка:")
        self.label.setMaximumHeight(35)
        self.label.setAlignment(Qt.AlignCenter)
        

        self.file_btn = QPushButton("Выберите картинку")
        self.file_btn.setMinimumHeight(38)

        self.pic = QLabel()
        self.pic.setMinimumSize(200, 200)
        self.pic.setAlignment(Qt.AlignCenter)
        
        self.cross = QLabel("""---------------------->
<----------------------""", alignment=Qt.AlignCenter)
        self.cross.setMaximumHeight(50)

        self.submit_button = QPushButton("Перевести в ascii")
        self.submit_button.setMinimumHeight(38)
        

        self.OUTLabel = QLabel("Ваш ascii арт:")
        self.OUTLabel.setMaximumHeight(35)
        self.OUTLabel.setAlignment(Qt.AlignCenter)
        

        self.text_area = QTextEdit()
        self.text_area.setLineWrapMode(QTextEdit.NoWrap)
        self.text_area.setFontFamily("Courier New")
        self.text_area.setPlaceholderText("Результат появится здесь...")
        self.text_area.setMinimumSize(400, 400)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.file_btn)
        input_layout.addWidget(self.pic, 1)

        central_layout = QVBoxLayout()
        central_layout.addStretch()
        central_layout.addWidget(self.cross)
        central_layout.addWidget(self.submit_button)
        central_layout.addStretch()  

        output_layout = QVBoxLayout()
        output_layout.addWidget(self.OUTLabel)
        output_layout.addWidget(self.text_area, 1)

        main_layout.addLayout(input_layout, 1)
        main_layout.addLayout(central_layout, 0)
        main_layout.addLayout(output_layout, 1)

        self.file_btn.clicked.connect(self.open_file_dialog)
        self.submit_button.clicked.connect(self.pic_to_ascii)
        
        self.original_pixmap = None
        self.file_path = None

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #000000;
                color: white;
                border-radius: 13px;
                padding: 8px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #595858;
                border: 2px solid black;
                border-radius: 7px;
            }
            QLabel {
                color: #000000;
                border-radius: 13px;
                padding: 8px;
                font-size: 18px;
                font: bold;
            }
            QTextEdit{
                font-size: 8px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)

    def open_file_dialog(self):#открытие файла
        self.file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Картинки (*.png *.jpg *.jpeg *.bmp);;Все файлы (*.*)"
        )
        if self.file_path:
            self.original_pixmap = QPixmap(self.file_path)
            self.update_pic_size()

    def update_pic_size(self):#Функция обновления размера превью
        if self.original_pixmap and not self.original_pixmap.isNull():
            pic_size = self.pic.size()
            if pic_size.width() > 0 and pic_size.height() > 0:
                scaled_pix = self.original_pixmap.scaled(
                    pic_size.width(),
                    pic_size.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.pic.setPixmap(scaled_pix)

    def resizeEvent(self, event: QResizeEvent):#привязка к изменению размера окна
        super().resizeEvent(event)
        self.update_pic_size()

    def pic_to_ascii(self):#перевод картинки в ascii
        gradient = "@$s*^-' "#палитра цветов на 8 оттенков (пока только так, в будующем увеличу кол-во оттенков)
        if self.file_path:
            img = Image.open(self.file_path)
            img = img.convert('L')#картинка в ЧБ
            max_size = 50
            scale = max(img.size) / max_size
            if scale > 1:#изменение разрешения
                new_size = (int(img.width / scale), int(img.height / scale))
                img = img.resize(new_size)

            pixels = img.load()
            ascii_pic = ""
            for y in range(img.height):#перебор цветов и подбор символа под оттенок
                for x in range(img.width):
                    color = pixels[x, y]
                    ascii_pic += gradient[color // 32] * 2
                ascii_pic += "\n"

            self.text_area.setText(ascii_pic)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()