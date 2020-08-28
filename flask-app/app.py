import os
from flask import Flask, render_template, request, redirect, url_for, abort, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask_uploads import UploadSet, configure_uploads, IMAGES
from .image_converter import binarize, resize, validate_image
import glob
import time
from PIL import Image
import numpy as np
from flask_bootstrap import Bootstrap 
import re


def create_app():
    """Create and configure an instance of the Flask application"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    cors = CORS(app)
    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['UPLOADS_DEFAULT_DEST'] = 'flask-app/static/img/uploads'
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    img_path = '/static/img/uploads/photos/'


    # Main route
    @app.route('/', methods=['GET'])
    def index():
        images = os.listdir(f"{app.config['UPLOADS_DEFAULT_DEST']}/photos")
        for img in images:
            resize(photos.path(img))
            binarize(photos.path(img))
        print(f"request.args.get(gameboard) = {request.args.get('gameboard')}")
        print(f"photos path = {photos.path('board1.jpg')}")
        if not request.args.get('gameboard'):
            gameimg = 'bird.jpg'
            gamegrid = np.array(Image.open(photos.path(gameimg))).tolist()
        else:
            gameimg = request.args.get('gameboard')
            gamegrid = np.array(Image.open(photos.path(gameimg))).tolist()
        print(f"gameimg = {gameimg}")
        print(f"path = {photos.path(gameimg)} url = {photos.url(gameimg)}")
        print(gamegrid[:10])
        return render_template('index.html', images=images, gameimg=photos.path(gameimg)[9:], gamegrid=gamegrid, img_path=img_path)

    @app.route('/', methods=['POST'])
    def upload_files():
        if "file_names" not in session:
            session['file_names'] = []
        file_names = session['file_names']
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            # save the file with to our photos folder
            file_names.append(photos.url(filename))
        session['file_names'] = file_names
        return redirect(url_for('index'))

    # This route gets the request for the user's game board from the "Play..." button
    @app.route("/game" , methods=['GET', 'POST'])
    def game():
        select = request.form.get('filedrop')
        print(f"selected = {select}")
        select = select[len(img_path):]
        return redirect(url_for('index', gameboard=select))

    
    @app.route('/delete_uploads')
    def delete():
        for fil in glob.glob('./flask-app/static/img/uploads/*'):
            if fil != './flask-app/static/img/uploads/bird.jpg':
                os.remove(fil)
        return "Images deleted!"
    
    
    return app



APP = create_app()

if __name__ == "__main__":
    APP.run()
