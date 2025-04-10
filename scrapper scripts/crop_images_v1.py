import os
from PIL import Image

# Configuration
INPUT_FOLDER = "scrapped_images_v1"
OUTPUT_FOLDER = "cropped_images_v1"
TARGET_SIZE = (415, 415)
TOP_ADJUSTMENT = 10  # Extra pixels to remove from top

def adjusted_crop():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    image_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    for filename in image_files:
        try:
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            
            with Image.open(input_path) as img:
                width, height = img.size
                
                if width < TARGET_SIZE[0] or height < TARGET_SIZE[1]:
                    print(f"Skipping {filename} - Image too small ({width}x{height})")
                    continue
                
                # Calculate crop coordinates with top adjustment
                left = (width - TARGET_SIZE[0]) // 2
                top = ((height - TARGET_SIZE[1]) // 2) + TOP_ADJUSTMENT
                
                # Ensure we don't crop outside the image bounds
                top = max(0, min(top, height - TARGET_SIZE[1]))
                right = left + TARGET_SIZE[0]
                bottom = top + TARGET_SIZE[1]

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img.save(output_path, quality=95)
                
            print(f"Processed: {filename} [Removed {top}px from top]")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    adjusted_crop()
    print("Top-adjusted cropping completed!")