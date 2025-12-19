import streamlit as st
import numpy as np
from creature import get_creature_templates, create_creature, TYPE_FIRE, TYPE_WATER, TYPE_EARTH, TYPE_AIR, TYPE_LIGHTNING, TYPE_SHADOW, TYPE_NATURE, TYPE_ICE, get_type_multiplier
import random

st.set_page_config(
    page_title="Creature Collector",
    page_icon="🐉",
    layout="wide"
)

# Screen constants
SCREEN_MENU = "menu"
SCREEN_WORLD = "world"
SCREEN_BATTLE = "battle"
SCREEN_COLLECTION = "collection"
SCREEN_GACHA = "gacha"
SCREEN_COMBINE = "combine"

# Initialize session state
if 'screen' not in st.session_state:
    st.session_state.screen = SCREEN_MENU
if 'player_creatures' not in st.session_state:
    st.session_state.player_creatures = []  # Will hold player's creature collection
if 'player_items' not in st.session_state:
    st.session_state.player_items = []  # Will hold player's item collection
if 'player_x' not in st.session_state:
    st.session_state.player_x = 5  # Starting X position in world grid
if 'player_y' not in st.session_state:
    st.session_state.player_y = 5  # Starting Y position in world grid
if 'world_grid' not in st.session_state:
    # Initialize a simple 10x10 world grid (0 = grass, 1 = water, 2 = forest)
    st.session_state.world_grid = np.random.choice([0, 1, 2], size=(10, 10), p=[0.5, 0.2, 0.3])

def show_menu():
    st.title("Creature Collector")
    st.header("Main Menu")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Explore World", use_container_width=True):
            st.session_state.screen = SCREEN_WORLD
            st.rerun()

        if st.button("Battle", use_container_width=True):
            st.session_state.screen = SCREEN_BATTLE
            st.rerun()

        if st.button("Collection", use_container_width=True):
            st.session_state.screen = SCREEN_COLLECTION
            st.rerun()

    with col2:
        if st.button("Gacha (Items)", use_container_width=True):
            st.session_state.screen = SCREEN_GACHA
            st.rerun()

        if st.button("Combine Creatures", use_container_width=True):
            st.session_state.screen = SCREEN_COMBINE
            st.rerun()

def show_world():
    st.title("World Exploration")

    # Display current position
    st.write(f"Position: ({st.session_state.player_x}, {st.session_state.player_y})")

    # Render the world grid
    terrain_symbols = {0: "🟩", 1: "🟦", 2: "🌲"}  # grass, water, forest

    grid_display = []
    for y in range(st.session_state.world_grid.shape[0]):
        row = []
        for x in range(st.session_state.world_grid.shape[1]):
            if x == st.session_state.player_x and y == st.session_state.player_y:
                row.append("🧍")  # player character
            else:
                terrain_type = st.session_state.world_grid[y, x]
                row.append(terrain_symbols[terrain_type])
        grid_display.append(" ".join(row))

    # Display grid with monospace font
    grid_text = "\n".join(grid_display)
    st.markdown(f"```\n{grid_text}\n```")

    # Movement controls
    st.write("---")
    st.write("Movement Controls:")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("⬆️ North", use_container_width=True):
            if st.session_state.player_y > 0:
                st.session_state.player_y -= 1
                st.rerun()

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("⬅️ West", use_container_width=True):
            if st.session_state.player_x > 0:
                st.session_state.player_x -= 1
                st.rerun()

    with col2:
        if st.button("⬇️ South", use_container_width=True):
            if st.session_state.player_y < st.session_state.world_grid.shape[0] - 1:
                st.session_state.player_y += 1
                st.rerun()

    with col3:
        if st.button("➡️ East", use_container_width=True):
            if st.session_state.player_x < st.session_state.world_grid.shape[1] - 1:
                st.session_state.player_x += 1
                st.rerun()

    # Display terrain info
    current_terrain = st.session_state.world_grid[st.session_state.player_y, st.session_state.player_x]
    terrain_names = {0: "Grassland", 1: "Water", 2: "Forest"}
    st.write(f"Current terrain: {terrain_names[current_terrain]}")

    st.write("---")
    if st.button("Back to Menu"):
        st.session_state.screen = SCREEN_MENU
        st.rerun()

