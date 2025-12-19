#!/bin/bash

# Setup script for Creature Collector game

echo "Setting up Creature Collector virtual environment..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Setup complete!"
echo "To activate the virtual environment in the future, run: source venv/bin/activate"
echo "To run the game, use: streamlit run main.py"
