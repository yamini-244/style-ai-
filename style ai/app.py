from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -------- Skin Tone Detection --------
def detect_skin_tone(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, _ = img.shape
    center_crop = img[h//4:3*h//4, w//4:3*w//4]

    avg_color = np.mean(center_crop.reshape(-1, 3), axis=0)
    r, g, b = avg_color

    if r > 200 and g > 180:
        tone = "Fair"
    elif r > 160 and g > 130:
        tone = "Medium"
    elif r > 120 and g > 100:
        tone = "Olive"
    else:
        tone = "Deep"

    return tone, (int(r), int(g), int(b))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    gender = request.form.get('gender')

    if not file:
        return jsonify({"error": "No file uploaded"})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    skin_tone, rgb = detect_skin_tone(filepath)

    # Simple AI fallback recommendation
    recommendation = f"""
    Based on your {skin_tone} skin tone:

    • Try pastel and neutral shades
    • Gold or silver accessories
    • Smart casual and formal outfits
    • Keep hairstyle clean and structured

    Gender selected: {gender}
    """

    return jsonify({
        "skin_tone": skin_tone,
        "rgb": rgb,
        "recommendation": recommendation
    })


if __name__ == '__main__':
    app.run(debug=True)