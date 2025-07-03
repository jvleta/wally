#!/bin/zsh

python3 -m venv venv
source venv/bin/activate
echo "Installing required packages..."
pip3 install numpy scipy matplotlib pandas scikit-learn jupyterlab
pip3 install Flask Flask-SQLAlchemy Werkzeug
if [ $? -eq 0 ]; then
    echo "Installation successful!"
else
    echo "Installation failed. Please check the error messages above."
    exit 1
fi