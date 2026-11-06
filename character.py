from data import CLASSES, RACES, TRAITS, STANDARD_ACTIONS

class Character:
    def __init__(self, data):
        self.data = data
        
        # Base Data from Classes/Races
        self.class_data = CLASSES.get(self.character_class, {})
        self.race_data = RACES.get(self.character_race, {})

    @property
    def name(self):
        return self.data.get("name", "Unnamed Adventurer")

    @property
    def level(self):
        return self.data.get("level", 1)

    @property
    def character_race(self):
        return self.data.get("race-name", "")

    @property
    def character_class(self):
        classes = self.data.get("classes", {})
        if classes:
            first = next(iter(classes.values()))
            return first.get("class-name", "")
        return ""

    @property
    def hit_die(self):
        classes = self.data.get("classes", {})
        if classes:
            first = next(iter(classes.values()))
            return first.get("hit-die", 0)
        return self.class_data.get("hit_die", 0)

    @property
    def speed(self):
        return self.race_data.get("speed", 30)

    @property
    def proficiency_bonus(self):
        return 2

    @property
    def final_stats(self):
        """Returns stats including racial bonuses."""
        base_scores = self.data.get("ability-scores", {})
        bonuses = self.race_data.get("ability_score_bonus", {})
        
        stats = {}
        for stat in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
            val = base_scores.get(stat.lower(), 10)
            bonus = bonuses.get(stat, 0)
            stats[stat] = val + bonus
        return stats

    def get_modifier(self, stat_name):
        value = self.final_stats.get(stat_name, 10)
        return (value - 10) // 2

    @property
    def armor_class(self):
        # Base AC
        ac = 10 + self.get_modifier("Dexterity")
        
        # Class specific AC calculations
        if self.character_class == "Barbarian":
            # Unarmored Defense: 10 + Dex + Con
            ac = 10 + self.get_modifier("Dexterity") + self.get_modifier("Constitution")
            
        return ac

    @property
    def max_hp(self):
        # Level 1 HP: Hit Die + Con Modifier
        return self.hit_die + self.get_modifier("Constitution")

    def sync_attributes(self):
        """Syncs calculated derived attributes into the DMV attributes dictionary."""
        self.data["attributes"] = {
            "hit-points-max": self.max_hp,
            "armor-class": self.armor_class,
            "speed": self.speed,
            "proficiency-bonus": self.proficiency_bonus
        }

    def __str__(self):
        stats_str = "\n".join([f"{k:12}: {v:2} ({self.get_modifier(k):+d})" for k, v in self.final_stats.items()])
        
        prof_data = self.class_data.get("proficiencies", {})
        weapons = ", ".join(prof_data.get("weapons", []))
        armor = ", ".join(prof_data.get("armor", []))
        saves = ", ".join(self.class_data.get("saves", []))
        
        features_str = "\n".join([f"- {name}: {desc}" for name, desc in self.class_data.get("features", {}).items()])
        
        traits = self.race_data.get("traits", [])
        traits_str = "\n".join([f"- {name}: {TRAITS.get(name, {}).get('description', 'N/A')}" for name in traits])

        # Available Actions
        actions = []
        for name, desc in STANDARD_ACTIONS.items():
            actions.append(f"- {name}: {desc}")
        
        # Check features for bonus actions or special actions
        special_actions = []
        for name, desc in self.class_data.get("features", {}).items():
            if "action" in desc.lower():
                special_actions.append(f"- {name}: {desc}")
        
        actions_str = "\n".join(actions)
        special_actions_str = "\n".join(special_actions) if special_actions else "None"
        
        skills_dict = self.data.get("skills", {})
        skills_list = [k.title() for k, v in skills_dict.items() if v.get("proficient")]
        skills_display = ", ".join(skills_list) if skills_list else "None"
        
        equip_items = self.data.get("equipment", [])
        if equip_items:
            equip_display = ", ".join([
                f"{item['quantity']}x {item['name']}" if item.get('quantity', 1) > 1 else item['name']
                for item in equip_items
            ])
        else:
            equip_display = "None"
        
        return f"""
--- Character Sheet ---
Name: {self.name}
Race: {self.character_race}
Class: {self.character_class}
Level: {self.level}

HP: {self.max_hp}
Hit Dice: {self.level}d{self.hit_die}
AC: {self.armor_class}
Speed: {self.speed} ft.
Proficiency Bonus: +{self.proficiency_bonus}

Stats:
{stats_str}

Saving Throws: {saves}
Armor Proficiencies: {armor}
Weapon Proficiencies: {weapons}
Skills: {skills_display}
Equipment: {equip_display}

Features:
{features_str}

Racial Traits:
{traits_str}

Available Actions:
{actions_str}

Special/Bonus Actions:
{special_actions_str}
-----------------------
"""

if __name__ == "__main__":
    test_data = {
        "name": "Angry Boy",
        "level": 1,
        "race-name": "Human",
        "classes": {
            "barbarian": {
                "class-name": "Barbarian",
                "class-level": 1,
                "hit-die": 12
            }
        },
        "ability-scores": {
            "strength": 10,
            "dexterity": 12,
            "constitution": 12,
            "intelligence": 17,
            "wisdom": 8,
            "charisma": 16
        },
        "attributes": {
            "hit-points-max": 13,
            "armor-class": 12,
            "speed": 30,
            "proficiency-bonus": 2
        },
        "skills": {
            "intimidation": {"proficient": True},
            "nature": {"proficient": True}
        },
        "equipment": [
            {"name": "Explorer's Pack", "quantity": 1, "equipped": False},
            {"name": "Javelin", "quantity": 4, "equipped": True},
            {"name": "Greataxe", "quantity": 1, "equipped": True},
            {"name": "Handaxe", "quantity": 2, "equipped": True}
        ],
        "features-and-traits": [
            {"name": "Extra Language", "source": "Human"},
            {"name": "Rage", "source": "Barbarian"}
        ]
    }
    c = Character(test_data)
    c.sync_attributes()
    print(c)
