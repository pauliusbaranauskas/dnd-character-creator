import sys
import random
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, 
    QWidget, QLineEdit, QLabel, QComboBox, QHBoxLayout, 
    QStackedWidget, QFrame, QScrollArea, QCheckBox
)
from PyQt6.QtCore import Qt
from character import Character
from data import CLASSES, RACES

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DnD Character Creator")
        self.setGeometry(100, 100, 600, 600)

        self.character_data = {
            "class": None,
            "race": None,
            "skills": [],
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
        self.customization_screen = self.create_customization_screen()
        self.review_screen = self.create_review_screen()

        self.stack.addWidget(self.main_menu)          # Index 0
        self.stack.addWidget(self.class_screen)        # Index 1
        self.stack.addWidget(self.race_screen)         # Index 2
        self.stack.addWidget(self.customization_screen) # Index 3
        self.stack.addWidget(self.review_screen)       # Index 4

    # --- Navigation ---
    def show_main_menu(self): self.stack.setCurrentIndex(0)
    def show_class_selection(self): self.stack.setCurrentIndex(1)
    def show_race_selection(self): self.stack.setCurrentIndex(2)
    def show_customization(self): 
        self.update_customization_screen()
        self.stack.setCurrentIndex(3)
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
            else: self.show_customization()
            
        btn_next.clicked.connect(on_next)

        self.resizable_buttons.extend([btn_back, btn_next])

        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_next)

        layout.addWidget(label)
        layout.addWidget(combo)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_customization_screen(self):
        # Main layout for the screen
        screen_layout = QVBoxLayout()
        
        # Scroll Area Setup
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.custom_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        
        # --- Skills Section ---
        self.skills_label = QLabel("Choose your skills:")
        self.custom_layout.addWidget(self.skills_label)
        
        self.skills_container = QVBoxLayout()
        self.custom_layout.addLayout(self.skills_container)
        self.skill_checkboxes = []
        
        btn_roll_skills = QPushButton("Roll Skills Randomly")
        btn_roll_skills.clicked.connect(self.generate_random_skills)
        self.custom_layout.addWidget(btn_roll_skills, 0, Qt.AlignmentFlag.AlignLeft)
        self.resizable_buttons.append(btn_roll_skills)
        
        self.custom_layout.addSpacing(20)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.custom_layout.addWidget(line)
        self.custom_layout.addSpacing(20)

        # --- Stats Section ---
        self.custom_layout.addWidget(QLabel("Allocate your Base Stats:"))
        notice = QLabel("(Empty fields will be generated randomly using 4d6)")
        notice.setStyleSheet("color: #666; font-style: italic; font-size: 11px;")
        self.custom_layout.addWidget(notice)
        
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
            self.custom_layout.addLayout(h_layout)

        btn_roll_stats = QPushButton("Roll All Stats")
        btn_roll_stats.clicked.connect(self.generate_random_stats)
        self.custom_layout.addWidget(btn_roll_stats, 0, Qt.AlignmentFlag.AlignLeft)
        self.resizable_buttons.append(btn_roll_stats)
        
        screen_layout.addWidget(scroll)

        # --- Bottom Navigation Row ---
        bottom_row = QHBoxLayout()
        
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_race_selection)
        
        btn_clear = QPushButton("Clear All")
        btn_clear.clicked.connect(self.clear_all_customization)
        
        btn_confirm = QPushButton("Confirm & Review")
        btn_confirm.clicked.connect(self.finalize_character)
        
        self.resizable_buttons.extend([btn_back, btn_clear, btn_confirm])
        
        bottom_row.addWidget(btn_back)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_clear)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_confirm)
        
        screen_layout.addLayout(bottom_row)
        
        widget = QWidget()
        widget.setLayout(screen_layout)
        return widget

    def update_customization_screen(self):
        # Clear old skill checkboxes
        for i in reversed(range(self.skills_container.count())): 
            self.skills_container.itemAt(i).widget().setParent(None)
        self.skill_checkboxes = []
        
        class_info = CLASSES.get(self.character_data["class"], {})
        skill_data = class_info.get("proficiencies", {}).get("skills", {})
        num_to_choose = skill_data.get("choose", 0)
        options = skill_data.get("options", [])
        
        self.skills_label.setText(f"Choose {num_to_choose} skills for {self.character_data['class']}:")
        self.skills_label.setStyleSheet("color: black;")
        
        for option in options:
            cb = QCheckBox(option)
            self.skill_checkboxes.append(cb)
            self.skills_container.addWidget(cb)

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
        btn_back.clicked.connect(self.show_customization)
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
    def clear_all_customization(self):
        # Clear stats
        for edit in self.stat_inputs.values():
            edit.clear()
        # Clear skills
        for cb in self.skill_checkboxes:
            cb.setChecked(False)

    def roll_4d6(self):
        rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
        return sum(rolls[:3])

    def generate_random_stats(self):
        for edit in self.stat_inputs.values():
            edit.setText(str(self.roll_4d6()))

    def generate_random_skills(self):
        # Uncheck all first
        for cb in self.skill_checkboxes: cb.setChecked(False)
        
        class_info = CLASSES.get(self.character_data["class"], {})
        num_to_choose = class_info.get("proficiencies", {}).get("skills", {}).get("choose", 0)
        if not self.skill_checkboxes: return
        
        to_check = random.sample(self.skill_checkboxes, min(num_to_choose, len(self.skill_checkboxes)))
        for cb in to_check: cb.setChecked(True)

    def finalize_character(self):
        # 1. Handle Stats
        stats = {}
        for name, edit in self.stat_inputs.items():
            val = edit.text().strip()
            if val.isdigit():
                stats[name] = int(val)
            else:
                rolled = self.roll_4d6()
                stats[name] = rolled
                edit.setText(str(rolled))
        self.character_data["stats"] = stats

        # 2. Handle Skills (auto-random if not enough selected)
        class_info = CLASSES.get(self.character_data["class"], {})
        num_to_choose = class_info.get("proficiencies", {}).get("skills", {}).get("choose", 0)
        selected_boxes = [cb for cb in self.skill_checkboxes if cb.isChecked()]
        
        if len(selected_boxes) < num_to_choose:
            # Need to pick more
            needed = num_to_choose - len(selected_boxes)
            available = [cb for cb in self.skill_checkboxes if not cb.isChecked()]
            if available:
                picked = random.sample(available, min(needed, len(available)))
                for cb in picked: cb.setChecked(True)
        elif len(selected_boxes) > num_to_choose:
            # Too many, just take first N
            for cb in selected_boxes[num_to_choose:]:
                cb.setChecked(False)

        self.character_data["skills"] = [cb.text() for cb in self.skill_checkboxes if cb.isChecked()]
        
        # Create and show
        self.char_obj = Character(self.character_data["class"], self.character_data["race"])
        self.char_obj.set_stats(self.character_data["stats"])
        self.char_obj.set_skills(self.character_data["skills"])
        self.show_review()

    def update_review_screen(self):
        if hasattr(self, 'char_obj'):
            self.review_label.setText(str(self.char_obj))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
