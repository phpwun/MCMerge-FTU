import sys
import subprocess
from PIL import Image

def check_and_install_pillow():
    """Ensure Pillow is installed for image manipulation."""
    try:
        __import__('pkg_resources').get_distribution('Pillow')
        print("Pillow is already installed.")
    except ImportError:
        print("Pillow not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("Pillow has been installed.")

def merge_skins(base_image_path, overlay_image_path, mode, parts, hard=False):
    """Merge two skins based on the mode, specific parts, and overlay type.
    
    Args:
        base_image_path (str): Path to the base skin image.
        overlay_image_path (str): Path to the overlay skin image.
        mode (str): 'ALL', 'Simple', or 'Advanced'.
        parts (list): Parts to merge in 'Simple' or 'Advanced' mode.
        hard (bool): If True, replace pixels ignoring transparency.
    """
    check_and_install_pillow()

    # Load the skins
    skin1 = Image.open(base_image_path).convert('RGBA')
    skin2 = Image.open(overlay_image_path).convert('RGBA')

    # Create a new image for the merged skin
    merged_skin = skin1.copy()

    if mode == 'ALL':
        # Overlay skin2 onto skin1 respecting only non-fully transparent pixels
        for x in range(skin2.width):
            for y in range(skin2.height):
                pixel2 = skin2.getpixel((x, y))
                if pixel2[3] > 0 and (hard or pixel2[3] == 255):  # Check transparency and HARD mode condition
                    merged_skin.putpixel((x, y), pixel2)
    else:
        # Apply detailed parts overlay for 'Simple' or 'Advanced' modes
        for part in parts:
            for box in part:
                region2 = skin2.crop(box)
                for x in range(box[0], box[2]):
                    for y in range(box[1], box[3]):
                        pixel2 = region2.getpixel((x - box[0], y - box[1]))
                        if pixel2[3] > 0 and (hard or pixel2[3] == 255):
                            merged_skin.putpixel((x, y), pixel2)

    # Save the merged skin
    merged_skin.save('merged_skin.png')

if __name__ == "__main__":
    # Command line arguments: Base.png Overlay.png 'Advanced' ['Face', 'Front Helmet'] hard=True
    base_image_path = sys.argv[1]
    overlay_image_path = sys.argv[2]
    mode = sys.argv[3]
    parts = eval(sys.argv[4])  # Convert string list input to actual list
    hard = eval(sys.argv[5])  # Convert string boolean input to actual boolean
    merge_skins(base_image_path, overlay_image_path, mode, parts, hard)