class Character:
    def __init__(self, character_class):
        self.character_class = character_class
        # self.character_race = character_race

        self.primary_ability = ""
        self.hit_die = 0

        self.strength = 0
        self.constitution = 0
        self.dexterity = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.armor_class = 0

        self.str_save_proficient = False
        self.con_save_proficient = False
        self.dex_save_proficient = False
        self.wis_save_proficient = False
        self.int_save_proficient = False
        self.cha_save_proficient = False
        self.proficiency_bonus = 2

        self.weapon_mastery_slots =0
        self.simple_weapons_proficient = False
        self.martial_weapons_proficient = False

        self.light_armor_proficient = False
        self.medium_armor_proficient = False

        self.shield = False

        self.rage_slots = 0
        self.rage_damage_bonus = 0

        self.bludgeoning_resistance = False
        self.piercing_resistance = False
        self.slashing_resistance = False

        self.handaxe_mastery = False
        self.greataxe_mastery = False

        if self.character_class == "Barbarian":
            print("Setting up Barbarian")
            self.settup_barbarian()

    def get_modifier(self, ability):
        return (ability - 10) // 2

    def settup_barbarian(self):
        self.primary_ability = "str"
        self.hit_die = 12
        self.str_save_proficient = True
        self.con_save_proficient = True
        self.simple_weapons_proficient = True
        self.martial_weapons_proficient = True
        self.light_armor_proficient = True
        self.medium_armor_proficient = True
        self.shield = True
        self.rage_slots = 2
        self.rage_damage_bonus = 2
        self.weapon_mastery_slots = 2
        self.bludgeoning_resistance = True
        self.piercing_resistance = True
        self.slashing_resistance = True
        self.armor_class = 10 + self.get_modifier(self.dexterity) + self.get_modifier(self.constitution)
        self.handaxe_mastery = True
        self.greataxe_mastery = True

    def __str__(self):
        return f"""Character Class: {self.character_class}
Strength: {self.strength}
Constitution: {self.constitution}
Dexterity: {self.dexterity}
Intelligence: {self.intelligence}
Wisdom: {self.wisdom}
Charisma: {self.charisma}
"""
