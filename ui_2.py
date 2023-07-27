import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QVBoxLayout, QWidget, QFileDialog)
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
from folium.plugins import MarkerCluster
import pandas as pd


def df_creator(excel_file):
    df = pd.read_excel(excel_file)
    return df


def show_on_map(excel_file):
    df = df_creator(excel_file)

    center_lat, center_lon = df.iloc[0]['Latitude'], df.iloc[0]['Longitude']
    map_center = [center_lat, center_lon]
    mymap = folium.Map(location=map_center, zoom_start=6)

    marker_cluster = MarkerCluster().add_to(mymap)

    for index, row in df.iterrows():
        lat, lon = row['Latitude'], row['Longitude']
        popup_text = f"Latitude: {lat}, Longitude: {lon}"
        folium.Marker(location=[lat, lon], popup=popup_text).add_to(marker_cluster)

    return mymap


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Map Viewer")

        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        # Create a QPushButton instance for file upload
        self.upload_button = QPushButton('Upload Excel File')
        self.upload_button.clicked.connect(self.open_file)

        # Create a QPushButton instance to create the map
        self.create_map_button = QPushButton('Create Map')
        self.create_map_button.clicked.connect(self.create_map)

        # Create a QWebEngineView instance for map display
        self.web_view = QWebEngineView()

        # Add widgets to the layout
        layout.addWidget(self.upload_button)
        layout.addWidget(self.create_map_button)
        layout.addWidget(self.web_view)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Variable to hold the current excel file name
        self.current_excel_file = None

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                "Excel Files (*.xlsx);;All Files (*)", options=QFileDialog.Option.ReadOnly)
        if file_name:
            self.current_excel_file = file_name





    def create_map(self):
        if self.current_excel_file:
            mymap = show_on_map(self.current_excel_file)
            mymap.save("temp.html")
            self.web_view.load(QUrl.fromLocalFile("temp.html"))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
