import os
from flask import Flask, redirect, url_for, request, flash, render_template
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone


ALLOWED_EXTENSIONS = {}

app = Flask(__name__)
UPLOAD_FOLDER = '/home/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'asrtarstaursdlarsn'


app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.csv, .xlsx'
app.config['DROPZONE_DEFAULT_MESSAGE'] =  "Drop a Quote Excel/CSV Here"

dropzone = Dropzone(app)






@app.route("/")
def hello():
    return "Hello World!"


'''
@app.route("/.auth/login/aad/callback")n
def authcallback():
    print("HEEREauth")
    print(request.params)
    print(request.params.get('access_token'))
    return redirect(url_for('/hello'))
'''


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            # store file name in some location
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return
    return render_template('upload.html')

@app.route('/result')
def result():
     #
     # submit quote against model and store results in blob
     # render results from blob into a serverside rendered chart
     quote_probability = 100
     filename = 'FileName.xlsx'
     return render_template('upload.html', file_name=filename, quote_probability=str(quote_probability) + '%')



@app.route('/snowflake')
def snowflake():
    con = snowflake.connector.connect(
    user=os.environ.get('SNOWFLAKE_USER'),
    password=os.environ.get('SNOWFLAKE_PASSWORD'),
    account=os.environ.get('SNOWFLAKE_ACCOUNT'),
    )
    data = con.cursor().execute("SHOW USERS;")
    print(data)
    return '<html><body><div>' + str(data) + '</div><body></html>'

if __name__ == '__main__':
    port= os.environ.get('PORT')
    app.run(host='0.0.0.0', debug=False, port=port)