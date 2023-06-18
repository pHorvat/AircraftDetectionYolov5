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
            
            return render_template_string(result_template, image_path=output_path)
        
    return render_template_string(index_template)

def run_detection(image_path):
    # Run the detect.py script with the provided image path
    command = f'python detect.py --weights best.pt --source "{image_path}" --name detect_su57'
    os.system(command)
    
    # Extract the output file name from the detect.py output
    output_file = 'runs/detect/detect_su57/' + os.path.basename(image_path)
    return output_file

index_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Upload and Detect</title>
</head>
<body>
    <h1>Upload an Image</h1>
    <form method="POST" action="/" enctype="multipart/form-data">
        <input type="file" name="file" accept=".jpg,.jpeg,.png">
        <input type="submit" value="Detect">
    </form>
</body>
</html>
'''

result_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Detection Result</title>
</head>
<body>
    <h1>Detection Result</h1>
    <img src="{{ image_path }}" alt="Detected Image">
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
