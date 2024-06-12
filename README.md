
# MC Skin Merger

## Description
This Python script merges two Minecraft skin images. It supports different merging modes and the ability to selectively merge parts of the skin, with an option to handle pixel transparency.

## Requirements
- Python 3.x
- Pillow library

## Installation
Run the following command to ensure Pillow is installed:
```bash
python -m pip install Pillow
```

## Usage
To use the script, provide the paths to the base and overlay skin images, the merge mode, the parts to merge (if applicable), and whether to use hard mode (ignores transparency).

### Command Line Arguments
- `base_image_path`: Path to the base skin image.
- `overlay_image_path`: Path to the overlay skin image.
- `mode`: Merge mode ('ALL', 'Simple', or 'Advanced').
- `parts`: List of parts to merge (applicable in 'Simple' or 'Advanced' mode).
- `hard`: Boolean value (`True` or `False`). If `True`, replaces pixels ignoring transparency.

### Example Command
```bash
python skin_merger.py Base.png Overlay.png 'Advanced' "['Face', 'Front Helmet']" True
```

## Function Descriptions
### `check_and_install_pillow()`
Checks if the Pillow library is installed and installs it if not present.

### `merge_skins(base_image_path, overlay_image_path, mode, parts, hard)`
Merges two skins based on provided parameters. Handles different modes and transparency based on the `hard` parameter.

## Output
The script saves the merged skin image as `merged_skin.png` in the current directory.

## Notes
Ensure that the input images are in PNG format and that they conform to the standard Minecraft skin dimensions.
