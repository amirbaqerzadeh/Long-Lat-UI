import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog
from PyQt6.QtGui import QPixmap

class FileDialogDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        self.btn = QPushButton("QFileDialog static method demo")
        self.btn.clicked.connect(self.get_file)
        layout.addWidget(self.btn)
        
        self.le = QLabel("Hello")
        layout.addWidget(self.le)
        
        self.btn1 = QPushButton("QFileDialog object")
        self.btn1.clicked.connect(self.get_files)
        layout.addWidget(self.btn1)
        
        self.contents = QTextEdit()
        layout.addWidget(self.contents)
        self.setLayout(layout)
        self.setWindowTitle("File Dialog demo")
        
    def get_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 
                                               'c:\\', "Image files (*.jpg *.gif)")
        if fname:
            self.le.setPixmap(QPixmap(fname))
        
    def get_files(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        dlg.setNameFilter("Text files (*.txt)")
        filenames, _ = dlg.getOpenFileNames()
        
        if filenames:
            with open(filenames[0], 'r') as f:
                data = f.read()
                self.contents.setPlainText(data)

def main():
    app = QApplication(sys.argv)
    ex = FileDialogDemo()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
