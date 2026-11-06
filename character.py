from data import CLASSES, SPECIES, RACES, BACKGROUNDS, FEATS, TRAITS, STANDARD_ACTIONS

class Character:
    def __init__(self, data):
        self.data = data
        
        # Base Data from Classes/Species/Backgrounds
        self.class_data = CLASSES.get(self.character_class, {})
        self.species_data = SPECIES.get(self.character_species, {})
        self.background_data = BACKGROUNDS.get(self.character_background, {})

    @property
    def name(self):
        return self.data.get("name", "Unnamed Adventurer")

    @property
    def level(self):
        return self.data.get("level", 1)

    @property
    def character_species(self):
        return self.data.get("race-name", self.data.get("species", ""))

    @property
    def character_race(self):
        """Backward-compatibility alias for character_species."""
        return self.character_species

    @property
    def character_background(self):
        return self.data.get("background-name", "")

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
        return self.species_data.get("speed", 30)

    @property
    def proficiency_bonus(self):
        return 2

    @property
    def final_stats(self):
        """Returns final ability scores (including background bonuses)."""
        base_scores = self.data.get("ability-scores", {})
        stats = {}
        for stat in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
            stats[stat] = base_scores.get(stat.lower(), 10)
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
            # 2024 Unarmored Defense: 10 + Dex + Con
            ac = 10 + self.get_modifier("Dexterity") + self.get_modifier("Constitution")
            
        return ac

    @property
    def max_hp(self):
        # 2024 Rules: Level 1 HP = Hit Die + Con Modifier + racial/feat bonuses
        hp = self.hit_die + self.get_modifier("Constitution")
        
        feature_names = [f.get("name", "") for f in self.data.get("features-and-traits", [])]
        
        # Dwarven Toughness (+1 HP per level)
        if "Dwarven Toughness" in feature_names or self.character_species == "Dwarf":
            hp += self.level
            
        # Tough feat (+2 HP per level)
        if "Tough" in feature_names or self.background_data.get("feat") == "Tough":
            hp += 2 * self.level
            
        return hp

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
        
        traits = self.species_data.get("traits", [])
        traits_str = "\n".join([f"- {name}: {TRAITS.get(name, {}).get('description', 'N/A')}" for name in traits])

        bg_str = self.character_background if self.character_background else "None"
        feat_name = self.background_data.get("feat", "")
        feat_desc = FEATS.get(feat_name, {}).get("description", "")
        feat_display = f"{feat_name}: {feat_desc}" if feat_name else "None"

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
--- Character Sheet (2024 Rules) ---
Name: {self.name}
Species: {self.character_species}
Class: {self.character_class}
Background: {bg_str}
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
Origin Feat: {feat_display}
Equipment: {equip_display}

Class Features:
{features_str}

Species Traits:
{traits_str}

Available Actions:
{actions_str}

Special/Bonus Actions:
{special_actions_str}
-------------------------------------
"""

if __name__ == "__main__":
    test_data = {
        "name": "Angry Boy",
        "level": 1,
        "race-name": "Dwarf",
        "background-name": "Soldier",
        "classes": {
            "barbarian": {
                "class-name": "Barbarian",
                "class-level": 1,
                "hit-die": 12
            }
        },
        "ability-scores": {
            "strength": 17,
            "dexterity": 13,
            "constitution": 16,
            "intelligence": 8,
            "wisdom": 12,
            "charisma": 10
        },
        "attributes": {
            "hit-points-max": 16,
            "armor-class": 14,
            "speed": 30,
            "proficiency-bonus": 2
        },
        "skills": {
            "athletics": {"proficient": True},
            "intimidation": {"proficient": True},
            "perception": {"proficient": True},
            "survival": {"proficient": True}
        },
        "equipment": [
            {"name": "Greataxe", "quantity": 1, "equipped": True},
            {"name": "Explorer's Pack", "quantity": 1, "equipped": False}
        ],
        "features-and-traits": [
            {"name": "Dwarven Toughness", "source": "Dwarf"},
            {"name": "Savage Attacker", "source": "Soldier"}
        ]
    }
    c = Character(test_data)
    c.sync_attributes()
    print(c)
