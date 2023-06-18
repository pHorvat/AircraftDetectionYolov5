from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_and_detect():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            
            output_file = run_detection(file_path)
            output_path = os.path.join('static', output_file)
            
            return render_template('result.html', image_path=output_path)
        
    return render_template('home.html')

def run_detection(image_path):
    # Run the detect.py script with the provided image path
    command = f'python detect.py --weights best.pt --source "{image_path}" --name detect_su57'
    os.system(command)
    
    # Extract the output file name from the detect.py output
    output_file = 'runs/detect/detect_su57/' + os.path.basename(image_path)
    return output_file

if __name__ == '__main__':
    app.run(debug=True)
