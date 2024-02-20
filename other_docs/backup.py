# from datetime import datetime,timedelta
# now=datetime.now()
# print(now)
#
# secureStorage={
#                 'nonce':'nonce',
#                 'tag':'tag',
#                 'ciphertext':'ciphertext',
#                 'key':'key'
#             }
# import  json
# jsonObject=json.dumps(secureStorage,indent=4)
# print(jsonObject)
#
# import base64
# asciiencrypted=jsonObject.encode("ascii")
# base64Encoded=base64.b64encode(asciiencrypted)
# decryptedPass=base64.b64decode(base64Encoded)
# print(f'Encoded is {base64Encoded}')
# print(f'Decoded is {decryptedPass}')

from flask import *
import pymysql
connection=pymysql.connect(database='umber',host='localhost',password='',user='root')
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
app=Flask(__name__)
app.secret_key=['vhdhkjcvd%^$%&$^vgcugsb&%*jkhgJH^$u3546341642HGUGFXUGufxu9(*667*%ygxwguvudgfyewfdeuwfgvu']
@app.route("/",methods=['POST','GET'])
def index():
    family = {"dad", "mom", "becky", 'atieno', "Tom","Dani","Waya","Pheli"}
    return render_template("index.html",myFamily=family)

# ======cart=====
@app.route('/headline')
def headline():
    return render_template("headline.html")

#==== end of cart ======

# ====nav====
@app.route('/navbar')
def navbar():
    return render_template("navbar.html")
# ====end of nav====

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
        elif not dateOfBirth:
            return render_template("signup.html", error="D.O.B cannot be empty")
        else:
            # =====ENCRYPTION=====
            # convert to base 64 before AES encryption
            import base64
            password_in_bytes=pswd.encode("ascii")
            base64Encoded=base64.b64encode(password_in_bytes)
            decryptedPass=base64.b64decode(base64Encoded)
            data=base64Encoded
            # AES encryption
            key =get_random_bytes(16)
            cipher=AES.new(key,AES.MODE_EAX)
            ciphertext,tag=cipher.encrypt_and_digest(data)
            nonce=cipher.nonce
            # this, advanceEncryption, is what we are going to store as password
            advanceEncryption=ciphertext
            secureStorage={
                'nonce':nonce,
                'tag':tag,
                'ciphertext':ciphertext,
                'key':key
            }
            # decrypting AES
            cipher=AES.new(key,AES.MODE_EAX,nonce)
            decryptedData=cipher.decrypt_and_verify(secureStorage['ciphertext'],secureStorage['tag'])
            # ======END OF ENCRYPTION====

            myNonce=secureStorage['nonce']
            myTag=secureStorage['tag']
            myCipher=secureStorage['ciphertext']
            myKey=secureStorage['key']
            # ====insert data into database====
            from datetime import datetime
            regDate = datetime.now()
            sql="insert into users(advanceEncryption,username,useremail,regDate,dateOfBirth,avatar) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor=connection.cursor()
            cursor.execute(sql,(advanceEncryption,username,useremail,regDate,dateOfBirth,avatar))
            connection.commit()
            # fetch user_id from users table
            userIDsql = "select user_id from users where username=%s"
            cursorUserId=connection.cursor()
            cursorUserId.execute(userIDsql,username)
            userId=cursorUserId.fetchone()
            user_id=userId
            # we insert the user id along side othere cridentials in this table
            sql_2 = "insert into mycreds(myNonce,myTag,myCipher,myKey,user_id) VALUES (%s,%s,%s,%s,%s)"
            cursor=connection.cursor()
            cursor.execute(sql_2,(myNonce,myTag,myCipher,myKey,user_id))
            connection.commit()
            session["signedUp"]=username
            return render_template("index.html",message = f'Welcome to this platform ~ {username}')
    else:
        # This piece of code will be executed when the user first visits the sign up page
        arr=['Mike','Tom','Atis','Lucy','Becky','Mum','Dad']
        return render_template("signup.html",error='Signup',secure="user()",
                               secure2="oninput",myId="username",arrays=arr,myupload="file")
# ====end of signup=======

#====== reader=======
@app.route('/readerPage')
def readerPage():
    return render_template("readerPage.html")
# ======end of reader=====

#====== video media play=======
@app.route('/videoMedia')
def videoMedia():
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
@app.route('/profile')
def profile():
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


#====== post plus upload=======
@app.route('/post')
def post():
    return render_template("post.html")
# ======end of post===

if __name__=='__main__':
    app.run(debug=True)



from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER='./static/upload_trial'
ALLOWED_EXTENSIONS={'txt','jpg','png','pdf'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
def allowed_files(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload_trial',methods=['POST','GET'])
def upload_trial():
    if request.method=='POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template("upload_trial.html",error="No file part in post")
        file=request.files['file']
        if file.filename=="":
            return render_template("upload_trial.html",error="No file chosen")
        if not allowed_files(file.filename):
            return render_template("upload_trial.html", error="Unsupported file type")
        if file and allowed_files(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # return redirect(url_for('upload_file', name=filename))
            return  render_template("upload_trial.html",error="success",name=file.filename)
    else:
        return render_template("upload_trial.html")



# <form action="" method="post" enctype="multipart/form-data"  class="form-control" style="background-color:azure;border-radius:15px;justify-content:center">
#               <p class="text danger"> {{error}} </p>
#               <div id="error" class="text-danger"></div>
#               <div id="valid" class="text-success"></div>
#               <img src="../static/upload_trial/{{name}}.jpg" alt="">
#               <input type="file"  name="file" id="upload" style="display:none" accept="multipart/form-data">
#               <button type="button" onclick="document.getElementById('upload').click()" class="btn btn-outline-success m-auto">Upload</button><br><br>
#               <br>
#               <input type="submit" value="Upload" class="btn btn-outline-warning m-auto">
#         </form>












