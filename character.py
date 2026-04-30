from data import CLASSES, RACES

class Character:
    def __init__(self, character_class_name, character_race_name):
        self.character_class = character_class_name
        self.character_race = character_race_name
        
        # Base Data from Classes/Races
        self.class_data = CLASSES.get(character_class_name, {})
        self.race_data = RACES.get(character_race_name, {})

        # Ability Scores (Base)
        self.base_stats = {
            "Strength": 0,
            "Dexterity": 0,
            "Constitution": 0,
            "Intelligence": 0,
            "Wisdom": 0,
            "Charisma": 0
        }

        # Derived values
        self.hit_die = self.class_data.get("hit_die", 0)
        self.speed = self.race_data.get("speed", 0)
        self.skills = []

    def set_stats(self, stats_dict):
        """Sets the base stats and applies racial bonuses."""
        for stat, value in stats_dict.items():
            if stat in self.base_stats:
                self.base_stats[stat] = value

    def set_skills(self, skills_list):
        self.skills = skills_list

    @property
    def final_stats(self):
        """Returns stats including racial bonuses."""
        bonuses = self.race_data.get("ability_score_bonus", {})
        return {stat: val + bonuses.get(stat, 0) for stat, val in self.base_stats.items()}

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

    def __str__(self):
        stats_str = "\n".join([f"{k:12}: {v:2} ({self.get_modifier(k):+d})" for k, v in self.final_stats.items()])
        
        prof_data = self.class_data.get("proficiencies", {})
        weapons = ", ".join(prof_data.get("weapons", []))
        armor = ", ".join(prof_data.get("armor", []))
        saves = ", ".join(self.class_data.get("saves", []))
        
        features_str = "\n".join([f"- {name}: {desc}" for name, desc in self.class_data.get("features", {}).items()])
        
        return f"""
--- Character Sheet ---
Race: {self.character_race}
Class: {self.character_class}
Level: 1

HP: {self.max_hp}
Hit Dice: 1d{self.hit_die}
AC: {self.armor_class}
Speed: {self.speed} ft.

Stats:
{stats_str}

Saving Throws: {saves}
Armor Proficiencies: {armor}
Weapon Proficiencies: {weapons}
Skills: {', '.join(self.skills) if self.skills else 'None'}

Features:
{features_str}
-----------------------
"""

if __name__ == "__main__":
    # Test setup
    c = Character("Barbarian", "Human")
    c.set_stats({
        "Strength": 15,
        "Dexterity": 14,
        "Constitution": 13,
        "Intelligence": 10,
        "Wisdom": 12,
        "Charisma": 8
    })
    print(c)
