# D&D 5e Data Definitions

CLASSES = {
    "Barbarian": {
        "description": "Barbarians are brute fighters. Fueled by their rage they ravage battlefields seeding a fear in their opponents.",
        "hit_die": 12,
        "primary_ability": "Strength",
        "saves": ["Strength", "Constitution"],
        "proficiencies": {
            "weapons": ["Simple", "Martial"],
            "armor": ["Light", "Medium", "Shields"],
            "skills": {
                "choose": 2,
                "options": ["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"]
            }
        },
        "features": {
            "Rage": "You can enter a rage as a bonus action. You gain advantage on Strength checks and saving throws, a bonus to damage rolls with Strength weapons (+2), and resistance to bludgeoning, piercing, and slashing damage. (2 uses per long rest)",
            "Unarmored Defense": "While you are not wearing any armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier. You can use a shield and still gain this benefit.",
            "Weapon Mastery": "Your training with weapons allows you to use the mastery properties of two kinds of weapons of your choice."
        },
    }
}

RACES = {
    "Human": {
        "description": "Humans are the most adaptable and ambitious people among the common races. They vary widely in physical appearance and culture.",
        "ability_score_bonus": {
            "Strength": 1,
            "Dexterity": 1,
            "Constitution": 1,
            "Intelligence": 1,
            "Wisdom": 1,
            "Charisma": 1,
        },
        "speed": 30,
        "traits": ["Extra Language"],
    }
}
