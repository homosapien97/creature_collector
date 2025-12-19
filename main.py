import streamlit as st
import numpy as np
from enum import Enum

# Game state management
class GameScreen(Enum):
    MENU = "menu"
    WORLD = "world"
    BATTLE = "battle"
    COLLECTION = "collection"
    GACHA = "gacha"
    COMBINE = "combine"

# Initialize session state
if 'screen' not in st.session_state:
    st.session_state.screen = GameScreen.MENU
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
            st.session_state.screen = GameScreen.WORLD
            st.rerun()

        if st.button("Battle", use_container_width=True):
            st.session_state.screen = GameScreen.BATTLE
            st.rerun()

        if st.button("Collection", use_container_width=True):
            st.session_state.screen = GameScreen.COLLECTION
            st.rerun()

    with col2:
        if st.button("Gacha (Items)", use_container_width=True):
            st.session_state.screen = GameScreen.GACHA
            st.rerun()

        if st.button("Combine Creatures", use_container_width=True):
            st.session_state.screen = GameScreen.COMBINE
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

    st.text("\n".join(grid_display))

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
        st.session_state.screen = GameScreen.MENU
        st.rerun()

def show_battle():
    st.title("Battle")
    st.write("Battle system - coming soon")

    if st.button("Back to Menu"):
        st.session_state.screen = GameScreen.MENU
        st.rerun()

def show_collection():
    st.title("Creature Collection")

    if len(st.session_state.player_creatures) == 0:
        st.write("No creatures yet!")
    else:
        for creature in st.session_state.player_creatures:
            st.write(f"- {creature}")

    if st.button("Back to Menu"):
        st.session_state.screen = GameScreen.MENU
        st.rerun()

def show_gacha():
    st.title("Item Gacha")
    st.write("Gacha system for items - coming soon")

    if st.button("Back to Menu"):
        st.session_state.screen = GameScreen.MENU
        st.rerun()

def show_combine():
    st.title("Combine Creatures")
    st.write("Creature combination system - coming soon")

    if st.button("Back to Menu"):
        st.session_state.screen = GameScreen.MENU
        st.rerun()

# Main app routing
def main():
    st.set_page_config(
        page_title="Creature Collector",
        page_icon="🐉",
        layout="wide"
    )

    # Route to appropriate screen
    if st.session_state.screen == GameScreen.MENU:
        show_menu()
    elif st.session_state.screen == GameScreen.WORLD:
        show_world()
    elif st.session_state.screen == GameScreen.BATTLE:
        show_battle()
    elif st.session_state.screen == GameScreen.COLLECTION:
        show_collection()
    elif st.session_state.screen == GameScreen.GACHA:
        show_gacha()
    elif st.session_state.screen == GameScreen.COMBINE:
        show_combine()

if __name__ == "__main__":
    main()
