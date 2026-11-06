# D&D 5e (2024 Ruleset) Data Definitions

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
        "description": "Barbarians are mighty warriors powered by primal fury. In the 2024 rules, they harness Weapon Mastery, extended Rage, and relentless instincts.",
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
            "Rage": "As a bonus action, you enter a rage for up to 10 minutes. While raging, you gain advantage on Strength checks and saving throws, a bonus to damage rolls with Strength melee attacks (+2), and resistance to bludgeoning, piercing, and slashing damage. (2 uses per long rest; regain 1 use on short rest)",
            "Unarmored Defense": "While you are not wearing any armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier. You can use a shield and still gain this benefit.",
            "Weapon Mastery": "Your training with weapons allows you to use the mastery properties of two kinds of weapons of your choice (e.g., Cleave, Graze, Nick, Push, Sap, Slow, Topple, Vex)."
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

SPECIES = {
    "Human": {
        "description": "Found across the multiverse, humans are renowned for their adaptability, resourcefulness, and ambition.",
        "speed": 30,
        "size": "Medium",
        "traits": ["Resourceful", "Skillful", "Versatile"],
    },
    "Dwarf": {
        "description": "Bold and hardy, dwarves are warriors and artisans shaped by their deep connection to mountains and stone.",
        "speed": 30,
        "size": "Medium",
        "traits": ["Darkvision", "Dwarven Resilience", "Dwarven Toughness", "Stonecunning"],
    },
    "Elf": {
        "description": "Elves are magical beings of otherworldly grace and deep awareness, steeped in woodland glades or silvery spires.",
        "speed": 30,
        "size": "Medium",
        "traits": ["Darkvision", "Elven Lineage", "Fey Ancestry", "Keen Senses", "Trance"],
    },
    "Halfling": {
        "description": "Small, courageous, and remarkably nimble folk who make up for their stature with legendary luck and stealth.",
        "speed": 30,
        "size": "Small",
        "traits": ["Brave", "Halfling Nimbleness", "Luck", "Naturally Stealthy"],
    }
}

# Alias for backward compatibility
RACES = SPECIES

BACKGROUNDS = {
    "Acolyte": {
        "description": "You devoted yourself to service in a temple, learning sacred rites and holy mysteries.",
        "ability_scores": ["Intelligence", "Wisdom", "Charisma"],
        "feat": "Magic Initiate (Cleric)",
        "skills": ["Insight", "Religion"]
    },
    "Artisan": {
        "description": "You began learning a trade in your youth, creating goods with precision and pride.",
        "ability_scores": ["Strength", "Dexterity", "Intelligence"],
        "feat": "Crafter",
        "skills": ["Investigation", "Persuasion"]
    },
    "Charlatan": {
        "description": "You spent your formative years learning how to read people, deception, and the art of the con.",
        "ability_scores": ["Dexterity", "Constitution", "Charisma"],
        "feat": "Skilled",
        "skills": ["Deception", "Sleight of Hand"]
    },
    "Criminal": {
        "description": "You learned survival in the shadows of the law, picking locks and navigating the underworld.",
        "ability_scores": ["Dexterity", "Constitution", "Intelligence"],
        "feat": "Alert",
        "skills": ["Sleight of Hand", "Stealth"]
    },
    "Entertainer": {
        "description": "You thrive in the spotlight, captivating audiences with music, storytelling, and dance.",
        "ability_scores": ["Strength", "Dexterity", "Charisma"],
        "feat": "Musician",
        "skills": ["Acrobatics", "Performance"]
    },
    "Farmer": {
        "description": "You grew up working the land, cultivating stamina and practical knowledge of nature.",
        "ability_scores": ["Strength", "Constitution", "Wisdom"],
        "feat": "Tough",
        "skills": ["Animal Handling", "Nature"]
    },
    "Guard": {
        "description": "You stood watch on city ramparts or protected gates, developing vigilance and physical discipline.",
        "ability_scores": ["Strength", "Intelligence", "Wisdom"],
        "feat": "Alert",
        "skills": ["Athletics", "Perception"]
    },
    "Guide": {
        "description": "You navigated dangerous wilderness, tracing paths through untamed lands.",
        "ability_scores": ["Dexterity", "Constitution", "Wisdom"],
        "feat": "Magic Initiate (Druid)",
        "skills": ["Stealth", "Survival"]
    },
    "Hermit": {
        "description": "You lived in quiet isolation, studying the mysteries of nature and internal wisdom.",
        "ability_scores": ["Constitution", "Wisdom", "Charisma"],
        "feat": "Healer",
        "skills": ["Medicine", "Religion"]
    },
    "Merchant": {
        "description": "You mastered the flow of goods and currency, negotiating trades across ports and markets.",
        "ability_scores": ["Constitution", "Intelligence", "Charisma"],
        "feat": "Lucky",
        "skills": ["Animal Handling", "Persuasion"]
    },
    "Noble": {
        "description": "You were raised among aristocracy and luxury, learning diplomacy, etiquette, and authority.",
        "ability_scores": ["Strength", "Intelligence", "Charisma"],
        "feat": "Skilled",
        "skills": ["History", "Persuasion"]
    },
    "Sage": {
        "description": "You spent years studying manuscripts in libraries, unearthing history and arcane secrets.",
        "ability_scores": ["Constitution", "Intelligence", "Wisdom"],
        "feat": "Magic Initiate (Wizard)",
        "skills": ["Arcana", "History"]
    },
    "Sailor": {
        "description": "You braved stormy waters and learned the rigors of seafaring life alongside fellow sailors.",
        "ability_scores": ["Strength", "Dexterity", "Wisdom"],
        "feat": "Tavern Brawler",
        "skills": ["Athletics", "Perception"]
    },
    "Scribe": {
        "description": "You recorded history, legal deeds, and scholarly treatises with meticulous focus.",
        "ability_scores": ["Dexterity", "Intelligence", "Wisdom"],
        "feat": "Skilled",
        "skills": ["Investigation", "Perception"]
    },
    "Soldier": {
        "description": "You trained for military campaigns, mastering formations, combat endurance, and tactical battle.",
        "ability_scores": ["Strength", "Dexterity", "Constitution"],
        "feat": "Savage Attacker",
        "skills": ["Athletics", "Intimidation"]
    },
    "Wayfarer": {
        "description": "You grew up on the move, picking pockets and relying on quick reflexes and instincts.",
        "ability_scores": ["Dexterity", "Wisdom", "Charisma"],
        "feat": "Lucky",
        "skills": ["Insight", "Stealth"]
    }
}

