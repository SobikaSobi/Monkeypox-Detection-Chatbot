from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
import os
import mysql.connector


from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify



english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch'
                          },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)



app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'




@app.route("/ask", methods=['GET', 'POST'])
def ask():
    message = str(request.form['messageText'])
    bott=''
    bott1 = ''
    sresult1=''

    bot_response = english_bot.get_response(message)

    print(bot_response)


    word = 'appointment'



    if word in message :

        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1medicalchatdb')

        cur1 = conn1.cursor()
        cur1.execute(
            "SELECT  distinct  UserName  from  doctortb")
        data = cur1.fetchall()

        for item in data:

            greet = ' <p class="price">  Hello  Search Result </p> <br>'

            doct = ' <p class="price">  Please Select Your Doctor to this list </p> <br>'

            ss = '<a href="http://127.0.0.1:5000/fullInfo?pid='
            ss1 = item[0] + '">'
            ss2 = item[0]
            ss3='</a> <br>'







            bot_response = ss + ss1+ss2+ss3

            if (bott == ""):
                bott = bot_response
            else:
                bott = bott + bot_response

            print(bott)





        return jsonify({'status': 'OK', 'answer':greet+ doct+bott})

    while True:




        if bot_response.confidence > 0.5:

            bot_response = str(bot_response)
            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

        elif message == ("bye") or message == ("exit"):

            bot_response = 'Hope to see you soon' + '<a href="http://127.0.0.1:5000/UserHome">Exit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

            break



        else:

            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})



            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'

                print(bot_response)
                return jsonify({'status': 'OK', 'answer': bot_response})

@app.route("/chat")
def chat():
    return render_template('chat.html')


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1monkeypoxchatdb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['Password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1monkeypoxchatdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()

            return render_template('AdminHome.html', data=data)
        else:
            flash("UserName or Password Incorrect!")

            return render_template('AdminLogin.html')


@app.route("/Prediction")
def Prediction():
    return render_template('Prediction.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']

        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        Password = request.form['Password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1monkeypoxchatdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' ")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1monkeypoxchatdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into regtb values('','" + name + "','" + age + "','" + mobile + "','" + email + "','" + address + "','" +
                username + "','" + Password + "')")
            conn.commit()
            conn.close()
            return render_template('UserLogin.html')



        else:
            flash('Already Register Username')
            return render_template('NewUser.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['Password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1monkeypoxchatdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        else:
            return render_template('Prediction.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        import tensorflow as tf
        import numpy as np
        import cv2
        from keras.preprocessing import image
        file = request.files['file']
        file.save('static/upload/Test.png')
        org1 = 'static/upload/Test.png'

        img1 = cv2.imread('static/upload/Test.png')

        dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
        # cv2.imshow("Nosie Removal", dst)
        noi = 'static/upload/noi.png'

        cv2.imwrite(noi, dst)

        import warnings
        warnings.filterwarnings('ignore')

        # Load the trained model
        classifierLoad = tf.keras.models.load_model('model.h5')

        # Load and preprocess the test image
        test_image = image.load_img('static/upload/Test.png', target_size=(150, 150))
        test_image = image.img_to_array(test_image)  # Convert to array
        test_image = test_image / 255.0  # Rescale as done during training
        test_image = np.expand_dims(test_image, axis=0)  # Expand dimensions for batch format

        # Make prediction
        result = classifierLoad.predict(test_image)
        print(result)

        # Get the index of the highest probability class
        #ind = np.argmax(result)

        ind = np.argmax(result)

        out = ''
        if ind == 0:
            print("Chickenpox")
            out = "Chickenpox"
            fer = """If you or your child is at high risk of complications, your provider may suggest antiviral medicine to fight the virus, such as acyclovir (Zovirax, Sitavig). This medicine may lessen the symptoms of chickenpox. But they work best when given within 24 hours after the rash first appears."""
        elif ind == 1:
            print("Measles")
            out = "Measles"
            fer = " There is no specific treatment for measles, but there are things you can do to help relieve symptoms and prevent complications: Rest,Drink fluids"
        elif ind == 2:
            print("Monkeypox")
            out = "Monkeypox"
            fer = "There aren't any currently approved antiviral treatments for mpox. If you're very sick, your provider might prescribe antiviral drugs like cidofovir or tecovirimat. These drugs are approved to treat other viral infections (like smallpox), but researchers need to learn more about how well they work for mpox"
        elif ind == 3:
            print("Normal")
            out = "Normal"
            fer = "Nil"

        return render_template('Result.html', result=out, org=org1, noi=noi, fer=fer)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
