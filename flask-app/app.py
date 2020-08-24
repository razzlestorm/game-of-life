import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from .image_converter import binarize, resize, validate_image
import glob
import time
from flask_bootstrap import Bootstrap 




def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    cors = CORS(app)
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['UPLOAD_PATH'] = 'uploads'

    # Main route
    @app.route('/')
    def index():
        files = os.listdir(app.config['UPLOAD_PATH'])
        for f in files:
            resize(f'uploads/{f}')
            binarize(f'uploads/{f}')
        if not request.args.get('gameboard'):
            gameboard = '/uploads/bird.jpg'
        else:
            gameboard = request.args.get('gameboard')
        return render_template('index.html', files=files, board=gameboard)

    # This route handles image uploads and upload checking (w/ Submit button)
    @app.route('/', methods=['POST'])
    def upload_files():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                print('Please try a different image!')
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            time.sleep(1)
        return redirect(url_for('index'))

    # This route sends the filename found in the directory to index
    @app.route('/uploads/<filename>')
    def upload(filename):
        return send_from_directory(app.config['UPLOAD_PATH'], filename)

    # This route gets the request for the user's game board from the "Play..." button
    @app.route("/game" , methods=['GET', 'POST'])
    def game():
        select = request.form.get('filedrop')
        return redirect(url_for('index', gameboard=select))

    
    @app.route('/delete_uploads')
    def delete():
        for fil in glob.glob('./uploads/*'):
            if fil != './uploads\\bird.jpg':
                os.remove(fil)
        return "Images deleted!"
    
    
    return app



APP = create_app()

if __name__ == "__main__":
    APP.run()
