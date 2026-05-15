# TASU 06 G CODE

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Copyright (C) 2026 Hamid Khatri

This project is licensed under the GNU General Public License v3. See LICENSE for details.

TASU 06 G CODE is a simple Inkscape extension for generating punch-style G-code from selected objects in an SVG drawing.

It is designed for workflows where each selected object represents one punch point. The extension reads the center point of every selected object, then creates a `.gcode` file with machine movement[...] 

Currently tested and working on **Inkscape 1.4.2**.

## What It Does

- Generates G-code from selected objects in Inkscape.
- Uses the center of each selected object's bounding box as the punch position.
- Outputs coordinates in millimeters using `G21`.
- Uses absolute positioning with `G90`.
- Moves to each punch point with `G0`.
- Turns the punch/tool on and off using configurable commands.
- Adds a configurable punch delay/dwell time.
- Supports a selectable starting position:
  - Left Bottom
  - Left Top
- Includes optional zig-zag movement optimization to reduce unnecessary travel.
- Writes the final G-code to a user-selected folder and filename.

## Generated G-code Pattern

For each punch point, the extension creates output similar to this:

```gcode
G0 X10.000 Y20.000
M8
G4 P0.5
M9
```

Default commands:

- Punch ON: `M8`
- Punch OFF: `M9`
- Punch delay: `0.5`

These values can be changed from the extension dialog inside Inkscape.

## Installation

1. Download or clone this repository.
2. Copy these two files:
   - `tasu06.inx`
   - `tasu06.py`
3. Paste them into your Inkscape user extensions folder.

On Windows, the folder is usually:

```text
C:\Users\YOUR_USER_NAME\AppData\Roaming\inkscape\extensions
```

For this development setup, the extension is installed at:

```text
C:\Users\AcerLaptop\AppData\Roaming\inkscape\extensions
```

4. Restart Inkscape.
5. Open Inkscape and go to:

```text
Extensions > TASU 06 G CODE
```

## How To Use

1. Open or create your SVG file in Inkscape.
2. Select the objects that should become punch points.
3. Run `Extensions > TASU 06 G CODE`.
4. Choose the output folder and file name.
5. Set the punch ON command, punch OFF command, and punch delay if needed.
6. Choose the G-code start position.
7. Enable `Optimize Zig Zag Movement` if you want the generated punch order optimized.
8. Click Apply.

The extension will generate a `.gcode` file at the selected output location.

## Options

### Output Folder

The folder where the generated G-code file will be saved.

### File Name

The name of the generated G-code file, for example:

```text
output.gcode
```

### Punch ON Command

The command used to turn the punch/tool on.

Default:

```gcode
M8
```

### Punch OFF Command

The command used to turn the punch/tool off.

Default:

```gcode
M9
```

### Punch Delay

The dwell time after turning the punch/tool on.

Default:

```gcode
G4 P0.5
```

### G-code Start Position

Controls the first move before punching starts.

Available options:

- `Left Bottom`
- `Left Top`

### Optimize Zig Zag Movement

When enabled, the extension sorts punch points in a zig-zag pattern to reduce travel movement.

It also avoids unnecessary repeated axis movement in optimized mode. For example, if only `X` changes between two points, the generated move can omit the unchanged `Y` value.

## Notes

- Select objects before running the extension.
- Each selected object becomes one punch point.
- The punch point is calculated from the center of the object's bounding box.
- The generated file ends with `M2`.
- This extension is currently confirmed working on Inkscape 1.4.2.
