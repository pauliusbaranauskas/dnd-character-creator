# D&D 5e Data Definitions

WEAPONS = {
    "Simple": [
        "Club", "Dagger", "Greatclub", "Handaxe", "Javelin", 
        "Light Hammer", "Mace", "Quarterstaff", "Sickle", "Spear"
    ],
    "Martial Melee": [
        "Battleaxe", "Flail", "Glaive", "Greataxe", "Greatsword", 
        "Halberd", "Lance", "Longsword", "Maul", "Morningstar", 
        "Pike", "Rapier", "Scimitar", "Shortsword", "Trident", 
        "War Pick", "Warhammer", "Whip"
    ]
}

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
        "starting_equipment": {
            "choices": [
                {
                    "options": [
                        {"label": "(a) a Greataxe", "item": "Greataxe"},
                        {"label": "(b) any Martial Melee weapon", "type": "Martial Melee"}
                    ]
                },
                {
                    "options": [
                        {"label": "(a) two Handaxes", "item": "2 Handaxes"},
                        {"label": "(b) any Simple weapon", "type": "Simple"}
                    ]
                }
            ],
            "fixed": ["Explorer's Pack", "4 Javelins"]
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
    },
    "Dwarf": {
        "description": "Bold and hardy, dwarves are known as skilled warriors, miners, and workers of stone and metal. They can live to be more than 400 years old.",
        "ability_score_bonus": {
            "Constitution": 2,
        },
        "speed": 25,
        "traits": ["Darkvision", "Dwarven Resilience", "Stonecunning"],
    },
    "Elf": {
        "description": "Elves are a magical people of otherworldly grace, living in the world but not entirely part of it. They live in places of ethereal beauty, in the midst of ancient forests or in silvery spires glittering with faerie light.",
        "ability_score_bonus": {
            "Dexterity": 2,
        },
        "speed": 30,
        "traits": ["Darkvision", "Keen Senses", "Fey Ancestry", "Trance"],
    },
    "Halfling": {
        "description": "Halflings are small people. Some would say that their goals are as well. Perfect life for most of the halflings is cozy home far away from any trouble, but sometimes it is possible to meet an adventurer on their way to a destroy a jewel or rob a dragon.",
        "ability_score_bonus": {
            "Dexterity": 2,
        },
        "speed": 30,
        "traits": ["Lucky", "Brave", "Halfling Nimbleness"],
    }
}


TRAITS = {
    "Extra Language": {"description": "You can speak, read, and write one extra language of your choice."},
    "Darkvision": {"description": "You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can't discern color in darkness, only shades of gray."},
    "Dwarven Resilience": {"description": "You have advantage on saving throws against poison, and you have resistance against poison damage."},
    "Stonecunning": {"description": "Whenever you make an Intelligence (History) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check."},
    "Keen Senses": {"description": "You have proficiency in the Perception skill."},
    "Fey Ancestry": {"description": "You have advantage on saving throws against being charmed, and magic can't put you to sleep."},
    "Trance": {"description": "Elves don't need to sleep. Instead, they meditate deeply for 4 hours a day. After resting in this way, you gain the same benefit that a human does from 8 hours of sleep."},
    "Lucky": {"description": "When you roll a 1 on the d20 for an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll."},
    "Brave": {"description": "You have advantage on saving throws against being frightened."},
    "Halfling Nimbleness": {"description": "You can move through the space of any creature that is of a size larger than yours."}
}