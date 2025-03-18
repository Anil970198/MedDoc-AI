import os
import google.generativeai as genai
from PIL import Image

# ✅ Load API Key from .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Ensure API key is available
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

# ✅ Initialize Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro-vision")

def extract_text_from_image(image_path):
    """Extract handwritten text from an image using Google Gemini API."""
    try:
        # ✅ Ensure the file exists
        if not os.path.exists(image_path):
            return f"Error: File '{image_path}' not found."

        # ✅ Open image using PIL (Google Gemini expects an actual image object)
        image = Image.open(image_path)

        # ✅ Debugging: Check if image is loaded correctly
        print(f"Processing image: {image_path}, Format: {image.format}, Mode: {image.mode}")

        # ✅ Send image for recognition
        response = model.generate_content([image])

        # ✅ Debugging: Print full API response
        print("API Response:", response)

        # ✅ Extract text from response
        recognized_text = response.text if response else "No text recognized."
        return recognized_text

    except Exception as e:
        return f"Error processing image: {str(e)}"

# ✅ Example usage
if __name__ == "__main__":
    image_path = "/Users/anilkumar/PyCharm Projects/MedDoc/new_backend/images/precptn.jpeg"  # Replace with an actual image path
    extracted_text = extract_text_from_image(image_path)
    print("\nExtracted Handwritten Text:", extracted_text)
