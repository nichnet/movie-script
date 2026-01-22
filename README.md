# Inkwell

Inkwell is an open-source screenplay authoring software that simplifies the process of writing screenplays. The software is written in Python and utilizes the PyQt library.

One of the unique features of Inkwell is its ability to format screenplays written in a simple markdown style automatically, saving users time and effort that would otherwise be spent on manual formatting. Additionally, Inkwell includes a range of editing tools to help users make quick and precise changes to their scripts.

The software is constantly being updated with new features and improvements to enhance its user-friendliness and functionality.

![Example](https://github.com/nichnet/movie-script/blob/master/example/example_1.png)


## Usage
```python
python main.py
python main.py --debug
```


## Features
- Simple markdown style editor with live page preview
- Title page support
- Supports inline HTML tags: `<b>`, `<i>`, `<u>`, `<br>`
- Save/Load `.ink` files
- Export to PDF
- Dark mode
- Word, scene, and page count


## Formatting

### Title Page
| Type | Prefix | Example |
| --- | :---: | :--- |
| Title | `**T` | `**T My Movie Title` |
| Author | `**A` | `**A Written by John Smith` |
| Comment | `**C` | `**C Based on a true story` |
| Date/Draft | `**D` | `**D Draft 1 - January 2024` |

### Scene Headings
| Location | Prefix | Result |
| --- | :---: | :--- |
| Interior | `#I` | INT. |
| Exterior | `#E` | EXT. |
| Int/Ext | `#IE` | INT./EXT. |
| Ext/Int | `#EI` | EXT./INT. |

**Time of Day** - Add `/` followed by time:
| Time | Suffix | Result |
| --- | :---: | :--- |
| Day | `/D` | - DAY |
| Night | `/N` | - NIGHT |
| Day/Night | `/DN` | - DAY/NIGHT |
| Night/Day | `/ND` | - NIGHT/DAY |
| Custom | `/DAWN` | - DAWN |
| Multi-word | `/"text"` | - TEXT (uppercase) |

**Examples:**
```
#I/D Coffee Shop           →  INT. COFFEE SHOP - DAY
#E/N Street                →  EXT. STREET - NIGHT
#IE/D Car                  →  INT./EXT. CAR - DAY
#I/DAWN Bedroom            →  INT. BEDROOM - DAWN
#I/CONTINUOUS Hall         →  INT. HALL - CONTINUOUS
#E/"Soon after" Park       →  EXT. PARK - SOON AFTER
#I/"The next day" Kitchen  →  INT. KITCHEN - THE NEXT DAY
```

### Other Elements
| Type | Prefix | Example |
| --- | :---: | :--- |
| In-script Title | `*` | `*ACT ONE` |
| Transition | `##` | `##FADE IN` |
| Dialogue | `@` | `@JOHN "Hello there."` |
| Action | _(none)_ | `John walks into the room.` |

### Inline Formatting
| Tag | Result |
| --- | :--- |
| `<b>text</b>` | **Bold** |
| `<i>text</i>` | *Italic* |
| `<u>text</u>` | Underline |
| `<br>` | Line break |


## Full Example
```
**T STAR TREK: THE NEXT GENERATION
**A Written by
**A Gene Roddenberry
**C Based on Star Trek created by Gene Roddenberry
**D First Draft

#I/D ENTERPRISE BRIDGE
The crew is at their stations. PICARD sits in the captain's chair.

@PICARD "Report, Number One."

@RIKER "All systems operational, Captain."

##CUT TO

#E/N SPACE
The Enterprise glides through the <b>stars</b>.
```


## Keyboard Shortcuts
| Shortcut | Action |
| --- | :--- |
| `Ctrl+N` | New document |
| `Ctrl+O` | Open document |
| `Ctrl+S` | Save document |
| `Ctrl+E` | Export to PDF |


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
