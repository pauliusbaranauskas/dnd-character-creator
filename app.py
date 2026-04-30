import sys
import random
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, 
    QWidget, QLineEdit, QLabel, QComboBox, QHBoxLayout, 
    QStackedWidget, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from character import Character
from data import CLASSES, RACES

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DnD Character Creator")
        self.setGeometry(100, 100, 600, 500)

        self.character_data = {
            "class": None,
            "race": None,
            "stats": {}
        }
        
        self.resizable_buttons = []

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_screens()
        self.show_main_menu()

    def init_screens(self):
        # Create persistent screen widgets
        self.main_menu = self.create_main_menu()
        self.class_screen = self.create_selection_screen("class", CLASSES)
        self.race_screen = self.create_selection_screen("race", RACES)
        self.stats_screen = self.create_stats_screen()
        self.review_screen = self.create_review_screen()

        self.stack.addWidget(self.main_menu)    # Index 0
        self.stack.addWidget(self.class_screen)  # Index 1
        self.stack.addWidget(self.race_screen)   # Index 2
        self.stack.addWidget(self.stats_screen)  # Index 3
        self.stack.addWidget(self.review_screen) # Index 4

    # --- Navigation ---
    def show_main_menu(self): self.stack.setCurrentIndex(0)
    def show_class_selection(self): self.stack.setCurrentIndex(1)
    def show_race_selection(self): self.stack.setCurrentIndex(2)
    def show_stats_allocation(self): self.stack.setCurrentIndex(3)
    def show_review(self): 
        self.update_review_screen()
        self.stack.setCurrentIndex(4)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        target_width = self.width() // 4
        for btn in self.resizable_buttons:
            btn.setFixedWidth(target_width)

    # --- Screen Builders ---
    def create_main_menu(self):
        layout = QVBoxLayout()
        title = QLabel("D&D Character Creator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        btn_new = QPushButton("Create New Character")
        btn_new.clicked.connect(self.show_class_selection)
        
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.close)

        self.resizable_buttons.extend([btn_new, btn_exit])

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(btn_new, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_exit, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_selection_screen(self, type_name, data_source):
        layout = QVBoxLayout()
        label = QLabel(f"Select your {type_name}:")
        
        combo = QComboBox()
        combo.addItems(list(data_source.keys()))
        
        desc_label = QLabel(data_source[combo.currentText()]["description"])
        desc_label.setWordWrap(True)
        desc_label.setMinimumHeight(100)
        
        combo.currentTextChanged.connect(lambda text: desc_label.setText(data_source[text]["description"]))
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_main_menu if type_name == "class" else self.show_class_selection)
        
        btn_next = QPushButton("Next")
        def on_next():
            self.character_data[type_name] = combo.currentText()
            if type_name == "class": self.show_race_selection()
            else: self.show_stats_allocation()
            
        btn_next.clicked.connect(on_next)

        self.resizable_buttons.extend([btn_back, btn_next])

        btn_layout.addWidget(btn_back)
        btn_layout.addStretch() # Oriented to opposite sides
        btn_layout.addWidget(btn_next)

        layout.addWidget(label)
        layout.addWidget(combo)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_stats_screen(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Allocate your Base Stats:"))
        
        notice = QLabel("(Empty fields will be generated randomly using 4d6)")
        notice.setStyleSheet("color: #666; font-style: italic; font-size: 11px;")
        layout.addWidget(notice)
        
        self.stat_inputs = {}
        stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        
        for stat in stats:
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(stat), 1)
            
            edit = QLineEdit()
            edit.setPlaceholderText("Empty = Random")
            edit.setMaxLength(2)
            self.stat_inputs[stat] = edit
            h_layout.addWidget(edit, 2)
            layout.addLayout(h_layout)

        controls_layout = QHBoxLayout()
        btn_gen = QPushButton("Roll All Randomly")
        btn_gen.clicked.connect(self.generate_random_stats)
        
        btn_clear = QPushButton("Clear All")
        btn_clear.clicked.connect(self.clear_stats)
        
        controls_layout.addWidget(btn_gen)
        controls_layout.addWidget(btn_clear)
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_race_selection)
        
        btn_next = QPushButton("Confirm & Review")
        btn_next.clicked.connect(self.finalize_character)
        
        self.resizable_buttons.extend([btn_gen, btn_clear, btn_back, btn_next])

        btn_layout.addWidget(btn_back)
        btn_layout.addStretch() # Opposite sides
        btn_layout.addWidget(btn_next)

        layout.addLayout(controls_layout)
        layout.addStretch()
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_review_screen(self):
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.review_label = QLabel("Character Review")
        self.review_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.review_label.setStyleSheet("font-family: monospace; font-size: 12px; padding: 10px;")
        self.review_label.setWordWrap(True)
        
        scroll.setWidget(self.review_label)
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_stats_allocation)
        
        btn_finish = QPushButton("Back to Main Menu")
        btn_finish.clicked.connect(self.show_main_menu)
        
        self.resizable_buttons.extend([btn_back, btn_finish])
        
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_finish)
        
        layout.addWidget(scroll)
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    # --- Logic ---
    def clear_stats(self):
        for edit in self.stat_inputs.values():
            edit.clear()

    def roll_4d6(self):
        rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
        return sum(rolls[:3])

    def generate_random_stats(self):
        for edit in self.stat_inputs.values():
            edit.setText(str(self.roll_4d6()))

    def finalize_character(self):
        stats = {}
        for name, edit in self.stat_inputs.items():
            val = edit.text().strip()
            if val.isdigit():
                stats[name] = int(val)
            else:
                # Generate random stat if empty or invalid
                rolled = self.roll_4d6()
                stats[name] = rolled
                edit.setText(str(rolled)) # Show the generated value to user
        
        self.character_data["stats"] = stats
        
        # Create the character object
        self.char_obj = Character(self.character_data["class"], self.character_data["race"])
        self.char_obj.set_stats(stats)
        
        self.show_review()

    def update_review_screen(self):
        if hasattr(self, 'char_obj'):
            self.review_label.setText(str(self.char_obj))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