def init_battle():
    """Initialize a new double battle with random creatures."""
    templates = list(get_creature_templates().keys())

    # Pick 2 random creatures for player and 2 for enemy
    player_picks = random.sample(templates, 2)
    enemy_picks = random.sample(templates, 2)

    st.session_state.battle = {
        "player_team": [create_creature(player_picks[0], 5), create_creature(player_picks[1], 5)],
        "enemy_team": [create_creature(enemy_picks[0], 5), create_creature(enemy_picks[1], 5)],
        "turn": 1,
        "log": ["Battle started!"],
        "phase": "select_action",  # select_action, select_target, enemy_turn, battle_over
        "selected_creature": 0,  # which player creature is acting (0 or 1)
        "selected_ability": None,
        "player_actions": [None, None],  # stores planned actions for both creatures
    }

def render_creature_card(creature, is_enemy=False):
    """Render a creature's status card."""
    element_icons = {
        TYPE_FIRE: "🔥", TYPE_WATER: "💧", TYPE_EARTH: "🌍", TYPE_AIR: "💨",
        TYPE_LIGHTNING: "⚡", TYPE_SHADOW: "🌑", TYPE_NATURE: "🌿", TYPE_ICE: "❄️",
    }
    hp_pct = creature.current_hp / creature.max_hp
    hp_bar_filled = int(hp_pct * 10)
    hp_bar = "█" * hp_bar_filled + "░" * (10 - hp_bar_filled)

    status = "💀" if not creature.is_alive() else ""
    element_icon = element_icons.get(creature.element, "")

    st.markdown(f"### {creature.sprite_path} {creature.name} {status}")
    st.caption(f"{element_icon} {creature.element.capitalize()} | Lv.{creature.level}")
    st.text(f"HP: [{hp_bar}] {creature.current_hp}/{creature.max_hp}")
    st.text(f"ATK: {creature.atk}  DEF: {creature.defense}  SPD: {creature.spd}")

def execute_turn(battle):
    """Execute all queued actions for this turn."""
    # Gather all combatants with their actions
    actions = []

    for i, action in enumerate(battle["player_actions"]):
        if action and battle["player_team"][i].is_alive():
            actions.append({
                "creature": battle["player_team"][i],
                "ability": action["ability"],
                "target": action["target"],
                "is_player": True,
                "index": i,
            })

    # Enemy AI: random ability on random player creature
    for i, enemy in enumerate(battle["enemy_team"]):
        if enemy.is_alive():
            alive_players = [p for p in battle["player_team"] if p.is_alive()]
            if alive_players and enemy.abilities:
                target = random.choice(alive_players)
                ability = random.choice(enemy.abilities)
                actions.append({
                    "creature": enemy,
                    "ability": ability,
                    "target": target,
                    "is_player": False,
                    "index": i,
                })

    # Sort by speed (faster goes first)
    actions.sort(key=lambda x: x["creature"].spd, reverse=True)

    # Execute actions
    for action in actions:
        attacker = action["creature"]
        defender = action["target"]
        ability = action["ability"]

        if not attacker.is_alive():
            continue  # skip if attacker fainted
        if not defender.is_alive():
            # Retarget to another alive enemy
            if action["is_player"]:
                alive_targets = [e for e in battle["enemy_team"] if e.is_alive()]
            else:
                alive_targets = [p for p in battle["player_team"] if p.is_alive()]
            if not alive_targets:
                continue
            defender = random.choice(alive_targets)

        result = attacker.use_ability(ability, defender)

        if result["hit"]:
            effectiveness = ""
            if result["type_effectiveness"] > 1:
                effectiveness = " It's super effective!"
            elif result["type_effectiveness"] < 1:
                effectiveness = " It's not very effective..."

            battle["log"].append(f"{attacker.name} used {ability.name} on {defender.name} for {result['damage']} damage!{effectiveness}")

            if result["defender_fainted"]:
                battle["log"].append(f"{defender.name} fainted!")
        else:
            battle["log"].append(f"{attacker.name}'s {ability.name} missed!")

    # Check win/lose conditions
    player_alive = any(c.is_alive() for c in battle["player_team"])
    enemy_alive = any(c.is_alive() for c in battle["enemy_team"])

    if not enemy_alive:
        battle["log"].append("🎉 Victory! You won the battle!")
        battle["phase"] = "battle_over"
    elif not player_alive:
        battle["log"].append("💀 Defeat... Your team was wiped out.")
        battle["phase"] = "battle_over"
    else:
        battle["turn"] += 1
        battle["player_actions"] = [None, None]
        battle["selected_creature"] = 0
        battle["phase"] = "select_action"

