#!/bin/bash
# setup.sh

# This script sets up the environment for the TSRS Moulsari AI Disaster Preparedness Evaluator.
# It creates a virtual environment, installs dependencies, and provides instructions for API key setup.

echo "===================================================="
echo "Setting up TSRS Moulsari AI Disaster Preparedness Evaluator"
echo "===================================================="

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3.8 or higher."
    exit
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Please check your Python installation."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "----------------------------------------------------"
        echo "ERROR: Failed to install all dependencies."
        echo "Please check the following:"
        echo "1. You have a stable internet connection."
        echo "2. 'requirements.txt' is not corrupted."
        echo "3. Some packages might have system-level dependencies (e.g., build-essentials, portaudio)."
        echo "   - On Debian/Ubuntu: sudo apt-get install build-essential portaudio19-dev"
        echo "   - On MacOS: brew install portaudio"
        echo "   - For pytesseract: Install Google's Tesseract-OCR: https://github.com/tesseract-ocr/tesseract"
        echo "After resolving, you can try running 'pip install -r requirements.txt' again manually."
        echo "----------------------------------------------------"
        exit 1
    fi
else
    echo "WARNING: requirements.txt not found. Skipping dependency installation."
fi

echo "===================================================="
echo "Environment Setup Complete!"
echo "===================================================="
echo ""
echo "------------------- NEXT STEPS -------------------"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Set up your API keys:"
echo "   - Create a file named '.env' in the root directory."
echo "   - Follow the instructions in 'API_SETUP_GUIDE.md' to get your keys."
echo "   - Add them to the '.env' file."
echo ""
echo "3. Add school-specific documents:"
echo "   - Follow the guide in 'DATA_SETUP_GUIDE.md' to add your school's emergency protocols to the '/data' directory."
echo ""
echo "4. Run the RAG ingestion pipeline:"
echo "   python -m rag.ingest"
echo ""
echo "5. Start the Streamlit application:"
echo "   streamlit run app.py"
echo "----------------------------------------------------"

