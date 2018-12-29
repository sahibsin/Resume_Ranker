
from flask import Flask
import os

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import model

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'blah_Blah'
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def uploaded():
    flash('JD & Resume have been successfully uploaded!')
    model.main()
    return render_template('webpage.html')

@app.route('/ranking')
def ranking_html():
    return render_template('htmlData.html')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basically show on the browser the uploaded file
        return redirect(url_for('uploaded'))
        # return redirect(url_for('uploaded_file', filename=filename))

    elif file.filename == '':
        return ''' No selected file '''

    else:
        return ''' unsupported file type '''


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return ''' File Successfully Uploaded '''
    # return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                            filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)