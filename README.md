# Code Assistant

[![Python Version](https://img.shields.io/badge/python-3.7+-brightgreen.svg?style=flat)]()
[![Release](https://img.shields.io/badge/release-v1.5.0-brightgreen.svg?style=flat)]()
[![License](https://img.shields.io/badge/license-MulanPSL2.0-brightgreen.svg?style=flat)]()
[![OS](https://img.shields.io/badge/os-win-brightgreen.svg?style=flat)]()
[![Author](https://img.shields.io/badge/Author-陌北v1-orange.svg?style=flat)]()

[中文版](README_zh.md)

A PyQt5-based Windows code snippet quick-input tool. Use the global hotkey `Ctrl+Alt+K` to bring up a search window, type a keyword to instantly match saved commands or code snippets, and copy them to the clipboard with optional auto-paste at the cursor position — greatly boosting development efficiency.

Developed with Python 3.8.

#### Run:
```bash
pip install -r requirements.txt
pythonw kk.py            # Run
pythonw kk.py && exit    # Run and close terminal
```
The program runs in the **background** after launch and can be summoned anytime via the global hotkey.

![image-20230113094605172](image-20230113094605172.png)

#### Usage:

Press **`Ctrl+Alt+K`** to bring up the quick-input window. Type your shortcut phrase to search and match in real time.

| Shortcut | Action |
|---|---|
| `Ctrl+Alt+K` | Global hotkey — show/activate the window from anywhere |
| `Ctrl+K` | Focus the search bar and select all text |
| `↓` | Move focus from search bar to result list |
| `↑` | Return to search bar when at the first list item |
| `Enter` | Copy selected item to clipboard and hide window |
| `Ctrl+Enter` | Copy to clipboard **and auto-paste** at current cursor position |
| `ESC` | Close / hide the window |

Matching keywords are **highlighted** in the result list. Input has a 150ms debounce to avoid excessive queries.

> **Don't forget to add commands before use.**

![image-20230113100333302](image-20230113100333302.png)

#### Data Fields:

Each record contains the following fields:

| Field | Description |
|---|---|
| Keyword | Search phrase for matching |
| Title | Displayed on the first line of the list item |
| Code/Example | Displayed on the second line of the list item |
| Content (note) | Actual text copied to the clipboard |
| Secret (is_secret) | When checked, content is displayed as `******` |

Hover over a list item to see the full note content via tooltip.

#### Adding:
Type `:add` to open the add window:

![add](add.png)

Add window:

![image-20230113095806716](image-20230113095806716.png)

#### Editing:

Right-click on a list item to open a context menu for editing and deleting.

![edit](edit.png)

#### Advanced Features:

- **Single instance**: Launching the program again activates the existing instance instead of opening a new window.
- **Dark theme**: Dark gray color scheme (#3c3c3c), easy on the eyes.
