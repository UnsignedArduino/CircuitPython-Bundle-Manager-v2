# This script uses PyInstaller to package the CircuitPython Bundle Manager v2
# Make sure to install everything you need in build-requirements.txt

# Build

# Hidden imports are from https://stackoverflow.com/a/53848300/10291933

pyinstaller main.py --name "CircuitPython_Bundle_Manager_v2" \
                    --icon="icon.ico" \
                    --noconfirm --clean \
                    --hidden-import="PIL" \
                    --hidden-import="PIL._imagingtk" \
                    --hidden-import="PIL._tkinter_finder" \

# Copy the necessary files

cp "LICENSE" "dist/CircuitPython_Bundle_Manager_v2"
cp "icon.png" "dist/CircuitPython_Bundle_Manager_v2"

# Set the binary as executable

cd dist/CircuitPython_Bundle_Manager_v2
chmod +x CircuitPython_Bundle_Manager_v2
