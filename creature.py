# Creature base class and type system
from dataclasses import dataclass, field
from typing import List, Optional
import random

# Elemental types
TYPE_FIRE = "fire"
TYPE_WATER = "water"
TYPE_EARTH = "earth"
TYPE_AIR = "air"
TYPE_LIGHTNING = "lightning"
TYPE_SHADOW = "shadow"
TYPE_NATURE = "nature"
TYPE_ICE = "ice"

# Type effectiveness chart: attacker -> defender -> multiplier
# Each type is strong (2x) against 2 types and weak (0.5x) against 2 types
g_type_chart = {
    TYPE_FIRE: {TYPE_FIRE: 0.5, TYPE_WATER: 0.5, TYPE_NATURE: 2.0, TYPE_ICE: 2.0},
    TYPE_WATER: {TYPE_WATER: 0.5, TYPE_FIRE: 2.0, TYPE_EARTH: 2.0, TYPE_NATURE: 0.5},
    TYPE_EARTH: {TYPE_EARTH: 0.5, TYPE_LIGHTNING: 2.0, TYPE_FIRE: 2.0, TYPE_AIR: 0.5},
    TYPE_AIR: {TYPE_AIR: 0.5, TYPE_EARTH: 2.0, TYPE_NATURE: 2.0, TYPE_LIGHTNING: 0.5},
    TYPE_LIGHTNING: {TYPE_LIGHTNING: 0.5, TYPE_WATER: 2.0, TYPE_AIR: 2.0, TYPE_EARTH: 0.5},
    TYPE_SHADOW: {TYPE_SHADOW: 0.5, TYPE_NATURE: 2.0, TYPE_AIR: 2.0, TYPE_FIRE: 0.5},
    TYPE_NATURE: {TYPE_NATURE: 0.5, TYPE_WATER: 2.0, TYPE_EARTH: 2.0, TYPE_ICE: 0.5},
    TYPE_ICE: {TYPE_ICE: 0.5, TYPE_AIR: 2.0, TYPE_SHADOW: 2.0, TYPE_FIRE: 0.5},
}

def get_type_multiplier(attacker_type: str, defender_type: str) -> float:
    return g_type_chart.get(attacker_type, {}).get(defender_type, 1.0)


@dataclass
class Ability:
    name: str
    power: int  # base damage (0 for status moves)
    accuracy: int  # percentage chance to hit (1-100)
    element: str  # elemental type of the ability
    description: str = ""


@dataclass
class Creature:
    name: str
    element: str
    base_hp: int
    base_atk: int
    base_def: int
    base_spd: int
    abilities: List[Ability] = field(default_factory=list)
    sprite_path: Optional[str] = None  # path to sprite image
    description: str = ""

    # Instance-specific stats (set when creature is created/caught)
    level: int = 1
    experience: int = 0
    current_hp: int = field(init=False)

    def __post_init__(self):
        self.current_hp = self.max_hp

    @property
    def max_hp(self) -> int:
        return int(self.base_hp * (1 + (self.level - 1) * 0.1))  # 10% increase per level

    @property
    def atk(self) -> int:
        return int(self.base_atk * (1 + (self.level - 1) * 0.08))  # 8% increase per level

    @property
    def defense(self) -> int:
        return int(self.base_def * (1 + (self.level - 1) * 0.08))

    @property
    def spd(self) -> int:
        return int(self.base_spd * (1 + (self.level - 1) * 0.05))  # 5% increase per level

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: int) -> int:
        actual_damage = max(1, damage)  # minimum 1 damage
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def heal(self, amount: int) -> int:
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp  # actual amount healed

    def full_heal(self):
        self.current_hp = self.max_hp

    def gain_experience(self, amount: int) -> bool:
        self.experience += amount
        exp_needed = self.exp_to_next_level()
        leveled_up = False
        while self.experience >= exp_needed and self.level < 100:  # max level 100
            self.experience -= exp_needed
            self.level += 1
            leveled_up = True
            exp_needed = self.exp_to_next_level()
        return leveled_up

    def exp_to_next_level(self) -> int:
        return self.level * 100  # simple linear scaling

    def calculate_damage(self, ability: Ability, defender: 'Creature') -> int:
        if ability.power == 0:
            return 0  # status move

        # Basic damage formula
        base_damage = (ability.power * (self.atk / defender.defense)) * (self.level / 5 + 1)

        # Type effectiveness
        type_mult = get_type_multiplier(ability.element, defender.element)

        # Random variance (85-100%)
        variance = random.uniform(0.85, 1.0)

        return int(base_damage * type_mult * variance)

    def use_ability(self, ability: Ability, defender: 'Creature') -> dict:
        result = {
            "attacker": self.name,
            "defender": defender.name,
            "ability": ability.name,
            "hit": False,
            "damage": 0,
            "type_effectiveness": 1.0,
            "defender_fainted": False,
        }

        # Accuracy check
        if random.randint(1, 100) > ability.accuracy:
            return result  # missed

        result["hit"] = True
        result["type_effectiveness"] = get_type_multiplier(ability.element, defender.element)
        result["damage"] = self.calculate_damage(ability, defender)
        defender.take_damage(result["damage"])
        result["defender_fainted"] = not defender.is_alive()

        return result


