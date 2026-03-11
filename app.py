from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Static

STARTING_BOARD = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


class SudokuCell(Static):
    can_focus = True

    def __init__(self, row: int, col: int, value: int) -> None:
        self.row = row
        self.col = col
        self.given = value != 0
        self.value = value if value != 0 else None

        classes = ["cell", "given" if self.given else "editable"]

        if (row // 3 + col // 3) % 2 == 0:
            classes.append("tone-sun")
        else:
            classes.append("tone-sea")

        if row in {0, 3, 6}:
            classes.append("block-top")
        if col in {0, 3, 6}:
            classes.append("block-left")
        if row in {2, 5, 8}:
            classes.append("block-bottom")
        if col in {2, 5, 8}:
            classes.append("block-right")

        super().__init__(self.display_value, id=f"cell-{row}-{col}", classes=" ".join(classes))

    @property
    def display_value(self) -> str:
        return str(self.value) if self.value is not None else ""

    def set_value(self, value: int) -> None:
        if self.given:
            return
        self.value = value
        self.update(self.display_value)

    def clear_value(self) -> None:
        if self.given:
            return
        self.value = None
        self.update("")

    def on_click(self, event: events.Click) -> None:
        self.focus()
        event.stop()


class SudokuApp(App):
    CSS_PATH = "sudoku.tcss"
    TITLE = "Sudoku Prototype"

    BINDINGS = [
        ("up", "move_up", "Up"),
        ("down", "move_down", "Down"),
        ("left", "move_left", "Left"),
        ("right", "move_right", "Right"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.cells = [
            [SudokuCell(row, col, value) for col, value in enumerate(values)]
            for row, values in enumerate(STARTING_BOARD)
        ]

    def compose(self) -> ComposeResult:
        with Container(id="game"):
            yield Static("Sudoku", id="title")
            yield Static("Barebones Textual prototype", id="subtitle")
            with Horizontal(id="topbar"):
                yield Static(
                    "Click a cell or use arrow keys, then type 1-9. Starting numbers are locked.",
                    id="instructions",
                )
                yield Static("Selected: --", id="status")
            with Container(id="board"):
                for row in self.cells:
                    for cell in row:
                        yield cell
            with Horizontal(id="legend"):
                yield Static("Locked", classes="legend-chip legend-given")
                yield Static("Editable", classes="legend-chip legend-editable")
                yield Static("Backspace/Delete clears", classes="legend-note")

    def on_mount(self) -> None:
        self._focus_first_editable_cell()
        self._update_status()

    def action_move_up(self) -> None:
        self._move_focus(-1, 0)

    def action_move_down(self) -> None:
        self._move_focus(1, 0)

    def action_move_left(self) -> None:
        self._move_focus(0, -1)

    def action_move_right(self) -> None:
        self._move_focus(0, 1)

    def on_key(self, event: events.Key) -> None:
        focused = self.focused
        if not isinstance(focused, SudokuCell):
            return

        if focused.given:
            return

        if event.key in "123456789":
            focused.set_value(int(event.key))
            self._update_status()
            event.stop()
        elif event.key in {"backspace", "delete", "0"}:
            focused.clear_value()
            self._update_status()
            event.stop()

    def on_focus(self, event: events.Focus) -> None:
        if isinstance(event.widget, SudokuCell):
            self._update_status(event.widget)

    def _focus_first_editable_cell(self) -> None:
        for row in self.cells:
            for cell in row:
                if not cell.given:
                    cell.focus()
                    return

    def _move_focus(self, row_delta: int, col_delta: int) -> None:
        focused = self.focused
        if not isinstance(focused, SudokuCell):
            self._focus_first_editable_cell()
            return

        new_row = min(8, max(0, focused.row + row_delta))
        new_col = min(8, max(0, focused.col + col_delta))
        self.cells[new_row][new_col].focus()

    def _update_status(self, cell: SudokuCell | None = None) -> None:
        active_cell = cell if cell is not None else self.focused
        status = self.query_one("#status", Static)

        if not isinstance(active_cell, SudokuCell):
            status.update("Selected: --")
            return

        cell_label = f"R{active_cell.row + 1} C{active_cell.col + 1}"
        if active_cell.given:
            status.update(f"Selected: {cell_label}  Locked")
            return

        value = str(active_cell.value) if active_cell.value is not None else "empty"
        status.update(f"Selected: {cell_label}  Value: {value}")


if __name__ == "__main__":
    SudokuApp().run()