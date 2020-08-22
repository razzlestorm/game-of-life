
import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from .image_converter import binarize, resize
import glob
import time



def allowed_image(filename, extensions):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in extensions:
        return True
    else:
        return False



def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    cors = CORS(app)

    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['UPLOAD_PATH'] = 'uploads'

    def validate_image(stream):
        header = stream.read(512)  # 512 bytes should be enough for a header check
        stream.seek(0)  # reset stream pointer
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')

    @app.route('/')
    def index():
        files = os.listdir(app.config['UPLOAD_PATH'])
        for f in files:
            resize(f'uploads/{f}')
            binarize(f'uploads/{f}')
        return render_template('index.html', files=files)

    @app.route('/', methods=['POST'])
    def upload_files():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            time.sleep(1)
        return redirect(url_for('index'))

    @app.route('/uploads/<filename>')
    def upload(filename):
        return send_from_directory(app.config['UPLOAD_PATH'], filename)
    
    @app.route('/delete_uploads')
    def delete():
        for fil in glob.glob('./uploads/*'):
            os.remove(fil)
        return "Images deleted!"
    
    
    return app




APP = create_app()

if __name__ == "__main__":
    APP.run()