# Some starter abilities (reduced power for longer battles)
g_abilities = {
    "tackle": Ability("Tackle", power=20, accuracy=100, element=TYPE_EARTH, description="A basic physical attack"),
    "ember": Ability("Ember", power=20, accuracy=100, element=TYPE_FIRE, description="A small flame attack"),
    "water_gun": Ability("Water Gun", power=20, accuracy=100, element=TYPE_WATER, description="A spray of water"),
    "gust": Ability("Gust", power=20, accuracy=100, element=TYPE_AIR, description="A blast of wind"),
    "flame_burst": Ability("Flame Burst", power=35, accuracy=90, element=TYPE_FIRE, description="A powerful fire blast"),
    "tidal_wave": Ability("Tidal Wave", power=35, accuracy=90, element=TYPE_WATER, description="A crashing wave"),
    "earthquake": Ability("Earthquake", power=35, accuracy=90, element=TYPE_EARTH, description="Shakes the ground"),
    "hurricane": Ability("Hurricane", power=35, accuracy=90, element=TYPE_AIR, description="A violent windstorm"),
    # Lightning abilities
    "spark": Ability("Spark", power=20, accuracy=100, element=TYPE_LIGHTNING, description="A small electric jolt"),
    "thunderbolt": Ability("Thunderbolt", power=35, accuracy=90, element=TYPE_LIGHTNING, description="A powerful lightning strike"),
    # Shadow abilities
    "shadow_bite": Ability("Shadow Bite", power=20, accuracy=100, element=TYPE_SHADOW, description="A bite from the darkness"),
    "dark_pulse": Ability("Dark Pulse", power=35, accuracy=90, element=TYPE_SHADOW, description="A wave of dark energy"),
    # Nature abilities
    "vine_whip": Ability("Vine Whip", power=20, accuracy=100, element=TYPE_NATURE, description="Strikes with thorny vines"),
    "solar_beam": Ability("Solar Beam", power=35, accuracy=90, element=TYPE_NATURE, description="A beam of concentrated sunlight"),
    # Ice abilities
    "frost_bite": Ability("Frost Bite", power=20, accuracy=100, element=TYPE_ICE, description="A freezing cold bite"),
    "blizzard": Ability("Blizzard", power=35, accuracy=90, element=TYPE_ICE, description="A devastating snowstorm"),
}


# Starter creatures (emoji placeholders for sprites)
def create_creature(template_name: str, level: int = 1) -> Optional[Creature]:
    """Factory function to create a creature from a template."""
    templates = get_creature_templates()
    if template_name not in templates:
        return None
    creature = templates[template_name]
    creature.level = level
    creature.current_hp = creature.max_hp
    return creature