def show_battle():
    st.title("Double Battle")

    # Initialize battle if needed
    if "battle" not in st.session_state or st.session_state.battle is None:
        init_battle()

    battle = st.session_state.battle

    # Display turn counter
    st.subheader(f"Turn {battle['turn']}")

    # Enemy team (top)
    st.markdown("### Enemy Team")
    enemy_cols = st.columns(2)
    for i, enemy in enumerate(battle["enemy_team"]):
        with enemy_cols[i]:
            render_creature_card(enemy, is_enemy=True)

    st.divider()

    # Player team (bottom)
    st.markdown("### Your Team")
    player_cols = st.columns(2)
    for i, player in enumerate(battle["player_team"]):
        with player_cols[i]:
            render_creature_card(player)
            if battle["phase"] == "select_action" and battle["selected_creature"] == i and player.is_alive():
                st.markdown("**⬇️ Select an action:**")

    st.divider()

    # Action selection phase
    if battle["phase"] == "select_action":
        current_idx = battle["selected_creature"]
        current_creature = battle["player_team"][current_idx]

        # Skip fainted creatures
        while not current_creature.is_alive() and current_idx < 2:
            battle["player_actions"][current_idx] = {"ability": None, "target": None, "skip": True}
            current_idx += 1
            if current_idx < 2:
                current_creature = battle["player_team"][current_idx]
                battle["selected_creature"] = current_idx

        if current_idx < 2 and current_creature.is_alive():
            st.markdown(f"**{current_creature.sprite_path} {current_creature.name}'s turn - Choose an ability:**")

            ability_cols = st.columns(len(current_creature.abilities))
            for i, ability in enumerate(current_creature.abilities):
                with ability_cols[i]:
                    if st.button(f"{ability.name}\n(Pow:{ability.power} Acc:{ability.accuracy}%)", key=f"ability_{current_idx}_{i}", use_container_width=True):
                        battle["selected_ability"] = ability
                        battle["phase"] = "select_target"
                        st.rerun()

    # Target selection phase
    elif battle["phase"] == "select_target":
        current_idx = battle["selected_creature"]
        current_creature = battle["player_team"][current_idx]
        ability = battle["selected_ability"]

        st.markdown(f"**{current_creature.name} will use {ability.name} - Select target:**")

        target_cols = st.columns(2)
        for i, enemy in enumerate(battle["enemy_team"]):
            with target_cols[i]:
                if enemy.is_alive():
                    type_mult = get_type_multiplier(ability.element, enemy.element)
                    eff_text = ""
                    if type_mult > 1:
                        eff_text = " (Super effective!)"
                    elif type_mult < 1:
                        eff_text = " (Not very effective)"

                    if st.button(f"Target {enemy.sprite_path} {enemy.name}{eff_text}", key=f"target_{i}", use_container_width=True):
                        battle["player_actions"][current_idx] = {"ability": ability, "target": enemy}

                        # Move to next creature or execute turn
                        next_idx = current_idx + 1
                        while next_idx < 2 and not battle["player_team"][next_idx].is_alive():
                            battle["player_actions"][next_idx] = {"ability": None, "target": None, "skip": True}
                            next_idx += 1

                        if next_idx >= 2:
                            execute_turn(battle)
                        else:
                            battle["selected_creature"] = next_idx
                            battle["phase"] = "select_action"
                        st.rerun()

        if st.button("Cancel"):
            battle["phase"] = "select_action"
            battle["selected_ability"] = None
            st.rerun()

    # Battle over phase
    elif battle["phase"] == "battle_over":
        if st.button("New Battle", use_container_width=True):
            init_battle()
            st.rerun()

    # Battle log
    st.divider()
    st.markdown("### Battle Log")
    for msg in battle["log"][-5:]:  # show last 5 messages
        st.text(msg)

    st.divider()
    if st.button("Flee (Back to Menu)"):
        st.session_state.battle = None
        st.session_state.screen = SCREEN_MENU
        st.rerun()

