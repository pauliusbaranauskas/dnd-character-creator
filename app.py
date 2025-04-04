from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QLineEdit, QLabel, QComboBox, QHBoxLayout
import sys
from character import Character
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.class_descriptions = {
            "Barbarian":"Barbarians are brute fighters. Fueled by their rage they ravage battlefields seeding a fear in their opponents.",
            "Wizard":"Wizards are magical creatures. They use their magic to create powerful spells and to control the elements."
        }
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

    def create_character(self, selected_class=None):
        # Clear the main window's central widget
        self.centralWidget().deleteLater()
        # Create a new layout for the class selection page
        layout = QVBoxLayout()
        # Add a label

        # Add radio buttons for class options
        horizontal_layout_1 = QHBoxLayout()
        class_button = QComboBox()
        class_button.addItems(["Barbarian", "Wizard"])  # Add values to the combo box
        if selected_class:
            index = class_button.findText(selected_class)
            if index >= 0:
                class_button.setCurrentIndex(index)

        class_button.currentTextChanged.connect(lambda: self.create_character(class_button.currentText()))
        horizontal_layout_1.addWidget(QLabel("Select the class of your character:"))
        horizontal_layout_1.addWidget(class_button)

        layout.addLayout(horizontal_layout_1)

        # Add a confirm button
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(lambda: self.confirm_selection(class_button))
        layout.addWidget(QLabel(self.class_descriptions[class_button.currentText()]))

        layout.addWidget(confirm_button)

        # # Create a widget and set it as the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def confirm_selection(self, class_button):
        self.character = Character(class_button.currentText())
        self.centralWidget().deleteLater()
        if self.character.character_class == "Barbarian":
            self.barbarian_setup()

    def validate_stat(self, stat_input):
        if stat_input.text().isdigit():
            if int(stat_input.text()) > 20:
                stat_input.setStyleSheet("color: red;")
            elif int(stat_input.text()) < 1:
                stat_input.setStyleSheet("color: red;")
            else:
                stat_input.setStyleSheet("color: black;")
        else:
            stat_input.setStyleSheet("color: red;")

    def stat_layout(self, stat_name):
        layout = QVBoxLayout()
        stat_input = QLineEdit()
        stat_input.setMaxLength(2)  # Limit input string length
        stat_input.setPlaceholderText(f"Enter {stat_name} value")
        stat_input.textChanged.connect(lambda: self.validate_stat(stat_input))
        layout.addWidget(QLabel(stat_name))
        layout.addWidget(stat_input)

        return stat_input, layout

    def barbarian_setup(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(
f"""You selected Barbarian.
We will start with your basic stats as if you were a 1st level character and work your way up."""))

        layout.addWidget(QLabel("As a 1st level Barbarian, you gain RAGE, UNARMORED DEFENSE, WEAPON MASTERY."))
        layout.addWidget(QLabel("Let's input your stats:"))

        horizontal_layout_1 = QHBoxLayout()

        stats = []

        str_input_box, str_layout = self.stat_layout("Strength")
        horizontal_layout_1.addLayout(str_layout)
        stats.append(str_input_box)

        dex_input_box, dex_layout = self.stat_layout("Dexterity")
        horizontal_layout_1.addLayout(dex_layout)
        stats.append(dex_input_box)

        con_input_box, con_layout = self.stat_layout("Constitution")
        horizontal_layout_1.addLayout(con_layout)
        stats.append(con_input_box)

        int_input_box, int_layout = self.stat_layout("Intelligence")
        horizontal_layout_1.addLayout(int_layout)
        stats.append(int_input_box)

        wis_input_box, wis_layout = self.stat_layout("Wisdom")
        horizontal_layout_1.addLayout(wis_layout)
        stats.append(wis_input_box)

        cha_input_box, cha_layout = self.stat_layout("Charisma")
        horizontal_layout_1.addLayout(cha_layout)
        stats.append(cha_input_box)

        layout.addLayout(horizontal_layout_1)
        widget = QWidget()
        widget.setLayout(layout)
        horizontal_layout_2 = QHBoxLayout()
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(lambda: self.create_barbarian(stats))
        generate_button = QPushButton("Generate")
        back_button = QPushButton("Back")
        exit_button = QPushButton("Exit")
        generate_button.clicked.connect(lambda: self.generate_numbers(stats))
        exit_button.clicked.connect(self.close)
        back_button.clicked.connect(self.create_character)
        horizontal_layout_2.addWidget(confirm_button)
        horizontal_layout_2.addWidget(generate_button)
        horizontal_layout_2.addWidget(back_button)
        horizontal_layout_2.addWidget(exit_button)
        layout.addLayout(horizontal_layout_2)
        self.setCentralWidget(widget)

    def create_barbarian(self, stats):
        print("Creating barbarian")
        self.character = Character("Barbarian")
        self.character.strength = int(stats[0].text())
        self.character.dexterity = int(stats[1].text())
        self.character.constitution = int(stats[2].text())
        self.character.intelligence = int(stats[3].text())
        self.character.wisdom = int(stats[4].text())
        self.character.charisma = int(stats[5].text())
        print(self.character)


    def generate_numbers(self, stats):
        print("Generating stats")
        for stat in stats:
            stat.setText(str(self.generate_stat()))

    def load_character(self):
        print("Load Character clicked")  # Replace with your logic

    def open_options(self):
        print("Options clicked")  # Replace with your logic

    def generate_stat(self):
        rolls = []
        for i in range(4):
            rolls.append(random.randint(1, 6))
        rolls.sort(reverse=True)
        rolls = rolls[0:3]
        print(rolls)
        return sum(rolls)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()  # Show the window
    sys.exit(app.exec())  # Ensure proper application exit

    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
