import sys
import os
import random
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QVBoxLayout, 
    QWidget, QLineEdit, QLabel, QComboBox, QHBoxLayout, 
    QStackedWidget, QFrame, QScrollArea, QCheckBox, QRadioButton, QButtonGroup,
    QFileDialog, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from character import Character
from data import CLASSES, RACES, WEAPONS, TRAITS, STATS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DnD Character Creator")
        self.setGeometry(100, 100, 600, 600)

        self.character_data = {
            "name": "Unnamed Adventurer",
            "level": 1,
            "race-name": "",
            "classes": {},
            "ability-scores": {
                "strength": 10,
                "dexterity": 10,
                "constitution": 10,
                "intelligence": 10,
                "wisdom": 10,
                "charisma": 10
            },
            "attributes": {
                "hit-points-max": 0,
                "armor-class": 10,
                "speed": 30,
                "proficiency-bonus": 2
            },
            "skills": {},
            "equipment": [],
            "features-and-traits": []
        }
        self.equipment_choices_history = []
        
        self.resizable_buttons = []

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_screens()
        self.show_main_menu()

    @property
    def current_class_name(self):
        classes = self.character_data.get("classes", {})
        if classes:
            first_cls = next(iter(classes.values()))
            return first_cls.get("class-name")
        return None

    @property
    def current_race_name(self):
        return self.character_data.get("race-name", "")

    def init_screens(self):
        # Create persistent screen widgets
        self.main_menu = self.create_main_menu()
        self.class_screen = self.create_class_selection_screen()
        self.race_screen = self.create_race_selection_screen()
        self.customization_screen = self.create_customization_screen()
        self.equipment_screen = self.create_equipment_screen()
        self.review_screen = self.create_review_screen()
        self.recent_characters_screen = self.create_recent_characters_screen()

        self.stack.addWidget(self.main_menu)                 # Index 0
        self.stack.addWidget(self.class_screen)               # Index 1
        self.stack.addWidget(self.race_screen)                # Index 2
        self.stack.addWidget(self.customization_screen)        # Index 3
        self.stack.addWidget(self.equipment_screen)            # Index 4
        self.stack.addWidget(self.review_screen)              # Index 5
        self.stack.addWidget(self.recent_characters_screen)   # Index 6

    # --- Navigation ---
    def show_main_menu(self): self.stack.setCurrentIndex(0)
    def show_recent_characters(self):
        self.update_recent_characters_screen()
        self.stack.setCurrentIndex(6)
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
        target_width = max(90, min(self.width() // 4 - 15, 140))
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
        
        btn_load = QPushButton("Load Character")
        btn_load.clicked.connect(self.show_recent_characters)

        btn_import = QPushButton("Import Character")
        btn_import.clicked.connect(self.import_character)
        
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.close)

        self.resizable_buttons.extend([btn_new, btn_load, btn_import, btn_exit])

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(btn_new, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_load, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_import, 0, Qt.AlignmentFlag.AlignCenter)
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
            cls_name = self.class_combo.currentText()
            cls_info = CLASSES.get(cls_name, {})
            self.character_data["classes"] = {
                cls_name.lower(): {
                    "class-name": cls_name,
                    "class-level": 1,
                    "hit-die": cls_info.get("hit_die", 0)
                }
            }
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
        
        self.race_info_label = QLabel()
        self.race_info_label.setWordWrap(True)
        
        self.traits_header = QLabel("Traits (hover for details):")
        self.traits_header.setStyleSheet("font-weight: bold; margin-top: 10px;")
        
        self.traits_widget = QWidget()
        self.traits_layout = QVBoxLayout(self.traits_widget)
        self.traits_layout.setContentsMargins(10, 0, 0, 0)
        
        def update_race_info(text):
            race = RACES[text]
            info = [race["description"], ""]
            bonuses = race.get("ability_score_bonus", {})
            if bonuses:
                bonus_str = ", ".join([f"+{v} {k}" for k, v in bonuses.items()])
                info.append(f"Ability Bonuses: {bonus_str}")
            info.append(f"Speed: {race['speed']} ft.")
            self.race_info_label.setText("\n".join(info))
            
            # Update Traits
            self.clear_layout(self.traits_layout)
            traits = race.get("traits", [])
            if traits:
                self.traits_header.show()
                for trait_name in traits:
                    trait_info = TRAITS.get(trait_name, {})
                    desc = trait_info.get("description", "No description available.")
                    t_label = QLabel(f"• <u>{trait_name}</u>")
                    t_label.setToolTip(desc)
                    t_label.setCursor(Qt.CursorShape.PointingHandCursor)
                    self.traits_layout.addWidget(t_label)
            else:
                self.traits_header.hide()

        self.race_combo.currentTextChanged.connect(update_race_info)
        
        layout.addWidget(self.race_combo)
        layout.addWidget(self.race_info_label)
        layout.addWidget(self.traits_header)
        layout.addWidget(self.traits_widget)
        layout.addStretch()
        
        # Trigger initial update
        update_race_info(self.race_combo.currentText())
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_class_selection)
        
        btn_next = QPushButton("Next")
        def on_next():
            race_name = self.race_combo.currentText()
            self.character_data["race-name"] = race_name
            
            features_and_traits = []
            for trait in RACES.get(race_name, {}).get("traits", []):
                features_and_traits.append({"name": trait, "source": race_name})
            
            cls_name = self.current_class_name
            if cls_name:
                for feat in CLASSES.get(cls_name, {}).get("features", {}).keys():
                    features_and_traits.append({"name": feat, "source": cls_name})
                    
            self.character_data["features-and-traits"] = features_and_traits
            self.character_data["attributes"]["speed"] = RACES.get(race_name, {}).get("speed", 30)
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
        if self.current_class_name:
            idx = self.class_combo.findText(self.current_class_name)
            if idx >= 0: self.class_combo.setCurrentIndex(idx)

    def update_race_selection(self):
        if self.current_race_name:
            idx = self.race_combo.findText(self.current_race_name)
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
            label = QLabel(f"<u>{stat}</u>")
            stat_info = STATS.get(stat, {})
            label.setToolTip(stat_info.get("description", ""))
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            h_layout.addWidget(label, 1)
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
        
        class_name = self.current_class_name or list(CLASSES.keys())[0]
        class_info = CLASSES.get(class_name, {})
        skill_data = class_info.get("proficiencies", {}).get("skills", {})
        num_to_choose = skill_data.get("choose", 0)
        options = skill_data.get("options", [])
        
        self.skills_label.setText(f"Choose {num_to_choose} skills for {class_name}:")
        self.skills_label.setStyleSheet("color: black;")
        
        skills_map = self.character_data.get("skills", {})
        current_skills = [k.lower() for k, v in skills_map.items() if v.get("proficient")]
        for option in options:
            cb = QCheckBox(option)
            if option.lower() in current_skills:
                cb.setChecked(True)
            cb.toggled.connect(self.on_skill_checkbox_toggled)
            self.skill_checkboxes.append(cb)
            self.skills_container.addWidget(cb)
            
        self.on_skill_checkbox_toggled()
            
        # Ensure stats are populated if coming back
        scores = self.character_data.get("ability-scores", {})
        for stat in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
            if stat in self.stat_inputs:
                if stat.lower() in scores:
                    self.stat_inputs[stat].setText(str(scores[stat.lower()]))

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
                self.clear_layout(item.layout())
        
        self.equip_choice_groups = []
        
        class_name = self.current_class_name or list(CLASSES.keys())[0]
        class_info = CLASSES.get(class_name, {})
        equip_data = class_info.get("starting_equipment", {})
        
        # Display fixed equipment
        if equip_data.get("fixed"):
            fixed_label = QLabel(f"Fixed Equipment: {', '.join(equip_data['fixed'])}")
            fixed_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            self.equip_choices_container.addWidget(fixed_label)

        # Display choices
        choices_history = self.equipment_choices_history
        
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
                if 0 <= selected_idx < len(choice_items):
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
        
        btn_save = QPushButton("Save Character")
        btn_save.clicked.connect(self.save_character)

        btn_export = QPushButton("Export Character")
        btn_export.clicked.connect(self.export_character)
        
        btn_finish = QPushButton("Back to Main Menu")
        btn_finish.clicked.connect(self.show_main_menu)
        
        self.resizable_buttons.extend([btn_back, btn_save, btn_export, btn_finish])
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_export)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_finish)
        
        layout.addWidget(scroll)
        layout.addLayout(btn_layout)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_recent_characters_screen(self):
        layout = QVBoxLayout()
        
        title = QLabel("Recent Characters")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        desc = QLabel("Select a saved character to load:")
        desc.setStyleSheet("color: #555; margin-bottom: 8px;")
        layout.addWidget(desc)
        
        self.recent_list = QListWidget()
        self.recent_list.setStyleSheet("font-size: 13px; padding: 5px;")
        self.recent_list.itemDoubleClicked.connect(self.load_selected_recent_character)
        self.recent_list.itemSelectionChanged.connect(self.on_recent_selection_changed)
        layout.addWidget(self.recent_list)
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_main_menu)
        
        self.btn_load_recent = QPushButton("Load Selected")
        self.btn_load_recent.setEnabled(False)
        self.btn_load_recent.clicked.connect(self.load_selected_recent_character)
        
        self.resizable_buttons.extend([btn_back, self.btn_load_recent])
        
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_load_recent)
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def on_recent_selection_changed(self):
        has_sel = len(self.recent_list.selectedItems()) > 0
        if has_sel:
            selected_item = self.recent_list.selectedItems()[0]
            self.btn_load_recent.setEnabled(bool(selected_item.data(Qt.ItemDataRole.UserRole)))
        else:
            self.btn_load_recent.setEnabled(False)

    def update_recent_characters_screen(self):
        self.recent_list.clear()
        self.btn_load_recent.setEnabled(False)
        
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_characters")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            
        json_files = [f for f in os.listdir(save_dir) if f.endswith(".json")]
        if not json_files:
            item = QListWidgetItem("No saved characters found in 'saved_characters'.")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.recent_list.addItem(item)
            return

        file_paths = [os.path.join(save_dir, f) for f in json_files]
        file_paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        
        for p in file_paths:
            try:
                with open(p, 'r') as f:
                    cdata = json.load(f)
                name = cdata.get("name", os.path.splitext(os.path.basename(p))[0])
                race = cdata.get("race-name", "Unknown Race")
                level = cdata.get("level", 1)
                
                classes = cdata.get("classes", {})
                if classes:
                    first_cls = next(iter(classes.values())).get("class-name", "Unknown Class")
                else:
                    first_cls = "Unknown Class"
                
                mtime = os.path.getmtime(p)
                mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                
                item_text = f"{name} — Level {level} {race} {first_cls}  ({mtime_str})"
            except Exception:
                item_text = f"{os.path.basename(p)} (Error reading details)"
                
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, p)
            self.recent_list.addItem(item)

    def load_selected_recent_character(self):
        selected_items = self.recent_list.selectedItems()
        if not selected_items:
            return
        file_path = selected_items[0].data(Qt.ItemDataRole.UserRole)
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "Warning", "Selected file no longer exists.")
            self.update_recent_characters_screen()
            return
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Validation for DMV format
            required_keys = ["race-name", "classes", "ability-scores"]
            if not all(k in data for k in required_keys):
                raise ValueError("Invalid character file format. Expected Dungeon Master's Vault format.")
            
            if "attributes" not in data:
                data["attributes"] = {}
            if "skills" not in data:
                data["skills"] = {}
            if "equipment" not in data:
                data["equipment"] = []
            if "features-and-traits" not in data:
                data["features-and-traits"] = []
            if "name" not in data:
                data["name"] = "Unnamed Adventurer"
            if "level" not in data:
                data["level"] = 1
            
            self.character_data = data
            self.show_review()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load character: {e}")

    def on_skill_checkbox_toggled(self):
        class_name = self.current_class_name or list(CLASSES.keys())[0]
        class_info = CLASSES.get(class_name, {})
        num_to_choose = class_info.get("proficiencies", {}).get("skills", {}).get("choose", 0)
        
        checked_boxes = [cb for cb in self.skill_checkboxes if cb.isChecked()]
        limit_reached = len(checked_boxes) >= num_to_choose
        
        for cb in self.skill_checkboxes:
            if not cb.isChecked():
                cb.setEnabled(not limit_reached)

    # --- Logic ---
    def clear_all_customization(self):
        # Clear stats
        for edit in self.stat_inputs.values():
            edit.clear()
        # Clear skills
        for cb in self.skill_checkboxes:
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.setEnabled(True)
            cb.blockSignals(False)
        self.on_skill_checkbox_toggled()

    def roll_4d6(self):
        rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
        return sum(rolls[:3])

    def generate_random_stats(self):
        for edit in self.stat_inputs.values():
            edit.setText(str(self.roll_4d6()))

    def generate_random_skills(self):
        # Uncheck and re-enable all first
        for cb in self.skill_checkboxes:
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.setEnabled(True)
            cb.blockSignals(False)
        
        class_name = self.current_class_name or list(CLASSES.keys())[0]
        class_info = CLASSES.get(class_name, {})
        num_to_choose = class_info.get("proficiencies", {}).get("skills", {}).get("choose", 0)
        if not self.skill_checkboxes: return
        
        to_check = random.sample(self.skill_checkboxes, min(num_to_choose, len(self.skill_checkboxes)))
        for cb in to_check:
            cb.setChecked(True)
        self.on_skill_checkbox_toggled()

    def finalize_customization(self):
        # Handle Stats
        scores = {}
        for name, edit in self.stat_inputs.items():
            val = edit.text().strip()
            if val.isdigit():
                scores[name.lower()] = int(val)
            else:
                rolled = self.roll_4d6()
                scores[name.lower()] = rolled
                edit.setText(str(rolled))
        self.character_data["ability-scores"] = scores

        # Handle Skills
        class_name = self.current_class_name or list(CLASSES.keys())[0]
        class_info = CLASSES.get(class_name, {})
        num_to_choose = class_info.get("proficiencies", {}).get("skills", {}).get("choose", 0)
        selected_boxes = [cb for cb in self.skill_checkboxes if cb.isChecked()]
        
        if len(selected_boxes) < num_to_choose:
            needed = num_to_choose - len(selected_boxes)
            available = [cb for cb in self.skill_checkboxes if not cb.isChecked()]
            if available:
                picked = random.sample(available, min(needed, len(available)))
                for cb in picked:
                    cb.setChecked(True)
            self.on_skill_checkbox_toggled()

        self.character_data["skills"] = {
            cb.text().lower(): {"proficient": True}
            for cb in self.skill_checkboxes if cb.isChecked()
        }
        self.show_equipment()

    def finalize_equipment(self):
        final_equip_names = []
        choices_state = []
        
        # Add fixed equipment
        class_name = self.current_class_name or list(CLASSES.keys())[0]
        class_info = CLASSES.get(class_name, {})
        equip_data = class_info.get("starting_equipment", {})
        final_equip_names.extend(equip_data.get("fixed", []))
        
        # Add chosen equipment
        if self.equip_choice_groups:
            for group, choice_items in self.equip_choice_groups:
                checked_idx = group.checkedId()
                combo_text = ""
                for i, (rb, combo, opt) in enumerate(choice_items):
                    if rb.isChecked():
                        if combo:
                            final_equip_names.append(combo.currentText())
                            combo_text = combo.currentText()
                        else:
                            final_equip_names.append(opt.get("item", ""))
                choices_state.append({"index": checked_idx, "combo_text": combo_text})
        else:
            choices_state = []
            
        self.equipment_choices_history = choices_state
        
        equipment_list = []
        for raw_item in final_equip_names:
            if not raw_item: continue
            raw_item = raw_item.strip()
            parts = raw_item.split(" ", 1)
            if len(parts) == 2 and parts[0].isdigit():
                qty = int(parts[0])
                name = parts[1].rstrip("s") if parts[1].endswith("s") and not parts[1].endswith("ss") else parts[1]
            else:
                qty = 1
                name = raw_item
            
            equipped = "pack" not in name.lower()
            equipment_list.append({
                "name": name,
                "quantity": qty,
                "equipped": equipped
            })
            
        self.character_data["equipment"] = equipment_list
        self.show_review()

    def update_review_screen(self):
        self.char_obj = Character(self.character_data)
        self.char_obj.sync_attributes()
        self.review_label.setText(str(self.char_obj))

    def save_character(self):
        try:
            if hasattr(self, 'char_obj'):
                self.char_obj.sync_attributes()
            
            save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_characters")
            os.makedirs(save_dir, exist_ok=True)
            
            raw_name = self.character_data.get("name", "Unnamed Adventurer").strip() or "Unnamed Adventurer"
            safe_name = "".join(c for c in raw_name if c.isalnum() or c in (' ', '_', '-')).strip() or "character"
            file_path = os.path.join(save_dir, f"{safe_name}.json")
            
            with open(file_path, 'w') as f:
                json.dump(self.character_data, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save character: {e}")

    def export_character(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Character", "", "JSON Files (*.json)")
        if file_path:
            try:
                if hasattr(self, 'char_obj'):
                    self.char_obj.sync_attributes()
                with open(file_path, 'w') as f:
                    json.dump(self.character_data, f, indent=4)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export character: {e}")

    def import_character(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Character", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Validation for DMV format
                required_keys = ["race-name", "classes", "ability-scores"]
                if not all(k in data for k in required_keys):
                    raise ValueError("Invalid character file format. Expected Dungeon Master's Vault format.")
                
                # Ensure all DMV keys exist
                if "attributes" not in data:
                    data["attributes"] = {}
                if "skills" not in data:
                    data["skills"] = {}
                if "equipment" not in data:
                    data["equipment"] = []
                if "features-and-traits" not in data:
                    data["features-and-traits"] = []
                if "name" not in data:
                    data["name"] = "Unnamed Adventurer"
                if "level" not in data:
                    data["level"] = 1
                
                self.character_data = data
                self.show_review()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import character: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