def get_creature_templates() -> dict:
    """Returns a dict of creature templates (creates fresh instances each call)."""
    return {
        # Fire creatures
        "emberling": Creature(
            name="Emberling",
            element=TYPE_FIRE,
            base_hp=45, base_atk=50, base_def=35, base_spd=60,
            abilities=[g_abilities["ember"], g_abilities["tackle"]],
            sprite_path="🦎",  # lizard emoji placeholder
            description="A small salamander with a flame-tipped tail.",
        ),
        "phoenixlet": Creature(
            name="Phoenixlet",
            element=TYPE_FIRE,
            base_hp=40, base_atk=60, base_def=30, base_spd=70,
            abilities=[g_abilities["ember"], g_abilities["gust"]],
            sprite_path="🐦",  # bird emoji placeholder
            description="A young firebird still learning to control its flames.",
        ),
        "infernoboar": Creature(
            name="Infernoboar",
            element=TYPE_FIRE,
            base_hp=70, base_atk=65, base_def=50, base_spd=35,
            abilities=[g_abilities["flame_burst"], g_abilities["tackle"]],
            sprite_path="🐗",  # boar emoji placeholder
            description="A fierce boar wreathed in flames.",
        ),

        # Water creatures
        "bubblefin": Creature(
            name="Bubblefin",
            element=TYPE_WATER,
            base_hp=50, base_atk=40, base_def=45, base_spd=55,
            abilities=[g_abilities["water_gun"], g_abilities["tackle"]],
            sprite_path="🐟",  # fish emoji placeholder
            description="A cheerful fish that blows bubbles when happy.",
        ),
        "shellsnap": Creature(
            name="Shellsnap",
            element=TYPE_WATER,
            base_hp=55, base_atk=55, base_def=65, base_spd=25,
            abilities=[g_abilities["water_gun"], g_abilities["tackle"]],
            sprite_path="🦀",  # crab emoji placeholder
            description="A tough crab with pincers that can crack stone.",
        ),
        "tidalserpent": Creature(
            name="Tidalserpent",
            element=TYPE_WATER,
            base_hp=60, base_atk=70, base_def=40, base_spd=50,
            abilities=[g_abilities["tidal_wave"], g_abilities["water_gun"]],
            sprite_path="🐍",  # snake emoji placeholder
            description="A sea serpent that commands the waves.",
        ),

        # Earth creatures
        "pebblehog": Creature(
            name="Pebblehog",
            element=TYPE_EARTH,
            base_hp=55, base_atk=45, base_def=60, base_spd=30,
            abilities=[g_abilities["tackle"], g_abilities["earthquake"]],
            sprite_path="🦔",  # hedgehog emoji placeholder
            description="A hedgehog with stone spines.",
        ),
        "boulderback": Creature(
            name="Boulderback",
            element=TYPE_EARTH,
            base_hp=80, base_atk=50, base_def=70, base_spd=20,
            abilities=[g_abilities["earthquake"], g_abilities["tackle"]],
            sprite_path="🐢",  # turtle emoji placeholder
            description="An ancient turtle with a mountain on its shell.",
        ),
        "tunnelmole": Creature(
            name="Tunnelmole",
            element=TYPE_EARTH,
            base_hp=50, base_atk=60, base_def=45, base_spd=45,
            abilities=[g_abilities["tackle"], g_abilities["earthquake"]],
            sprite_path="🐀",  # rat emoji placeholder (mole not available)
            description="A mole that digs through solid rock.",
        ),

        # Air creatures
        "breezewing": Creature(
            name="Breezewing",
            element=TYPE_AIR,
            base_hp=40, base_atk=45, base_def=35, base_spd=75,
            abilities=[g_abilities["gust"], g_abilities["tackle"]],
            sprite_path="🦅",  # eagle emoji placeholder
            description="A swift eagle that rides the wind currents.",
        ),
        "cloudhopper": Creature(
            name="Cloudhopper",
            element=TYPE_AIR,
            base_hp=45, base_atk=40, base_def=40, base_spd=65,
            abilities=[g_abilities["gust"], g_abilities["tackle"]],
            sprite_path="🐰",  # rabbit emoji placeholder
            description="A fluffy rabbit that can leap into the clouds.",
        ),
        "stormbat": Creature(
            name="Stormbat",
            element=TYPE_AIR,
            base_hp=50, base_atk=65, base_def=35, base_spd=70,
            abilities=[g_abilities["hurricane"], g_abilities["gust"]],
            sprite_path="🦇",  # bat emoji placeholder
            description="A bat that summons thunderstorms.",
        ),

        # Lightning creatures
        "sparkrat": Creature(
            name="Sparkrat",
            element=TYPE_LIGHTNING,
            base_hp=40, base_atk=55, base_def=30, base_spd=80,
            abilities=[g_abilities["spark"], g_abilities["tackle"]],
            sprite_path="🐁",  # mouse emoji placeholder
            description="A tiny mouse crackling with static electricity.",
        ),
        "thunderwolf": Creature(
            name="Thunderwolf",
            element=TYPE_LIGHTNING,
            base_hp=55, base_atk=70, base_def=45, base_spd=65,
            abilities=[g_abilities["thunderbolt"], g_abilities["spark"]],
            sprite_path="🐺",  # wolf emoji placeholder
            description="A fierce wolf with lightning in its fur.",
        ),
        "stormeel": Creature(
            name="Stormeel",
            element=TYPE_LIGHTNING,
            base_hp=50, base_atk=65, base_def=40, base_spd=60,
            abilities=[g_abilities["thunderbolt"], g_abilities["spark"]],
            sprite_path="🐉",  # dragon emoji placeholder (electric eel)
            description="An eel that generates massive electric shocks.",
        ),

        # Shadow creatures
        "duskcat": Creature(
            name="Duskcat",
            element=TYPE_SHADOW,
            base_hp=45, base_atk=60, base_def=35, base_spd=70,
            abilities=[g_abilities["shadow_bite"], g_abilities["tackle"]],
            sprite_path="🐈‍⬛",  # black cat emoji placeholder
            description="A sleek cat that melts into shadows.",
        ),
        "nightowl": Creature(
            name="Nightowl",
            element=TYPE_SHADOW,
            base_hp=50, base_atk=55, base_def=45, base_spd=55,
            abilities=[g_abilities["dark_pulse"], g_abilities["shadow_bite"]],
            sprite_path="🦉",  # owl emoji placeholder
            description="An owl that hunts in complete darkness.",
        ),
        "voidspider": Creature(
            name="Voidspider",
            element=TYPE_SHADOW,
            base_hp=55, base_atk=70, base_def=50, base_spd=45,
            abilities=[g_abilities["dark_pulse"], g_abilities["shadow_bite"]],
            sprite_path="🕷️",  # spider emoji placeholder
            description="A spider that weaves webs of pure darkness.",
        ),

        # Nature creatures
        "sproutling": Creature(
            name="Sproutling",
            element=TYPE_NATURE,
            base_hp=50, base_atk=45, base_def=50, base_spd=45,
            abilities=[g_abilities["vine_whip"], g_abilities["tackle"]],
            sprite_path="🐛",  # caterpillar emoji placeholder
            description="A small creature with leaves growing from its back.",
        ),
        "thornbear": Creature(
            name="Thornbear",
            element=TYPE_NATURE,
            base_hp=75, base_atk=60, base_def=55, base_spd=30,
            abilities=[g_abilities["solar_beam"], g_abilities["vine_whip"]],
            sprite_path="🐻",  # bear emoji placeholder
            description="A bear covered in thorny vines.",
        ),
        "florafox": Creature(
            name="Florafox",
            element=TYPE_NATURE,
            base_hp=45, base_atk=55, base_def=40, base_spd=70,
            abilities=[g_abilities["vine_whip"], g_abilities["solar_beam"]],
            sprite_path="🦊",  # fox emoji placeholder
            description="A graceful fox with flowers in its fur.",
        ),

        # Ice creatures
        "frostpup": Creature(
            name="Frostpup",
            element=TYPE_ICE,
            base_hp=45, base_atk=50, base_def=45, base_spd=55,
            abilities=[g_abilities["frost_bite"], g_abilities["tackle"]],
            sprite_path="🐕",  # dog emoji placeholder
            description="A playful pup with icy breath.",
        ),
        "glacialbear": Creature(
            name="Glacialbear",
            element=TYPE_ICE,
            base_hp=80, base_atk=65, base_def=60, base_spd=25,
            abilities=[g_abilities["blizzard"], g_abilities["frost_bite"]],
            sprite_path="🐻‍❄️",  # polar bear emoji placeholder
            description="A massive bear from the frozen tundra.",
        ),
        "crystalbird": Creature(
            name="Crystalbird",
            element=TYPE_ICE,
            base_hp=40, base_atk=55, base_def=35, base_spd=75,
            abilities=[g_abilities["blizzard"], g_abilities["frost_bite"]],
            sprite_path="🐧",  # penguin emoji placeholder
            description="A bird with feathers made of ice crystals.",
        ),
    }
