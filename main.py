import streamlit as st
import numpy as np
from creature import get_creature_templates, TYPE_FIRE, TYPE_WATER, TYPE_EARTH, TYPE_AIR, TYPE_LIGHTNING, TYPE_SHADOW, TYPE_NATURE, TYPE_ICE

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

def show_battle():
    st.title("Battle")
    st.write("Battle system - coming soon")

    if st.button("Back to Menu"):
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
