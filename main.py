from  flask import Flask , render_template ,request,flash,redirect
import os
from werkzeug.utils import secure_filename
import cv2
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processimage(filename,operation):
    print(f"the operation is {operation} and the filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
            newFilename =f"static/{filename}"
            cv2.imwrite(newFilename,imgProcessed)
            return newFilename
        
        case "cwebp":
            newFilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename,img)
            return newFilename

        case "cpng":
            newFilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename,img)
            return newFilename

        case "c":
            newFilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename,img)
            return newFilename


app.secret_key = 'ahshdg224242#@vjfj'


@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/about")
def about():
    return render_template("about.html") 
@app.route("/edit" ,  methods =["GET","POST"])
def edit():
    if request.method =="POST":
        operation = request.form.get("operation")

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processimage(filename , operation)

            flash(f"your image has been processed and is availaible <a href ='/{new}'>here</a>")

            return render_template("index.html")
    

    return render_template("about.html") 
# app.run(debug =True,port=9000)
