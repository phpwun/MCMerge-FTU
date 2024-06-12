import subprocess
import sys
from PIL import Image
import argparse
import ast

def check_and_install_pillow():
    try:
        __import__('pkg_resources').get_distribution('Pillow')
        print("Pillow is already installed.")
    except ImportError:
        print("Pillow not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("Pillow has been installed.")

def merge_skins(skin1_path, skin2_path, mode, parts=None, hard=False):
    check_and_install_pillow()

    # Load the skins
    skin1 = Image.open(skin1_path).convert('RGBA')
    skin2 = Image.open(skin2_path).convert('RGBA')

    # Create a new image for the merged skin
    merged_skin = skin1.copy()

    if mode == 'ALL':
        # Overlay skin2 onto skin1 respecting transparency
        for x in range(skin2.width):
            for y in range(skin2.height):
                pixel2 = skin2.getpixel((x, y))
                if pixel2[3] > 0:  # Only consider pixels that are not fully transparent
                    merged_skin.putpixel((x, y), pixel2)
    else:
        # Convert parts string to list of parts
        if parts:
            parts = ast.literal_eval(parts)

        # Definitions for skin parts
        parts_definitions = {
            'Head': [(0, 0, 32, 16), (32, 0, 64, 16)],
            'Torso': [(16, 16, 40, 32), (16, 32, 40, 48)],
            'Right Arm': [(40, 16, 56, 32), (40, 32, 56, 48)],
            'Left Arm': [(32, 48, 48, 64), (48, 48, 64, 64)],
            'Right Leg': [(0, 16, 16, 32), (0, 32, 16, 48)],
            'Left Leg': [(16, 48, 32, 64), (0, 48, 16, 64)],
            'Face': [(8, 8, 16, 16)],
            'Front Helmet': [(40, 8, 48, 16)],
            'Front Torso': [(20, 20, 28, 32)],
            'Front Jacket': [(20, 36, 28, 48)],
            'Right Arm': [(44, 20, 48, 32), (44, 36, 48, 48)],
            'Left Arm': [(36, 52, 40, 64), (52, 52, 56, 64)],
            'Right Leg': [(4, 20, 8, 32), (4, 36, 8, 48)],
            'Left Leg': [(20, 52, 24, 64), (20, 68, 24, 80)]
        }

        if mode == 'Simple':
            target_parts = {'Top': ['Head', 'Front Helmet', 'Face'], 'Middle': ['Torso', 'Right Arm', 'Left Arm'], 'Bottom': ['Right Leg', 'Left Leg']}
            selected_parts = [part for section in parts for part in target_parts[section]]
        elif mode == 'Advanced':
            selected_parts = [key for key in parts if key in parts_definitions]

        # Merge specified parts
        for part in selected_parts:
            for box in parts_definitions[part]:
                region2 = skin2.crop(box)
                region1 = merged_skin.crop(box)

                for x in range(box[0], box[2]):
                    for y in range(box[1], box[3]):
                        pixel2 = region2.getpixel((x - box[0], y - box[1]))
                        if pixel2[3] > 0:
                            if hard:
                                region1.putpixel((x - box[0], y - box[1]), pixel2)
                            else:
                                pixel1 = region1.getpixel((x - box[0], y - box[1]))
                                alpha = pixel2[3] / 255
                                blended_pixel = tuple(int(alpha * p2 + (1 - alpha) * p1) for p1, p2 in zip(pixel1, pixel2))
                                region1.putpixel((x - box[0], y - box[1]), blended_pixel)

                merged_skin.paste(region1, box)

    # Save the merged skin
    merged_skin.save('merged_skin.png')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two Minecraft skins based on specified modes and areas.")
    parser.add_argument('skin1_path', type=str, help='Path to the first skin image file')
    parser.add_argument('skin2_path', type=str, help='Path to the second skin image file')
    parser.add_argument('mode', type=str, choices=['ALL', 'Simple', 'Advanced'], help='Mode of merging')
    parser.add_argument('parts', type=str, nargs='?', help='Parts to merge, required if mode is Simple or Advanced')
    parser.add_argument('--hard', action='store_true', help='Use hard merging (overwrite pixels)')

    args = parser.parse_args()
    merge_skins(args.skin1_path, args.skin2_path, args.mode, args.parts, args.hard)
