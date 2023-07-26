import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import folium
import pandas as pd
import io
import base64


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Map Viewer")

        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        # Create a QPushButton instance for file upload
        self.button = QPushButton('Upload Excel File')
        self.button.clicked.connect(self.open_file)

        # Create a QWebEngineView instance for map display
        self.web_view = QWebEngineView()

        # Add widgets to the layout
        layout.addWidget(self.button)
        layout.addWidget(self.web_view)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            self.show_on_map(file_name)

    def show_on_map(self, excel_file):
        df = pd.read_excel(excel_file)

        center_lat, center_lon = df.iloc[0]['Latitude'], df.iloc[0]['Longitude']
        map_center = [center_lat, center_lon]
        mymap = folium.Map(location=map_center, zoom_start=6)

        for index, row in df.iterrows():
            lat, lon = row['Latitude'], row['Longitude']
            popup_text = f"Latitude: {lat}, Longitude: {lon}"
            folium.Marker(location=[lat, lon], popup=popup_text).add_to(mymap)

        # Save it to temp.html
        mymap.save("temp.html")

        # Load temp.html to the QWebEngineView
        self.web_view.load(QUrl.fromLocalFile("temp.html"))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
