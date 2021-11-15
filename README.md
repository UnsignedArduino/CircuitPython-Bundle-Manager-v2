[comment]: <> (This README is based off the template found here: )
[comment]: <> (https://github.com/dbader/readme-template)

# CircuitPython-Bundle-Manager-v2
> A Python program that makes it easy to manage modules on a CircuitPython 
> device!

The CircuitPython Bundle Manager v2 is a program that allows you to easily 
download bundles and use them to install modules on CircuitPython devices!

As the name implies, it's version 2 of the original 
[CircuitPython-Bundle-Manager](https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager)
with many more fixes and features!

![A picture of the CircuitPython Bundle Manager's Modules tab open](assets/images/1.png)

## Installation

Here are some quick instructions, for more detailed and through instructions 
go to the 
[wiki](https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/wiki/Installation).

### Install from ZIP

There will be ZIP files that you can just pass into the Python interpreter 
eventually! (once I get a release in)

### Install from source

#### Windows

1. `cd` to somewhere convenient. (Like a drive where all your projects go`)
2. Download the repo
   (`git clone https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2`)
3. `cd` into the downloaded repo. 
4. Create a virtual environment. (`python -m venv .venv`)
5. Activate the virtual environment. (`".venv/Scripts/activate.bat"`)
6. Install the requirements. (`pip install -r requirements.txt`)
7. Run! (`python main.py`)

#### Linux / macOS

1. `cd` to somewhere convenient. (Like your home directory)
2. Download the repo
   (`git clone https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2`)
3. `cd` into the downloaded repo. 
4. Create a virtual environment. (`python3 -m venv .venv`)
5. Activate the virtual environment. (`source .venv/bin/activate`)
6. Install the requirements. (`pip3 install -r requirements.txt`)
7. If the installation fails, then follow the instructions to 
   [install `cryptography`](https://cryptography.io/en/latest/installation/#building-cryptography-on-linux)
   on your machine. Then try step 6 again. 
8. Run! (`python3 main.py`)

## Usage

> Please note that the wiki is still a work in progress! Contributions are 
> welcomed!

All the documentation is available online on this repo's 
[wiki](https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/wiki)!

## Contributing

No different from any other project on GitHub - fork, clone, commit, 
push, and pull request! 

## License

This project is distributed under the `GNU General Public License v3.0`. See 
the [`LICENSE`](LICENSE) file for the full license. 
