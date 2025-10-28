# Here were are importing libraries to help and make this script itself more concise.
# random -> Can generate random values which are used for damage numbers in this script.
# time -> Operations involving time. We use "time.sleep()" in this script to give the user more time to read information presented.
# os -> Allows interaction with the operating system itself, here used to clear the terminal emulator output.
import random, time, os

# Used for clear the terminal emulator output. This function evaluates if the current operating system is Winblows and uses the "cls" command, otherwise, if it is Unix-like or Unix-based, the "clear" command is used instead.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# This is a generic superclass used to define generic character attributes such as health and attack damage.
class Character:
    # __init__ is a special function that runs when we create a new "Character".
    # name -> Character name, vocation or type (such as "Goblin" or "Archer").
    # health -> How much life a character has (integer).
    # attack -> Max damage a character can do (integer).
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    # This function checks if the character is still alive by checking if the health value is not zero.
    def is_alive(self):
        return self.health != 0

    # This function makes one character attack another character.
    def attack_target(self, target):
        # Picks a random damage number between 5 and set max attack.
        damage = random.randint(5, self.attack)
        # Subtract damage from the target's health but don't go below 0.
        target.health = max(target.health - damage, 0)
        print(f"{self.name} hits {target.name} for {damage} ({target.health} HP left)")
        time.sleep(0.5)
# This is a special subclass for heroes, allowing them to do critical attacks.
class Hero(Character):
    def __init__(self, name, health, attack, crit_chance):
        super().__init__(name, health, attack)
        self.crit_chance = crit_chance  # The chance is a float from 0.0 (0%) to 1.0 (100%). Eg.: 0.77 = 77%

    # Hero attack target.
    def attack_target(self, target):
        # If random number drawn is inside the critical percentage, the attack will be critical.
        is_crit = random.random() < self.crit_chance
        base_damage = random.randint(5, self.attack)
        # If attack is critical, damage dealt will be multiplied by 3.
        damage = base_damage * 3 if is_crit else base_damage
        target.health = max(target.health - damage, 0)
        # The text "CRITICAL" is attached to damage display if attack is critical.
        crit_text = " CRITICAL" if is_crit else ""
        print(f"{self.name} hits {target.name} for {damage}{crit_text} ({target.health} HP left)")
        time.sleep(0.5)

# These are vocations of heroes in the game.
# Each vocation has a health, attack and critical value respectively (all are required, even if 0).
HERO_TYPES = {
    "Ranger": (55, 14, 0.20),
    "Mage": (45, 16, 0.25),
    "Warrior": (65, 12, 0.15),
    "Paladin": (70, 12, 0.10),
    "Assassin": (50, 18, 0.35),
    "Cleric": (60, 10, 0.10)
}

# These are types of monsters in the game.
# Each vocation has a health, attack value respectively.
MONSTER_TYPES = {
    "Goblin": (25, 8),
    "Orc": (45, 11),
    "Skeleton": (30, 9),
    "Troll": (55, 13),
    "Dragon": (70, 16)
}

# This function instantiates the teams that will be later assembled.
# types_dict -> Contains information such as "HERO_TYPES" or "MONSTER_TYPES".
# counts_dict -> Tells how many of each character we want.
def create_team(types_dict, counts_dict, is_hero=False):
    # This automatically flags a team as a hero team from the number of attributes.
    is_hero_team = all(len(v) == 3 for v in types_dict.values())
    # Loop through each character vocations or type and how many we want. For each one, creates a "Character" object with its vocation or type (referred internally as name), health, and attack.
    return [
        # Asterisk symbol unpacks the tuple (health, attack).
        (Hero(name, *types_dict[name]) if is_hero_team else Character(name, *types_dict[name]))
        for name, count in counts_dict.items()
        for _ in range(count)  # Repeat for the number of characters we want.
    ]

# This function handles a 1 on 1 battle between two characters.
# "char_one" refers to the hero while "char_two" refers to the monster.
def battle(char_one, char_two):
    clear_screen()
    print(f"Battle: {char_one.name} vs {char_two.name}")
    time.sleep(2)
    clear_screen()

    # Loop until the hero (char_one) or monster dies.
    while char_one.is_alive() and char_two.is_alive():
        char_one.attack_target(char_two)  # Hero attacks first.
        if char_two.is_alive():           # If the monster is still alive, it attacks back.
            char_two.attack_target(char_one)

    # Find winner and display it.
    winner = char_one if char_one.is_alive() else char_two
    time.sleep(1)
    clear_screen()
    print(f"{winner.name} wins the battle!")
    time.sleep(1)
    return winner

# Main autobattler function.
def auto_battler(hero_team, monster_team):
    # Shuffle both team orders.
    random.shuffle(hero_team)
    random.shuffle(monster_team)
    hero_index, monster_index = 0, 0  # Start at the first hero and monster (index 0).

    # While there are characters alive, keep looping.
    # Determines if there are characters still alive.
    while hero_index < len(hero_team) and monster_index < len(monster_team):
        # Determines winner by finding if there are characters still alive in the team.
        winner = battle(hero_team[hero_index], monster_team[monster_index])
        if winner in hero_team: # If hero survives, move to next monster.
            monster_index += 1
        else: # Vice-versa.
            hero_index += 1

    # Check for survivors after the war.
    surviving_heroes = [h for h in hero_team if h.is_alive()]
    surviving_monsters = [m for m in monster_team if m.is_alive()]

    clear_screen()
    # Display winning team and its survivors.
    if surviving_heroes and not surviving_monsters:
        print("Heroes win!", "Survivors:", ", ".join(h.name for h in surviving_heroes))
    elif surviving_monsters and not surviving_heroes:
        print("Monsters win!", "Survivors:", ", ".join(m.name for m in surviving_monsters))

# Assemble hero formation.
HERO_COUNTS = {
    "Ranger": 1,
    "Mage": 1,
    "Warrior": 1,
    "Paladin": 0,
    "Assassin": 0,
    "Cleric": 1
}

# Assemble monster formation.
MONSTER_COUNTS = {
    "Goblin": 3,
    "Skeleton": 2,
    "Orc": 2,
    "Troll": 1,
    "Dragon": 1
}

# Finally instantiate hero and monster teams from the formations assembled.
hero_team = create_team(HERO_TYPES, HERO_COUNTS)
monster_team = create_team(MONSTER_TYPES, MONSTER_COUNTS)

# Start the automated team battle.
auto_battler(hero_team, monster_team)
