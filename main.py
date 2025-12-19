import streamlit as st
import numpy as np
from enum import Enum

# Game state management
class GameScreen(Enum):
    MENU = "menu"
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

def show_menu():
    st.title("Creature Collector")
    st.header("Main Menu")

    col1, col2 = st.columns(2)

    with col1:
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