def show_collection():
    st.title("Creature Collection")

    # Element display info
    element_icons = {
        TYPE_FIRE: "🔥", TYPE_WATER: "💧", TYPE_EARTH: "🌍", TYPE_AIR: "💨",
        TYPE_LIGHTNING: "⚡", TYPE_SHADOW: "🌑", TYPE_NATURE: "🌿", TYPE_ICE: "❄️",
    }
    element_order = [TYPE_FIRE, TYPE_WATER, TYPE_EARTH, TYPE_AIR, TYPE_LIGHTNING, TYPE_SHADOW, TYPE_NATURE, TYPE_ICE]

    templates = get_creature_templates()

    # Group creatures by element
    creatures_by_element = {e: [] for e in element_order}
    for name, creature in templates.items():
        creatures_by_element[creature.element].append(creature)

    # Display creatures by element
    for element in element_order:
        creatures = creatures_by_element[element]
        if not creatures:
            continue

        st.subheader(f"{element_icons[element]} {element.capitalize()}")

        cols = st.columns(3)
        for i, creature in enumerate(creatures):
            with cols[i % 3]:
                st.markdown(f"### {creature.sprite_path} {creature.name}")
                st.caption(creature.description)
                st.text(f"HP: {creature.base_hp}  ATK: {creature.base_atk}")
                st.text(f"DEF: {creature.base_def}  SPD: {creature.base_spd}")
                abilities_str = ", ".join([a.name for a in creature.abilities])
                st.text(f"Moves: {abilities_str}")
                st.divider()

    if st.button("Back to Menu"):
        st.session_state.screen = SCREEN_MENU
        st.rerun()

def show_gacha():
    st.title("Item Gacha")
    st.write("Gacha system for items - coming soon")

    if st.button("Back to Menu"):
        st.session_state.screen = SCREEN_MENU
        st.rerun()

def show_combine():
    st.title("Combine Creatures")
    st.write("Creature combination system - coming soon")

    if st.button("Back to Menu"):
        st.session_state.screen = SCREEN_MENU
        st.rerun()

# Main app routing
def main():
    # Route to appropriate screen
    if st.session_state.screen == SCREEN_MENU:
        show_menu()
    elif st.session_state.screen == SCREEN_WORLD:
        show_world()
    elif st.session_state.screen == SCREEN_BATTLE:
        show_battle()
    elif st.session_state.screen == SCREEN_COLLECTION:
        show_collection()
    elif st.session_state.screen == SCREEN_GACHA:
        show_gacha()
    elif st.session_state.screen == SCREEN_COMBINE:
        show_combine()
    else:
        show_menu()  # Fallback to menu

if __name__ == "__main__":
    main()
