from flask import Flask, request
from flask import Flask, send_file
from flask_cors import CORS  # Import CORS from flask_cors
import melody_master as mm
import notes_optimizer
import os
import csv

app = Flask(__name__)
CORS(app)  # Initialize CORS for your Flask app

@app.route('/upload', methods=['POST'])
def upload_file():
    os.remove("notes_csv/noteslist.csv")
    print("uploading")
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file to a specific location

    file.save('uploads/raw_music.mid')  # Save to the 'uploads' folder
    notes_list = mm.process_music()
    notes_list = notes_optimizer.optimize_notes(notes_list)

    filename = 'notes_csv/noteslist.csv'
    fobj = open(filename, 'w')
    for i in notes_list:
        fobj.write(str(i) + '\n')
    fobj.close()
    return 'File uploaded successfully', 200


@app.route('/getFile')
def generate_file():
    # Replace the file path with your actual file path
    file_path = 'notes_csv/noteslist.csv'
    os.remove("uploads/raw_music.mid")
    os.remove("processed_music/processed_music.mid")
    return send_file(file_path, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])  # Allow POST method for the root route
def index():
    if request.method == 'POST':
        # Handle POST requests here if needed
        return 'Received POST request', 200
    else:
        return 'JamJam', 200


if __name__ == '__main__':
    app.run(debug=True)
