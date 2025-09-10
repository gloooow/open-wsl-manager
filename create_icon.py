#!/usr/bin/env python3
"""
Icon Creation Helper for WSL Manager

This script helps create a simple icon file for the WSL Manager application.
It creates a basic icon using Python's built-in libraries.
"""

import os
from pathlib import Path

def create_simple_icon():
    """Create a simple icon file using PIL if available, or provide instructions."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Check if user has provided an icon image
        icon_sources = ['icon.png', 'icon.jpg', 'icon.jpeg', 'penguin.png', 'penguin.jpg']
        source_image = None
        
        for source in icon_sources:
            if Path(source).exists():
                source_image = source
                break
        
        if source_image:
            # Use the provided image
            print(f"Found image: {source_image}")
            img = Image.open(source_image)
            
            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize to 256x256
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
            
        else:
            # Create a simple WSL-themed icon
            size = 256
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw a simple WSL-themed icon
            # Background circle
            margin = 20
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill=(0, 120, 215, 255), outline=(0, 80, 180, 255), width=4)
            
            # Draw "WSL" text
            try:
                # Try to use a system font
                font_size = 60
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
            
            text = "WSL"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2 - 10
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        # Save as ICO file
        icon_path = Path("icon.ico")
        img.save(icon_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        
        print(f"✓ Created icon file: {icon_path}")
        if source_image:
            print(f"  Converted from: {source_image}")
        print("  The icon will be used for both CLI and GUI executables.")
        return True
        
    except ImportError:
        print("PIL (Pillow) not available. Cannot create icon automatically.")
        print("\nTo create an icon manually:")
        print("1. Install Pillow: pip install Pillow")
        print("2. Run this script again")
        print("\nOr create an icon manually:")
        print("1. Create a 256x256 pixel image")
        print("2. Save it as 'icon.ico' in the project root")
        print("3. Use an online ICO converter if needed")
        return False
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False


def show_icon_alternatives():
    """Show alternative ways to get an icon."""
    print("\n" + "="*60)
    print("Alternative Ways to Get an Icon")
    print("="*60)
    
    print("\n1. Online Icon Generators:")
    print("   - https://favicon.io/favicon-generator/")
    print("   - https://www.icoconverter.com/")
    print("   - https://convertio.co/png-ico/")
    
    print("\n2. Free Icon Resources:")
    print("   - https://icons8.com/")
    print("   - https://www.flaticon.com/")
    print("   - https://feathericons.com/")
    
    print("\n3. Create Your Own:")
    print("   - Use GIMP, Paint.NET, or similar")
    print("   - Create a 256x256 pixel image")
    print("   - Save as .ico format")
    
    print("\n4. WSL-themed Suggestions:")
    print("   - Linux penguin icon")
    print("   - Terminal/console icon")
    print("   - Gear/settings icon")
    print("   - Text 'WSL' with terminal styling")


def main():
    """Main function."""
    print("WSL Manager - Icon Creation Helper")
    print("="*60)
    
    # Check if icon already exists
    if Path("icon.ico").exists():
        print("✓ Icon file already exists: icon.ico")
        response = input("Do you want to recreate it? (y/N): ").lower()
        if response != 'y':
            print("Keeping existing icon file.")
            return
    
    # Try to create icon
    if create_simple_icon():
        print("\n✓ Icon created successfully!")
        print("  You can now build your executables with the custom icon.")
    else:
        show_icon_alternatives()
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("1. If you created an icon, run: python build.py")
    print("2. If you want to use a different icon:")
    print("   - Replace 'icon.ico' with your preferred icon")
    print("   - Run: python build.py")
    print("3. If you don't want an icon:")
    print("   - Edit the .spec files and set icon=None")
    print("   - Run: python build.py")


if __name__ == "__main__":
    main()
