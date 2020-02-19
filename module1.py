
import flask
import werkzeug
import time

app = flask.Flask(__name__)

@app.route('/getNoteText',methods=['GET','POST'])
def GetNoteText():
    if request.method == 'POST':
        file = request.files['pic']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        processImage(filename)            
    else:
        return "Y U NO USE POST?"