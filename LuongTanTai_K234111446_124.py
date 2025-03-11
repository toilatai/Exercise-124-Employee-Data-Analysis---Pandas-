import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, \
    QComboBox
import pandas as pd

# Employee Data
data = {
    "Id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Name": [
        "Tuan Kiet", "Khánh Hưng", "Gia Hân", "Ngọc Tú", "Lê Minh",
        "Trần Bảo", "Hoàng Vũ", "Phương Linh", "Bảo Ngọc", "Hải Đăng"
    ],
    "Dob": ["12/2/2000", "22/04/2003", "6/8/2002", "2/2/2001", "5/5/1999",
            "10/10/2001", "7/7/1998", "1/1/2000", "15/3/1997", "9/9/1996"],
    "Role": [
        "Web Developer", "Tester", "Business Analyst", "Mobile App Developer", "Data Scientist",
        "Software Engineer", "Tester", "Project Manager", "HR Manager", "Web Developer"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)
df["Dob"] = pd.to_datetime(df["Dob"], dayfirst=True)


def load_data(table_widget, data_frame):
    table_widget.setRowCount(data_frame.shape[0])
    table_widget.setColumnCount(data_frame.shape[1])
    table_widget.setHorizontalHeaderLabels(data_frame.columns)

    for row in range(data_frame.shape[0]):
        for col in range(data_frame.shape[1]):
            table_widget.setItem(row, col, QTableWidgetItem(str(data_frame.iloc[row, col])))


class EmployeeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee List")
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.filter_box = QComboBox()
        self.filter_box.addItems(["All Employees", "Born in 2001", "Top 3 Oldest", "Exclude Testers", "Count by Role"])
        self.filter_box.currentIndexChanged.connect(self.apply_filter)
        layout.addWidget(self.filter_box)

        self.load_button = QPushButton("Load Employee Data")
        self.load_button.clicked.connect(lambda: load_data(self.table_widget, df))
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    def apply_filter(self):
        filter_type = self.filter_box.currentText()

        if filter_type == "All Employees":
            load_data(self.table_widget, df)
        elif filter_type == "Born in 2001":
            filtered_df = df[df["Dob"].dt.year == 2001]
            load_data(self.table_widget, filtered_df)
        elif filter_type == "Top 3 Oldest":
            filtered_df = df.sort_values(by="Dob", ascending=True).head(3)
            load_data(self.table_widget, filtered_df)
        elif filter_type == "Exclude Testers":
            filtered_df = df[df["Role"] != "Tester"]
            load_data(self.table_widget, filtered_df)
        elif filter_type == "Count by Role":
            role_counts = df["Role"].value_counts().reset_index()
            role_counts.columns = ["Role", "Count"]
            load_data(self.table_widget, role_counts)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmployeeApp()
    window.show()
    sys.exit(app.exec())