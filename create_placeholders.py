import os
from PIL import Image, ImageDraw, ImageFont

# Create directories if they don't exist
directories = [
    'images/logo',
    'images/caravan',
    'images/traveller',
    'images/icu',
    'images/urbania',
    'images/campaign',
    'images/interior'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create placeholder images
categories = {
    'logo': ['logo1.jpg', 'logo2.jpg'],
    'caravan': ['caravan1.jpg', 'caravan2.jpg'],
    'traveller': ['traveller1.jpg', 'traveller2.jpg'],
    'icu': ['icu1.jpg', 'icu2.jpg'],
    'urbania': ['urbania1.jpg', 'urbania2.jpg', 'urbania3.jpg'],
    'campaign': ['campaign1.jpg'],
    'interior': ['interior1.jpg', 'interior2.jpg']
}

# Colors for different categories
colors = {
    'logo': (30, 60, 114),
    'caravan': (42, 82, 152),
    'traveller': (30, 60, 114),
    'icu': (42, 82, 152),
    'urbania': (30, 60, 114),
    'campaign': (42, 82, 152),
    'interior': (30, 60, 114)
}

# Create images for each category
for category, filenames in categories.items():
    for filename in filenames:
        # Create a new image
        img = Image.new('RGB', (400, 250), color=colors[category])
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            # Try to use a better font if available
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        text = f"{category.capitalize()} Image"
        # Get text dimensions (newer Pillow versions)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (400 - text_width) // 2
        y = (250 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Save the image
        img.save(f'images/{category}/{filename}')

print("Placeholder images created successfully!")