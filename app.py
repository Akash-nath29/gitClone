import os
import mimetypes    
from flask import Flask, render_template, request, send_file, redirect
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from datetime import date

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'MLXH243rjbGu38iBIbibIUBImmfrdTWS7FDhdwYF56wPj8'

db = SQLAlchemy(app)
#TODO: make the database with these components: id, filename, filedata, date
class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), nullable = False)
    fileData = db.Column(db.BLOB, nullable = False)
    fileDescription = db.Column(db.Text(5000), nullable = True)
    date = db.Column(db.String(100), nullable = True)
    repoName = db.Column(db.String(100), nullable=False)
    
    def __init__(self, filename, fileData, fileDescription, date, repoName):
        self.filename = filename
        self.fileData = fileData
        self.fileDescription = fileDescription
        self.date = date
        self.repoName = repoName

@app.route('/')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)


@app.route('/upload', methods=['GET', 'POST'])
def postFile():
    if request.method == 'POST':
        filelist = request.files.getlist('fileData')
        for file in filelist:
            filename = file.filename
            filedata = file.read()
            fileDescription = request.form.get('fileDescription')
            repoName = request.form.get('repoName')
            newFile = File(filename=filename, fileData=filedata, fileDescription=fileDescription, date=date.today(), repoName=repoName)
            db.session.add(newFile)
            db.session.commit()
        return redirect('/')
        
    return render_template('upload.html')

@app.route('/<int:id>/view')
def viewFile(id):
    file = File.query.get(id)
    mime_type, _ = mimetypes.guess_type(file.filename)
    return render_template('viewFile.html', file=file)

@app.route('/<int:id>/download')
def download(id):
    file = File.query.get(id)
    fileExtension = file.filename.split('.')
    return send_file(BytesIO(file.fileData), mimetype='', download_name=f'C:\\Users\\AKASH NATH\\folder\\DownloadsfileShare.{fileExtension[1]}', as_attachment=True)

@app.route('/<int:id>/delete')
def deleteFile(id):
    fileToDelete = File.query.get(id)
    db.session.delete(fileToDelete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')