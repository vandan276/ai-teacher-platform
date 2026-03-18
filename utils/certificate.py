import os
try:
    import cloudinary
    import cloudinary.utils
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Cloudinary Config
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

if CLOUDINARY_AVAILABLE and CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )
    CLOUDINARY_CONFIGURED = True
else:
    CLOUDINARY_CONFIGURED = False

def generate_certificate_url(name, completion_date=None):
    """
    Generates a personalized completion certificate.
    Returns a URL if using Cloudinary, or a local file path if using Pillow.
    """
    if not completion_date:
        completion_date = datetime.now().strftime('%B %d, %Y')
    
    # Method A: Cloudinary (API)
    # Note: Requires a base image uploaded to Cloudinary with ID 'certificate_base'
    if CLOUDINARY_CONFIGURED:
        try:
            # This is a conceptual implementation of Cloudinary text overlays
            # In a real scenario, you'd upload the bg first once.
            url, _ = cloudinary.utils.cloudinary_url(
                "certificate_base", # Assumes you uploaded the bg to Cloudinary
                transformation=[
                    {"width": 1000, "crop": "scale"},
                    {"overlay": {"font_family": "Arial", "font_size": 20, "font_weight": "bold", "text": name}, "gravity": "center", "y": -20, "color": "#D4AF37"},
                    {"overlay": {"font_family": "Arial", "font_size": 20, "text": f"Completed on {completion_date}"}, "gravity": "center", "y": 80, "color": "#FFFFFF"}
                ]
            )
            return url
        except Exception as e:
            print(f"DEBUG: Cloudinary generation failed: {e}")

    # Method B: Local Pillow (Fallback) - High Quality Local Generation
    return generate_local_certificate(name, completion_date)

def generate_local_certificate(name, completion_date):
    """
    Generates a certificate using Pillow and saves it to a static/temp folder.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    bg_path = os.path.join(base_dir, 'static', 'images', 'certificate_bg.png')
    output_dir = os.path.join(base_dir, 'static', 'certificates')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_filename = f"cert_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        img = Image.open(bg_path)
        draw = ImageDraw.Draw(img)
        
        W, H = img.size
        
        # Color Palette - Premium Navy & Gold
        COLOR_TITLE = "#1E1B4B"      # Indigo 950 (Dark Navy)
        COLOR_NAME = "#A85507"       # Amber 700 (Goldish)
        COLOR_SECONDARY = "#475569"  # Slate 600
        COLOR_GOLD = "#A85507"       # Amber 700
        COLOR_LINE = "#E2E8F0"       # Slate 200
        
        # Scale font sizes based on image width (normalized to ~1000px)
        scale = W / 1000.0

        # Use a system font (macOS) or fallback to default
        try:
            # Main Serif Fonts - Using Georgia/Arial for premium feel
            title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", int(36 * scale))
            name_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", int(72 * scale))
            sub_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", int(18 * scale))
            date_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Italic.ttf", int(18 * scale))
            footer_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", int(14 * scale))
        except:
            title_font = name_font = sub_font = date_font = footer_font = ImageFont.load_default()
            
        CX, CY = W / 2, H / 2
        
        # 1. Main Header - Positioned higher in the white space
        draw.text((CX, CY - 180 * scale), "CERTIFICATE OF COMPLETION", fill=COLOR_TITLE, font=title_font, anchor="mm")
        
        # 2. Sub-header
        draw.text((CX, CY - 120 * scale), "Awarded to", fill=COLOR_SECONDARY, font=sub_font, anchor="mm")
        
        # 3. Recipient Name (Prominent Gold)
        draw.text((CX, CY - 40 * scale), name.upper(), fill=COLOR_NAME, font=name_font, anchor="mm")
        
        # 4. Ornate Line under name
        bbox = draw.textbbox((CX, CY - 40 * scale), name.upper(), font=name_font, anchor="mm")
        name_w = bbox[2] - bbox[0]
        line_y = CY + 20 * scale
        draw.line([CX - name_w/2 - 30 * scale, line_y, CX + name_w/2 + 30 * scale, line_y], fill=COLOR_GOLD, width=int(3 * scale))
        
        # 5. Achievement Description
        draw.text((CX, CY + 70 * scale), "for successfully mastering all modules of the", fill=COLOR_SECONDARY, font=sub_font, anchor="mm")
        
        # Special catch for program title font
        try:
            program_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", int(24 * scale))
        except:
            program_font = sub_font
            
        draw.text((CX, CY + 110 * scale), "Microsoft Elevate: AI Teacher Training Program", fill=COLOR_TITLE, font=program_font, anchor="mm")

        # 6. Success Metrics / Footer
        draw.text((CX, CY + 180 * scale), f"Verified on {completion_date}", fill=COLOR_GOLD, font=date_font, anchor="mm")
        
        # 7. Subtle ID or Authenticity Note - Moved to bottom right corner area
        cert_id = f"ID: MS-ELV-{hash(name) % 10000:04d}"
        draw.text((W - 120 * scale, H - 100 * scale), cert_id, fill="#94A3B8", font=footer_font, anchor="rm")
        
        img.save(output_path)
        return f"/static/certificates/{output_filename}"
    except Exception as e:
        print(f"DEBUG: Local certificate generation failed: {e}")
        return None
