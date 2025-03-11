import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QTableWidgetItem
import pandas as pd


class EmployeeApp(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("employee.ui", self)  # Load the UI from XML file

        self.df = pd.DataFrame()

        # Connect filter combo box to filtering function
        self.comboBox.currentIndexChanged.connect(self.apply_filter)

        # Connect button to load data
        self.pushButton.clicked.connect(self.load_csv_data)

        # Load CSV Data on startup
        self.load_csv_data()

    def load_csv_data(self):
        try:
            self.df = pd.read_csv("employee.csv", encoding='latin1')
            self.df["Dob"] = pd.to_datetime(self.df["Dob"], dayfirst=True, errors='coerce')
            self.display_data(self.df)  # Load all employees initially
        except Exception as e:
            print(f"Error loading CSV file: {e}")

    def apply_filter(self):
        if self.df.empty:
            return

        choice = self.comboBox.currentText()
        if choice == "All Employees":
            self.display_data(self.df)
        elif choice == "Employees born in 2001":
            filtered_df = self.df[self.df["Dob"].dt.year == 2001]
            self.display_data(filtered_df)
        elif choice == "Top 3 Oldest Employees":
            filtered_df = self.df.sort_values(by="Dob", ascending=True).head(3)
            self.display_data(filtered_df)
        elif choice == "Exclude Testers":
            filtered_df = self.df[self.df["Role"] != "Tester"]
            self.display_data(filtered_df)
        elif choice == "Count Employees by Role":
            role_counts = self.df["Role"].value_counts().reset_index()
            role_counts.columns = ["Role", "Count"]
            self.display_data(role_counts)

    def display_data(self, data):
        self.tableWidget.setRowCount(data.shape[0])
        self.tableWidget.setColumnCount(data.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(data.columns)

        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(data.iloc[row, col])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmployeeApp()
    window.show()
    sys.exit(app.exec())