FEATS = {
    "Alert": {"description": "You gain a bonus to Initiative rolls equal to your Proficiency Bonus, and you can swap your initiative roll with a willing ally."},
    "Crafter": {"description": "You gain proficiency with three Artisan's Tools, and you get a 20% discount on nonmagical items."},
    "Healer": {"description": "You can reroll 1s on healing dice, and you can expend a Healer's Kit use to heal an ally."},
    "Lucky": {"description": "You have Luck Points equal to your Proficiency Bonus to gain Advantage on d20 rolls or give Disadvantage to attackers."},
    "Magic Initiate (Cleric)": {"description": "You learn two cantrips and one 1st-level spell from the Cleric spell list."},
    "Magic Initiate (Druid)": {"description": "You learn two cantrips and one 1st-level spell from the Druid spell list."},
    "Magic Initiate (Wizard)": {"description": "You learn two cantrips and one 1st-level spell from the Wizard spell list."},
    "Musician": {"description": "You can give Heroic Inspiration to allies after completing a short or long rest."},
    "Savage Attacker": {"description": "Once per turn when you hit with a weapon attack, you can roll the weapon's damage dice twice and use the higher roll."},
    "Skilled": {"description": "You gain proficiency in three skills or tools of your choice."},
    "Tavern Brawler": {"description": "Your unarmed strikes deal 1d4 + Strength modifier, and you can push a creature 5 feet once per turn on hit."},
    "Tough": {"description": "Your hit point maximum increases by 2 for each level your character has (starting at +2 at level 1)."}
}

TRAITS = {
    "Resourceful": {"description": "You gain Heroic Inspiration whenever you finish a Long Rest."},
    "Skillful": {"description": "You gain proficiency in one skill of your choice."},
    "Versatile": {"description": "You gain one Origin Feat of your choice."},
    "Darkvision": {"description": "You can see in dim light within 60 feet (120 feet for Dwarves) as if it were bright light, and in darkness as if it were dim light. You can't discern color in darkness, only shades of gray."},
    "Dwarven Resilience": {"description": "You have advantage on saving throws against poison, and you have resistance against poison damage."},
    "Dwarven Toughness": {"description": "Your hit point maximum increases by 1, and it increases by 1 every time you gain a level."},
    "Stonecunning": {"description": "As a bonus action, you gain Tremorsense with a range of 60 feet for 10 minutes while on a stone surface (uses equal to proficiency bonus per long rest)."},
    "Elven Lineage": {"description": "You have a magical lineage that grants you mystical gifts and cantrips."},
    "Fey Ancestry": {"description": "You have advantage on saving throws against being charmed, and magic can't put you to sleep."},
    "Keen Senses": {"description": "You have proficiency in the Perception skill."},
    "Trance": {"description": "You don't need to sleep. Instead, you meditate deeply for 4 hours a day to gain the same benefit that a human does from 8 hours of sleep."},
    "Brave": {"description": "You have advantage on saving throws against being frightened."},
    "Halfling Nimbleness": {"description": "You can move through the space of any creature that is of a size larger than yours."},
    "Luck": {"description": "When you roll a 1 on the d20 for an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll."},
    "Naturally Stealthy": {"description": "You can take the Hide action even when you are only obscured by a creature that is at least one size larger than you."}
}

STATS = {
    "Strength": {"description": "Measures physical power and athletic training. Important for: Barbarian, Fighter, Paladin."},
    "Dexterity": {"description": "Measures agility, reflexes, and balance. Important for: Monk, Ranger, Rogue."},
    "Constitution": {"description": "Measures health, stamina, and vital force. Important for: Everyone (affects Hit Points)."},
    "Intelligence": {"description": "Measures mental acuity, information recall, and analytical skill. Important for: Wizard."},
    "Wisdom": {"description": "Measures awareness, intuition, and insight. Important for: Cleric, Druid."},
    "Charisma": {"description": "Measures confidence, eloquence, and leadership. Important for: Bard, Sorcerer, Warlock."}
}

STANDARD_ACTIONS = {
    "Attack": "Make one melee or ranged attack.",
    "Dash": "Gain extra movement for the current turn equal to your speed.",
    "Disengage": "Your movement doesn't provoke opportunity attacks for the rest of the turn.",
    "Dodge": "Attack rolls against you have disadvantage if you can see the attacker, and you make Dexterity saving throws with advantage.",
    "Help": "You help another creature with a task, giving them advantage on the next ability check it makes, or you provide help in attacking a creature.",
    "Hide": "Make a Dexterity (Stealth) check in an attempt to hide.",
    "Ready": "You wait for a particular circumstance before you act, which lets you take your action as a reaction before the start of your next turn.",
    "Search": "You devote your attention to finding something, making a Wisdom (Perception) check or an Intelligence (Investigation) check.",
    "Use an Object": "You normally interact with an object while doing something else, but if the object requires your action, you take this action."
}
