REM This script uses PyInstaller to package the CircuitPython Bundle Manager v2
REM Make sure to install everything needed to build in build-requirements.txt

REM Build

pyinstaller main.py --name "CircuitPython_Bundle_Manager_v2" ^
                    --icon="icon.ico" --noconfirm --clean

REM Copy the neccessary files

COPY "LICENSE" "dist/CircuitPython_Bundle_Manager_v2" /Y
COPY "icon.png" "dist/CircuitPython_Bundle_Manager_v2" /Y

REM Go there

CD dist/CircuitPython_Bundle_Manager_v2

REM Make the certificates directory

MKDIR certifi

REM Set certifi_loc to the location of the certificates

FOR /F "tokens=* USEBACKQ" %%F IN (`python -c "import certifi; print(certifi.where())"`) DO (
    SET certifi_loc=%%F
)

REM Copy the certificate file

COPY "%certifi_loc%" "certifi"
