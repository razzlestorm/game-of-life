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


    # Main route
    @app.route('/', methods=['GET'])
    def index():
        files = os.listdir(f"{app.config['UPLOADS_DEFAULT_DEST']}/photos")
        images = []
        for f in files:
            resize(photos.path(f))
            binarize(photos.path(f))
            images.append(photos.url(f))
        print(f"request.args.get(gameboard) = {request.args.get('gameboard')}")
        print(f"photos path = {photos.path('board1.jpg')}")
        if not request.args.get('gameboard'):
            gameimg = 'bird.jpg'
        else:
            gameimg = request.args.get('gameboard')
        print(f"gameimg = {gameimg}")
        print(f"path = {photos.path(gameimg)} url = {photos.url(gameimg)}")
        gameimg_path = photos.path(gameimg)
        gamegrid = np.array(Image.open(gameimg_path)).tolist()
        print(gamegrid[:10])
        return render_template('index.html', images=images, gameimg=photos.url(gameimg), gamegrid=gamegrid)

        # TO DO FINISH THIS ############################################
        '''files = os.listdir(app.config['UPLOAD_PATH'])
        for f in files:
            resize(f'./flask-app/uploads/{f}')
            binarize(f'./flask-app/uploads/{f}')
        if not request.args.get('gameboard'):
            gameimg = './flask-app/uploads/bird.jpg'
        else:
            gameimg = f".{request.args.get('gameboard')}"
        gamegrid = np.array(Image.open(gameimg)).tolist()
        print(gameimg[11:])
        return render_template('index.html', files=files, gameimg=gameimg, gamegrid=gamegrid)'''

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


    '''    # This route handles image uploads and upload checking (w/ Submit button)
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
        return redirect(url_for('index'))'''
    


    # This route gets the request for the user's game board from the "Play..." button
    @app.route("/game" , methods=['GET', 'POST'])
    def game():
        select = request.form.get('filedrop').replace("pic-game-of-life.herokuapp.com/_uploads/photos/", "")
        print(f"selected = {select}")
        return redirect(url_for('index', gameboard=select))

    
    @app.route('/delete_uploads')
    def delete():
        for fil in glob.glob('./flask-app/uploads/*'):
            if fil != './flask-app/uploads\\bird.jpg':
                os.remove(fil)
        return "Images deleted!"
    
    
    return app



APP = create_app()

if __name__ == "__main__":
    APP.run()
