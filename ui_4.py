import os
import sys
import webbrowser

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pandas as pd
import folium
from folium.plugins import MarkerCluster


def create_dataframe(excel_file):
    df = pd.read_excel(excel_file)
    return df


def create_map(excel_file):
    df = create_dataframe(excel_file)
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
        super().__init__()
        self.setWindowTitle("Map Viewer")
        self.setFixedSize(400, 100)
        self.current_excel_file = None
        self.create_layout()
        self.create_widgets()
        self.create_connections()

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

    def create_widgets(self):
        self.upload_button = QPushButton('Upload Excel File')
        self.create_map_button = QPushButton('Create Map')
        self.label = QLabel("github.com/amirbaqerzadeh")

        self.upload_button.setFixedSize(150, 30)
        self.create_map_button.setFixedSize(150, 30)

        self.buttons_layout.addWidget(self.upload_button)
        self.buttons_layout.addWidget(self.create_map_button)

        self.layout.addLayout(self.buttons_layout)
        self.layout.addStretch()
        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignBottom)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def create_connections(self):
        self.upload_button.clicked.connect(self.open_file)
        self.create_map_button.clicked.connect(self.create_map)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                "Excel Files (*.xlsx);;All Files (*)", options=QFileDialog.Option.ReadOnly)
        if file_name:
            self.current_excel_file = file_name

    def create_map(self):
        if self.current_excel_file:
            mymap = create_map(self.current_excel_file)
            output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp.html")
            mymap.save(output_file)
            webbrowser.open(output_file)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())