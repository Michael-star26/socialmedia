import base64
from flask import *
import pymysql
connection=pymysql.connect(database='umber',host='localhost',password='',user='root')
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER='./static/files/images'
PROFILE_UPLOAD_FOLDER='./static/files/profilePic'
ALLOWED_EXTENSIONS={'txt','mp4','MP4',"jpg", "JPG", 'png', 'PNG', 'gif', 'GIF', 'tiff', 'TIFF', 'heic',
                  'HEIC', 'jpeg', 'JPEG', 'jpg', 'JPG', 'jpe', 'JPE', 'jffif', 'JFFIF', 'bmp', 'BMP', 'dib', 'DIB'}
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['PROFILE_UPLOAD_FOLDER']=PROFILE_UPLOAD_FOLDER
app.secret_key=['vhdhkjcvd%^$%&$^vb&%*jkhgJH^$u3546hggfd$%&&*(h4466#$#347$$hh341642HGUGFXUGufxu9(*667*%ygxwu']
@app.route("/",methods=['POST','GET'])
def index():
    postsql="select * from posts"
    postcursor=connection.cursor()
    postcursor.execute(postsql)
    posts=postcursor.fetchall()
    return render_template("index.html",user_posts=posts)

# ======cart=====
@app.route('/headline')
def headline():
    return render_template("headline.html")

#==== end of cart ======

def allowedFiles(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
# ====signup====
@app.route("/signup",methods=['POST','GET'])
def signup():
    # This piece of code will be executed when the user submits the form
    if request.method=='POST':
        username=request.form['username']
        useremail=request.form['useremail']
        pswd=request.form['password']
        confirmPassword=request.form['confirmPassword']
        dateOfBirth=request.form['dateOfBirth']
        avatar="Default Avatar"
        # search for preexisting username and email to avoid duplicates
        confirmUserEmailSql="select useremail from users where useremail=%s"
        confirmUserNameSql="select username from users where username=%s"
        confirmUserName_cursor=connection.cursor()
        confirmUserName_cursor.execute(confirmUserNameSql,username)
        confirmUserEmail_cursor=connection.cursor()
        confirmUserEmail_cursor.execute(confirmUserEmailSql,useremail)
        if 'file' not in request.files:
            return render_template("signup.html", error="No file part in post")
        file = request.files['file']
        if confirmUserName_cursor.rowcount !=0:
            duplicateNames=confirmUserName_cursor.fetchone()
            return render_template("signup.html",error=f'user { username } already exists')
        elif confirmUserEmail_cursor.rowcount !=0:
            duplicateEmail=confirmUserEmail_cursor.fetchone()
            return render_template("signup.html",error=f'The email {useremail} already exists')
        elif " " in username:
            return render_template("signup.html",error="No whitespace allowed in username")
        elif not username:
            return render_template("signup.html", error="Username cannot be empty")
        elif  '@' not in useremail:
            return render_template("signup.html",error="Incorrect email format")
        elif not useremail:
            return render_template("signup.html", error="Email cannot be empty")
        elif len(pswd)<8:
            return render_template("signup.html",error="Password Must be atleast 8 characters long")
        elif not pswd:
            return render_template("signup.html", error="Password cannot be empty")
        elif not confirmPassword:
            return render_template("signup.html", error="Please Confirm your Password")
        elif pswd != confirmPassword:
            return render_template("signup.html",error="Password do not match")
        elif file.filename == "":
            return render_template("signup.html", error="No file chosen")
        elif not allowedFiles(file.filename):
            return render_template("signup.html", error="Unsupported file type")
        elif "_" in file.filename:
            return render_template("signup.html", error="File name should not contain space")
        elif " " in file.filename:
            return render_template("signup.html", error="File name should not contain space")
        elif not dateOfBirth:
            return render_template("signup.html", error="D.O.B cannot be empty")
        else:
            # upload profile photo
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], filename))
            media = file.filename
            from image_processing import images
            mymedia = images(media)
            profile_pic = mymedia.replace("'", "")
            # ====insert data into database====
            from datetime import datetime
            regDate = datetime.now()
            # convert password to b64 format
            import base64
            password_in_bytes = pswd.encode("ascii")
            password = base64.b64encode(password_in_bytes)
            sql="insert into users(profile_pic,password,username,useremail,regDate,dateOfBirth,avatar) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cursor=connection.cursor()
            cursor.execute(sql,(profile_pic,password,username,useremail,regDate,dateOfBirth,avatar))
            connection.commit()
            old_name = f"./static/files/profilePic/{media}"
            new_name = f"./static/files/profilePic/{profile_pic}"
            if os.path.isfile(new_name):
                return render_template("signup.html", error="Failed to upload your profile picture.",Message="You can Upload the photo later.Proceed to login")
            else:
                os.rename(old_name, new_name)
            session["signedUp"]=username
            return redirect("/")
    else:
        # This piece of code will be executed when the user first visits the sign up page
        return render_template("signup.html",error='Signup',secure="user()",
                               secure2="oninput",myId="username",myupload="file")
# ====end of signup=======

