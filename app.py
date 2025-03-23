from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QRadioButton, QComboBox
import sys
from character import Character

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DnD character creator")

        # Set window size
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        self.start_window()


    def start_window(self):
        # Create a main layout
        main_layout = QVBoxLayout()

        # Create buttons
        button1 = QPushButton("Create Character")
        button2 = QPushButton("Load Character")
        button3 = QPushButton("Options")
        button4 = QPushButton("Exit")

        # Connect buttons to actions (replace with your desired functions)
        button1.clicked.connect(self.create_character)
        button2.clicked.connect(self.load_character)
        button3.clicked.connect(self.open_options)
        button4.clicked.connect(self.close)

        # Add buttons to the layout
        main_layout.addWidget(button1)
        main_layout.addWidget(button2)
        main_layout.addWidget(button3)
        main_layout.addWidget(button4)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_character(self):
        # Clear the main window's central widget
        self.centralWidget().deleteLater()
        # Create a new layout for the class selection page
        layout = QVBoxLayout()
        # Add a label
        layout.addWidget(QLabel("Select the class of your character:"))

        # Add radio buttons for class options
        class_button = QComboBox()
        class_button.addItems(["Barbarian", "Wizard (N/A)"])  # Add values to the combo box
        layout.addWidget(class_button)

        layout.addWidget(QLabel("Select the race of your character:"))
        # Adding race button
        race_button = QComboBox()
        race_button.addItems(["Human", "Elf (N/A)"])
        layout.addWidget(race_button)

        # Add a confirm button
        confirm_button = QPushButton("Confirm")
        # confirm_button.clicked.connect(self.confirm_class_selection)
        layout.addWidget(confirm_button)
        #
        # # Create a widget and set it as the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def load_character(self):
        print("Load Character clicked")  # Replace with your logic

    def open_options(self):
        print("Options clicked")  # Replace with your logic


app = QApplication(sys.argv)
w = MainWindow()
w.show()  # Show the window
sys.exit(app.exec())  # Ensure proper application exit

app = QApplication(sys.argv)
w = MainWindow()
app.exec()