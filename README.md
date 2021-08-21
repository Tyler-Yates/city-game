# city-game

City building game built using PyGame.

## Setup

### Python

You need Python 3.9 or greater in order to run this program.
You can download and install Python from here: https://www.python.org/downloads/

### Virtual Environment

You will need to create a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
to develop or run this application:
```bash
virtualenv --python=python3 venv
source venv/bin/activate
```

Next, install the requirements:
```bash
pip install -Ur requirements.txt
```

## Running

Before running the application, ensure you have sourced the virtual environment created above.

From the root of the repo, run the following command to start the game:
```bash
python3 -m mygame
```

## Development

### Tests and Code Style

This repo uses `tox` to run unit tests and perform code style cleanup and static analysis checks.

`tox` is not included in the requirements file so install it into the venv:
```bash
pip install tox
```

Then, simply run `tox`.

### Module Hierarchy

To avoid cyclical imports, there is a hierarchy of modules.
Modules should only import from modules lower than them on
this list.

```
controllers
frameprocessors
state
interfaces
util
constants
```

Thus, the `constants` module should not import any other modules.

## Game State

Game state is handled by a central state class called `GameState`.
This class is passed into the `Scene` objects which can reference and modify the game state as needed.
