# Silent Hill: Townfall collectible checker

A small script that reads your Silent Hill: Townfall save files and tells you which collectibles you're still missing for the related achievements. It's handy when you're one document or one radio signal short and have no idea which one.

It covers:

- Documents (Observation 50% / Thorough Inspection)
- CRTV signals (Sweeping Signals)
- VHF transmissions
- Phone numbers (Cold Calling)
- Resource containers (Resourceful)
- Strange postcards (Blur Your Eyes)

The script only reads your saves. It never writes to them, so it can't break anything.

## Requirements

- Windows
- Python 3.8 or newer, unless you use the .exe (see below)

The script only uses the Python standard library.

## Usage

Open a terminal in the folder containing the script and run:

```
python check_collectibles.py
```

By default, it looks for your saves in:

```
%LOCALAPPDATA%\Townfall\Saved\SaveGames
```

That's where the game keeps them on a standard install, so most people won't need to change anything.

### Options

If your saves are somewhere else, pass the folder as an argument:

```
python check_collectibles.py "D:\Some\Other\Folder"
```

By default, only the missing items are listed. Add `--all` to see everything, found or not:

```
python check_collectibles.py --all
```

## Using the .exe instead

If you don't have Python installed, you can use `TownfallChecker.exe` instead. Double-click it and the report shows up in a console window. The window stays open until you press Enter.

The same options work if you run it from a terminal:

```
TownfallChecker.exe --all
```

Windows SmartScreen or your antivirus may complain the first time you run it. That's common with small unsigned programs built with PyInstaller. If you'd rather not deal with that, run the Python script directly.

To build the .exe yourself:

```
pip install pyinstaller
python -m PyInstaller --onefile --name TownfallChecker check_collectibles.py
```

The result ends up in the `dist` folder.

## Reading the output

Each section shows how many items you've found, the total, and the achievement it counts toward. For example:

```
== CRTV signals: 8/10   [Sweeping Signals]
   [ ] Hotel Room 2
   [ ] Missing Parts: Where
```

## How it works

The game keeps two kinds of save data:

- `ProfileData.sav` tracks your progress across all playthroughs. Documents, signals, phone numbers and containers are read from this file, so anything you've found in any run counts.
- `SaveGame*.sav` are your individual playthroughs. Strange postcards don't seem to carry over between runs, so they're checked per save. The script uses the save with the most postcards, and when two saves are tied, it picks the most recent one.

## Notes and limitations

- The game doesn't give resource containers proper names, so they're listed as Lock box A to G. They should match the order you come across them.
- If a save file can't be read (corrupted, or from a different game version), the script says so and moves on to the others.
