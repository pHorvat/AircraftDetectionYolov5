import os
from flask import Flask, request, render_template
from PIL import Image
import torch

app = Flask(__name__)

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='path/to/your/model.pt')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded image
        image = request.files['image']
        image_path = os.path.join('static', 'uploads', image.filename)
        image.save(image_path)

        # Process the image using the YOLOv5 model
        results = model(image_path)

        # Get the path of the output image
        output_image_path = results.save(save_dir='static', save_img=True)

        # Render the template with the output image
        return render_template('index.html', output_image=output_image_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
