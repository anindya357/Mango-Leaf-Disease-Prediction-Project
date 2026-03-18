#!/bin/bash

# Mango Leaf Disease Prediction - Quick Start Script (Linux/macOS)
# This script sets up and runs the backend

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║    🥭 Mango Leaf Disease Prediction System 🥭             ║"
echo "║           Quick Start - Linux/macOS                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[✗] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[✓] Python found: $(python3 --version)"
echo ""

# Navigate to backend directory
cd backend || { echo "[✗] backend directory not found"; exit 1; }

echo "═══════════════════════════════════════════════════════════"
echo "STEP 1: Setting up Backend"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[✗] Failed to create virtual environment"
        exit 1
    fi
    echo "[✓] Virtual environment created"
else
    echo "[✓] Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "[✓] Virtual environment activated"

echo ""
echo "Installing backend dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[✗] Failed to install dependencies"
    exit 1
fi
echo "[✓] Dependencies installed"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 2: Verifying Model File"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [ ! -f "models/mango_leaf_disease_MobileNetV2_model.h5" ]; then
    echo ""
    echo "[!] Model file not found at: models/mango_leaf_disease_MobileNetV2_model.h5"
    echo ""
    echo "You need to train the model first:"
    echo "1. Open notebooks/train_model.ipynb in Jupyter"
    echo "2. Run all cells in the notebook"
    echo "3. The model will be saved to backend/models/"
    echo ""
    echo "For now, we'll start the backend anyway."
    echo "The API will fail on predictions until the model exists."
else
    echo "[✓] Model file found: models/mango_leaf_disease_MobileNetV2_model.h5"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 3: Starting Backend Server"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Backend will start at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

sleep 2

python main.py
