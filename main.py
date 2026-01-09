from PIL import Image
from flask import Flask, render_template, request
import os

img = Image.open('colorful.jpg')

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OUTPUT_DIR = "static/result"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return "No file uploaded"

    with Image.open(file.stream) as img:
        img = img.convert("RGB")
        
        # Calculate colors
        max_c = img.size[0] * img.size[1]
        color_counts = img.getcolors(maxcolors=max_c)
        
        if color_counts:
            sorted_colors = sorted(color_counts, key=lambda x: x[0], reverse=True)
            most_frequent_color_counts = sorted_colors[:10]
            
            # Return the template just like before
            return render_template("colors.html", color_counts=most_frequent_color_counts)
        else:
            return "Too many colors!"
                    

if __name__ == '__main__':
    app.run(debug=True)

