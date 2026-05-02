import sys
import random
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, 
    QWidget, QLineEdit, QLabel, QComboBox, QHBoxLayout, 
    QStackedWidget, QFrame, QScrollArea, QCheckBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from character import Character
from data import CLASSES, RACES, WEAPONS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DnD Character Creator")
        self.setGeometry(100, 100, 600, 600)

        self.character_data = {
            "class": None,
            "race": None,
            "skills": [],
            "stats": {},
            "equipment": "",
            "equipment_choices": [] # To store [ { "index": 0, "combo_text": "..." }, ... ]
        }
        
        self.resizable_buttons = []

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_screens()
        self.show_main_menu()

    def init_screens(self):
        # Create persistent screen widgets
        self.main_menu = self.create_main_menu()
        self.class_screen = self.create_class_selection_screen()
        self.race_screen = self.create_race_selection_screen()
        self.customization_screen = self.create_customization_screen()
        self.equipment_screen = self.create_equipment_screen()
        self.review_screen = self.create_review_screen()

        self.stack.addWidget(self.main_menu)          # Index 0
        self.stack.addWidget(self.class_screen)        # Index 1
        self.stack.addWidget(self.race_screen)         # Index 2
        self.stack.addWidget(self.customization_screen) # Index 3
        self.stack.addWidget(self.equipment_screen)     # Index 4
        self.stack.addWidget(self.review_screen)       # Index 5

    # --- Navigation ---
    def show_main_menu(self): self.stack.setCurrentIndex(0)
    def show_class_selection(self): 
        self.update_class_selection()
        self.stack.setCurrentIndex(1)
    def show_race_selection(self): 
        self.update_race_selection()
        self.stack.setCurrentIndex(2)
    def show_customization(self): 
        self.update_customization_screen()
        self.stack.setCurrentIndex(3)
    def show_equipment(self):
        self.update_equipment_screen()
        self.stack.setCurrentIndex(4)
    def show_review(self): 
        self.update_review_screen()
        self.stack.setCurrentIndex(5)

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

    def create_class_selection_screen(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select your Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItems(list(CLASSES.keys()))
        
        self.class_desc = QLabel()
        self.class_desc.setWordWrap(True)
        self.class_desc.setMinimumHeight(250)
        
        def update_class_info(text):
            cls = CLASSES[text]
            info = [cls["description"], ""]
            info.append(f"Hit Die: d{cls['hit_die']}")
            info.append(f"Primary Ability: {cls['primary_ability']}")
            info.append(f"Saving Throws: {', '.join(cls['saves'])}")
            features = cls.get("features", {})
            if features:
                info.append("\nFeatures:")
                for name, desc in features.items():
                    info.append(f"• {name}: {desc}")
            self.class_desc.setText("\n".join(info))

        self.class_combo.currentTextChanged.connect(update_class_info)
        update_class_info(self.class_combo.currentText())
        
        layout.addWidget(self.class_combo)
        layout.addWidget(self.class_desc)
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_main_menu)
        
        btn_next = QPushButton("Next")
        def on_next():
            self.character_data["class"] = self.class_combo.currentText()
            self.show_race_selection()
        btn_next.clicked.connect(on_next)

        self.resizable_buttons.extend([btn_back, btn_next])
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_next)
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_race_selection_screen(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select your Race:"))
        self.race_combo = QComboBox()
        self.race_combo.addItems(list(RACES.keys()))
        
        self.race_desc = QLabel()
        self.race_desc.setWordWrap(True)
        self.race_desc.setMinimumHeight(200)
        
        def update_race_info(text):
            race = RACES[text]
            info = [race["description"], ""]
            bonuses = race.get("ability_score_bonus", {})
            if bonuses:
                bonus_str = ", ".join([f"+{v} {k}" for k, v in bonuses.items()])
                info.append(f"Ability Bonuses: {bonus_str}")
            info.append(f"Speed: {race['speed']} ft.")
            traits = race.get("traits", [])
            if traits:
                info.append(f"Traits: {', '.join(traits)}")
            self.race_desc.setText("\n".join(info))

        self.race_combo.currentTextChanged.connect(update_race_info)
        update_race_info(self.race_combo.currentText())
        
        layout.addWidget(self.race_combo)
        layout.addWidget(self.race_desc)
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_class_selection)
        
        btn_next = QPushButton("Next")
        def on_next():
            self.character_data["race"] = self.race_combo.currentText()
            self.show_customization()
        btn_next.clicked.connect(on_next)

        self.resizable_buttons.extend([btn_back, btn_next])
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_next)
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def update_class_selection(self):
        if self.character_data["class"]:
            idx = self.class_combo.findText(self.character_data["class"])
            if idx >= 0: self.class_combo.setCurrentIndex(idx)

    def update_race_selection(self):
        if self.character_data["race"]:
            idx = self.race_combo.findText(self.character_data["race"])
            if idx >= 0: self.race_combo.setCurrentIndex(idx)

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
        
        btn_next = QPushButton("Next")
        btn_next.clicked.connect(self.finalize_customization)
        
        self.resizable_buttons.extend([btn_back, btn_clear, btn_next])
        
        bottom_row.addWidget(btn_back)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_clear)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_next)
        
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
        
        current_skills = self.character_data.get("skills", [])
        for option in options:
            cb = QCheckBox(option)
            if option in current_skills:
                cb.setChecked(True)
            self.skill_checkboxes.append(cb)
            self.skills_container.addWidget(cb)
            
        # Ensure stats are populated if coming back
        for stat, value in self.character_data.get("stats", {}).items():
            if stat in self.stat_inputs:
                self.stat_inputs[stat].setText(str(value))

    def create_equipment_screen(self):
        screen_layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.equip_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        
        self.equip_label = QLabel("Choose your starting equipment:")
        self.equip_layout.addWidget(self.equip_label)
        
        self.equip_choices_container = QVBoxLayout()
        self.equip_layout.addLayout(self.equip_choices_container)
        
        self.equip_choice_groups = [] # List of (button_group, list of (radio, combo or None))

        screen_layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_customization)
        
        btn_next = QPushButton("Confirm & Review")
        btn_next.clicked.connect(self.finalize_equipment)
        
        self.resizable_buttons.extend([btn_back, btn_next])
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_next)
        
        screen_layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(screen_layout)
        return widget

    def update_equipment_screen(self):
        # Clear old content
        for i in reversed(range(self.equip_choices_container.count())):
            item = self.equip_choices_container.itemAt(i)
            if item.widget(): item.widget().setParent(None)
            elif item.layout():
                # Need to recursively clear layouts
                self.clear_layout(item.layout())
        
        self.equip_choice_groups = []
        
        class_info = CLASSES.get(self.character_data["class"], {})
        equip_data = class_info.get("starting_equipment", {})
        
        # Display fixed equipment
        if equip_data.get("fixed"):
            fixed_label = QLabel(f"Fixed Equipment: {', '.join(equip_data['fixed'])}")
            fixed_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            self.equip_choices_container.addWidget(fixed_label)

        # Display choices
        choices_history = self.character_data.get("equipment_choices", [])
        
        for block_idx, choice_block in enumerate(equip_data.get("choices", [])):
            group = QButtonGroup(self)
            choice_items = []
            
            choice_box = QFrame()
            choice_box.setFrameShape(QFrame.Shape.StyledPanel)
            choice_vbox = QVBoxLayout(choice_box)
            
            for i, opt in enumerate(choice_block["options"]):
                h_layout = QHBoxLayout()
                rb = QRadioButton(opt["label"])
                group.addButton(rb, i)
                h_layout.addWidget(rb)
                
                combo = None
                if "type" in opt:
                    combo = QComboBox()
                    combo.addItems(WEAPONS.get(opt["type"], []))
                    combo.setEnabled(False)
                    h_layout.addWidget(combo)
                    
                    # Connect radio button to enable/disable combo
                    rb.toggled.connect(lambda checked, c=combo: c.setEnabled(checked))

                choice_vbox.addLayout(h_layout)
                choice_items.append((rb, combo, opt))

            self.equip_choices_container.addWidget(choice_box)
            self.equip_choice_groups.append((group, choice_items))
            
            # Restore state if exists, otherwise select first
            if block_idx < len(choices_history):
                hist = choices_history[block_idx]
                selected_idx = hist["index"]
                if selected_idx >= 0 and selected_idx < len(choice_items):
                    choice_items[selected_idx][0].setChecked(True)
                    if choice_items[selected_idx][1] and hist["combo_text"]:
                        c = choice_items[selected_idx][1]
                        c_idx = c.findText(hist["combo_text"])
                        if c_idx >= 0: c.setCurrentIndex(c_idx)
            elif choice_items:
                choice_items[0][0].setChecked(True)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

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
        btn_back.clicked.connect(self.show_equipment)
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

    def finalize_customization(self):
        # Handle Stats
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

        # Handle Skills
        class_info = CLASSES.get(self.character_data["class"], {})
        num_to_choose = class_info.get("proficiencies", {}).get("skills", {}).get("choose", 0)
        selected_boxes = [cb for cb in self.skill_checkboxes if cb.isChecked()]
        
        if len(selected_boxes) < num_to_choose:
            needed = num_to_choose - len(selected_boxes)
            available = [cb for cb in self.skill_checkboxes if not cb.isChecked()]
            if available:
                picked = random.sample(available, min(needed, len(available)))
                for cb in picked: cb.setChecked(True)
        elif len(selected_boxes) > num_to_choose:
            for cb in selected_boxes[num_to_choose:]:
                cb.setChecked(False)

        self.character_data["skills"] = [cb.text() for cb in self.skill_checkboxes if cb.isChecked()]
        self.show_equipment()

    def finalize_equipment(self):
        final_equip = []
        choices_state = []
        
        # Add fixed equipment
        class_info = CLASSES.get(self.character_data["class"], {})
        equip_data = class_info.get("starting_equipment", {})
        final_equip.extend(equip_data.get("fixed", []))
        
        # Add chosen equipment
        for group, choice_items in self.equip_choice_groups:
            checked_idx = group.checkedId()
            combo_text = ""
            for i, (rb, combo, opt) in enumerate(choice_items):
                if rb.isChecked():
                    if combo:
                        final_equip.append(combo.currentText())
                        combo_text = combo.currentText()
                    else:
                        final_equip.append(opt["item"])
            choices_state.append({"index": checked_idx, "combo_text": combo_text})
            
        self.character_data["equipment_choices"] = choices_state
        self.character_data["equipment"] = ", ".join(final_equip)
        self.show_review()

    def update_review_screen(self):
        self.char_obj = Character(self.character_data["class"], self.character_data["race"])
        self.char_obj.set_stats(self.character_data["stats"])
        self.char_obj.set_skills(self.character_data["skills"])
        self.char_obj.set_equipment(self.character_data["equipment"])
        self.review_label.setText(str(self.char_obj))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