# ====end of login=======
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        useremail=request.form['useremail']
        pswd=request.form['password']
        password_to_ascii=pswd.encode("ascii")
        password=base64.b64encode(password_to_ascii)
        sql="select * from users where useremail=%s and password=%s"
        userSql="select username from users where useremail=%s and password=%s"
        usercursor=connection.cursor()
        usercursor.execute(userSql,(useremail,password))
        cursor=connection.cursor()
        cursor.execute(sql,(useremail,password))
        user_details=usercursor.fetchone()
        profile_sql = "select * from users where useremail=%s and password=%s"
        profilecursor = connection.cursor()
        profilecursor.execute(profile_sql, (useremail, password))
        user_prof=profilecursor.fetchone()
        if not password:
            return render_template("login.html", error="Password cannot be empty")
        elif not useremail:
            return render_template("login.html", error="Email cannot be empty")
        elif cursor.rowcount==0:
            return render_template("login.html",error="No account matches your details")
        elif usercursor.rowcount==0:
            return render_template("login.html", error="No account matches your details")
        else:
            user=user_details[0]
            profile=user_prof[7]
            session['profile']=profile
            session['LoggedIn']=user
            status = "Online"
            sql = "update users set status=%s where useremail=%s"
            cursor = connection.cursor()
            cursor.execute(sql, (status, useremail))
            connection.commit()
            session['online'] = status
            return redirect('/')
    else:
        messages="Please Login"
        session['notLoggedIn']=messages
        return render_template("login.html",error="Login")
# ====end of login=======


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
#====== post plus upload=======
@app.route('/post/<username>',methods=['POST','GET'])
def post(username):
    if request.method=='POST':
        postBody=request.form['user_post']
        from datetime import datetime
        postTime = datetime.now()
        if 'file' not in request.files:
            return render_template("post.html", error="No file part in post")
        file = request.files['file']
        if not postBody:
            return render_template("post.html",error="Empty Posts aren't allowed")
        elif not  username:
            return render_template("post.html", error="Please Login or Create an account")
        elif file.filename == "":
            return render_template("post.html", error="No file chosen")
        elif not allowed_files(file.filename):
            return render_template("post.html", error="Unsupported file type")
        elif "_" in file.filename:
            return render_template("post.html", error="File name should not contain space")
        elif " " in file.filename:
            return render_template("post.html", error="File name should not contain space")
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            userSql="select * from users where username=%s"
            usercursor=connection.cursor()
            usercursor.execute(userSql,(username))
            id=usercursor.fetchone()
            user_id=id[3]
            media=file.filename
            from image_processing import images
            mymedia=images(media)
            mediaName=mymedia.replace("'","")
            sql="insert into posts(postBody,user_id,postTime,mediaName) VALUES(%s,%s,%s,%s)"
            cursor=connection.cursor()
            cursor.execute(sql,(postBody,user_id,postTime,mediaName))
            connection.commit()
            old_name=f"./static/files/images/{media}"
            new_name=f"./static/files/images/{mediaName}"
            os.rename(old_name,new_name)
            return render_template("post.html",message="Posted Successfully")
    else:
        return render_template("post.html", message="Post")

# ======end of post===

#====== reader=======
@app.route('/readerPage')
def readerPage():
    return render_template("readerPage.html")
# ======end of reader=====

#====== video media play=======

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/videoMedia',methods=['POST','GET'])
def videoMedia():
    if request.method=='POST':
        if 'file' not in request.files:
            return render_template("videoMedia.html",error="No file part")
        file=request.files['file']
        if file.filename=="":
            return render_template("videoMedia.html",error="No file chosen")
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            flash("success")
            # return redirect(url_for('upload_file', name=filename))
            return  render_template("videoMedia.html",error="success")
    return render_template("videoMedia.html")
# ======end video media play=====

#====== socialise=======
@app.route('/socialise')
def socialise():
    return render_template("socialise.html")
# ======end of socialise=====

#====== followers=======
@app.route('/followers')
def followers():
    return render_template("followers.html")
# ======end of followers=====


#====== following=======
@app.route('/following')
def following():
    return render_template("following.html")
# ======end of following=====

#====== Photo =======
@app.route('/photoMedia')
def photoMedia():
    return render_template("photoMedia.html")
# ======end of following=====

#====== blogThreadOne =======
@app.route('/threadOne')
def threadOne():
    return render_template("threadOne.html")
# ======end of threadOne=====

#====== blogThreadTwo =======
@app.route('/threadTwo')
def threadTwo():
    return render_template("threadTwo.html")
# ======end of threadTwo=====

#====== blogThreadThree =======
@app.route('/threadThree')
def threadThree():
    return render_template("threadThree.html")
# ======end of threadThree=====

#====== blogThreadFour =======
@app.route('/threadFour')
def threadFour():
    return render_template("threadFour.html")
# ======end of threadFour=====

#====== profile =======
@app.route('/profile/<username>')
def profile(username):
    return render_template("profile.html")
# ======end of profile=====

#====== comments =======
@app.route('/comments')
def comments():
    return render_template("comments.html")
# ======end of comments=====

#====== messages =======
@app.route('/messages')
def messages():
    return render_template("messages.html")
# ======end of messages===

#====== admin =======
@app.route('/admin')
def admin():
    return render_template("admin.html")
# ======end of admin===


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
# ======end video media play=====
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
@app.route("/sematic")
def sematic():
    return render_template("sematic.html")


if __name__=='__main__':
    app.run(debug=True)