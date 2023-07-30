from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os
import webbrowser
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog

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


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("coordinates on map")
        Form.setFixedSize(381, 334)
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(130, 130, 119, 58))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.upload_button = QtWidgets.QPushButton(parent=self.widget)
        self.upload_button.setObjectName("upload_button")
        self.verticalLayout.addWidget(self.upload_button)

        self.load_map_button = QtWidgets.QPushButton(parent=self.widget)
        self.load_map_button.setObjectName("load_map_button")
        self.verticalLayout.addWidget(self.load_map_button)

        self.retranslateUi(Form)
        self.upload_button.clicked.connect(self.handle_upload_button)
        self.load_map_button.clicked.connect(self.handle_load_map_button)

    def handle_upload_button(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                "Excel Files (*.xlsx);;All Files (*)", options=QFileDialog.Option.ReadOnly)
        if file_name:
            df = df_creator(file_name)
            self.df = df
            print("Excel file uploaded successfully.")

    def handle_load_map_button(self):
        if hasattr(self, 'df') and not self.df.empty:
            mymap = show_on_map(self.df)
            # Open the map in the browser
            tmp_map_path = "temp_map.html"
            mymap.save(tmp_map_path)
            webbrowser.open(f"file://{os.path.abspath(tmp_map_path)}")
            print("Map loaded successfully.")
        else:
            print("No data to display. Please upload an Excel file first.")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("coordinates on map", "Coordinates on Map"))
        self.upload_button.setText(_translate("coordinates on map", "Upload Excel File"))
        self.load_map_button.setText(_translate("coordinates on map", "Load the Map"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
