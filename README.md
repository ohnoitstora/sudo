# Sudoku

A small, entry-level Sudoku user interface built with Python and Textual.

This project intentionally keeps the game logic minimal:

- hardcoded starting board
- read-only starting numbers
- editable empty cells
- single-digit input only
- no solver
- no win checker
- no puzzle validation

## Requirements

- Python 3.11+
- Textual

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

If you are using the existing virtual environment in this workspace, you can also run:

```bash
.venv/bin/python app.py
```

## Controls

- click any cell to focus it
- use arrow keys to move between cells
- type `1` to `9` in editable cells
- use `Backspace`, `Delete`, or `0` to clear an editable cell

## Notes

The interface focuses on the board layout and direct input handling. It does not try to enforce Sudoku rules beyond locking the original given numbers.