from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors
import re
import uuid
import hashlib
import re
import datetime
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


@app.route("/")
def first():
    return render_template("fresh_tomatoes.html")


ratings = pd.read_csv('dataset/ratings.csv')
movies = pd.read_csv('dataset/movies.csv')
ratings = pd.merge(movies, ratings).drop(['genres', 'timestamp'], axis=1)
user_ratings = ratings.pivot_table(index=['userId'], columns=[
                                   'title'], values='rating')
user_ratings = user_ratings.dropna(thresh=10, axis=1).fillna(0)
item_similarity_df = user_ratings.corr(method='pearson')
item_similarity_df.to_csv('item_similarity_df.csv')


def get_similar_movies(movie_name, user_rating):
    similar_score = item_similarity_df[movie_name]*(float(user_rating)-2.5)
    similar_movies = similar_score.sort_values(ascending=False)
    return similar_movies


def getRecommendations(movie, rating):
    try:
        similar_movies = pd.DataFrame()
        similar_movies = similar_movies.append(
            get_similar_movies(movie, rating), ignore_index=True)
        all_recommend = similar_movies.sum().sort_values(ascending=False)
        m = all_recommend[1:11].to_string()
        m = m.split("\n")
        l = []
        for i in m:
            i = i.split("  ")
            l.append(i[0])
        return l
    except:
        return("NoMatchName ครับ")


@app.route('/login/collab', methods=['POST'])
def recommend():
    features = [str(x) for x in request.form.values()]
    print(features)
    movie_name = str(features[0])
    movie_rating = float(features[1])
    print(movie_name, movie_rating)
    output = getRecommendations(movie_name, movie_rating)
    return render_template('collab.html', recommended_movie=output)


df2 = pd.read_csv('dataset/tmdb.csv')
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
all_titles = [df2['title'][i] for i in range(len(df2['title']))]


def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    reu = df2['revenue'].iloc[movie_indices]
    bud = df2['budget'].iloc[movie_indices]
    vot = df2['vote_average'].iloc[movie_indices]
    run = df2['runtime'].iloc[movie_indices]
    cou = df2['vote_count'].iloc[movie_indices]
    return_df = pd.DataFrame(
        columns=['Title', 'revenue', 'Budget', 'vote_average', 'runtime', 'vote_count'])
    return_df['Title'] = tit
    return_df['revenue'] = reu
    return_df['Budget'] = bud
    return_df['vote_average'] = vot
    return_df['runtime'] = run
    return_df['vote_count'] = cou
    return return_df


app.secret_key = 'your secret key'
app.config['threaded'] = True

# ข้อมูลในการเชื่อม Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '197324685'
app.config['MYSQL_DB'] = 'pythonlogin_advanced'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pachalapol_sod@cmu.ac.th'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['DOMAIN'] = 'http://yourdomain.com'
mysql = MySQL(app)
mail = Mail(app)
account_activation_required = False
csrf_protection = False


@app.route('/login/contentbase', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return(render_template('contentbase.html'))
    if request.method == 'POST':
        m_name = request.form['movie_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            return(render_template('error.html', name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            revenue = []
            budget = []
            vote_average = []
            runtime = []
            vote_count = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                revenue.append(result_final.iloc[i][1])
                budget.append(result_final.iloc[i][2])
                vote_average.append(result_final.iloc[i][3])
                runtime.append(result_final.iloc[i][4])
                vote_count.append(result_final.iloc[i][5])
            return render_template('result.html', movie_names=names, movie_revenue=revenue, movie_budget=budget, movie_vote_average=vote_average, movie_runtime=runtime, movie_vote_count=vote_count, search_name=m_name)


@app.route('/login/result1', methods=['GET', 'POST'])
def main1():
    if request.method == 'GET':
        return(render_template('contentbase.html'))
    if request.method == 'POST':
        m_name = request.form['movie_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            return(render_template('error.html', name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            runtime = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                runtime.append(result_final.iloc[i][4])
            return render_template('result1.html', movie_names=names, movie_runtime=runtime, search_name=m_name)


@app.route('/login/result2', methods=['GET', 'POST'])
def main2():
    if request.method == 'GET':
        return(render_template('contentbase.html'))
    if request.method == 'POST':
        m_name = request.form['movie_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            return(render_template('error.html', name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            vote_average = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                vote_average.append(result_final.iloc[i][3])
            return render_template('result2.html', movie_names=names, movie_vote_average=vote_average, search_name=m_name)


@app.route('/login/result3', methods=['GET', 'POST'])
def main3():
    if request.method == 'GET':
        return(render_template('contentbase.html'))
    if request.method == 'POST':
        m_name = request.form['movie_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            return(render_template('error.html', name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            vote_count = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                vote_count.append(result_final.iloc[i][5])
            return render_template('result3.html', movie_names=names, movie_vote_count=vote_count, search_name=m_name)

# เข้าสู่ระบบ


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # ส่งไปยังหน้า Home เมื่อทำการ login แล้ว
    if loggedin():
        return redirect(url_for('home'))
    # ตรวจสอบเงื่อนไขการเข้าสู่ระบบ
    msg = ''
    # ตรวจ "username" และ "password"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'token' in request.form:
        username = request.form['username']
        password = request.form['password']
        token = request.form['token']
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        # เช็คบัญชีในตารางฐานข้อมูล
        if account:
            if account_activation_required and account['activation_code'] != 'activated' and account['activation_code'] != '':
                return 'Please activate your account to login!'
            if csrf_protection and str(token) != str(session['token']):
                return 'Invalid token!'
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']
        else:
            return 'Username หรือ Password ไม่ถูกต้อง'
    token = uuid.uuid4()
    session['token'] = token
    return render_template('index.html', msg=msg, token=token)

# สมัครสมาชิก


@app.route('/login/register', methods=['GET', 'POST'])
def register():
    if loggedin():
        return redirect(url_for('home'))
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'cpassword' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']
        email = request.form['email']
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        hashed_password = hash.hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            return 'บัญชีนี้มีผู้ใช้แล้ว'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return 'Email address ไม่ถูกต้อง'
        elif not re.match(r'[A-Za-z0-9]+', username):
            return 'Username ต้องประกอบด้วยอักขระและตัวเลขเท่านั้น!'
        elif not username or not password or not cpassword or not email:
            return 'กรุณากรอกแบบฟอร์ม!'
        elif password != cpassword:
            return 'รหัสผ่านไม่ตรงกัน!'
        elif len(username) < 5 or len(username) > 20:
            return 'Username ต้องมีความยาวระหว่าง 5 ถึง 20 ตัวอักขระ!'
        elif len(password) < 5 or len(password) > 20:
            return 'Password ต้องมีความยาวระหว่าง 5 ถึง 20 ตัวอักขระ!'
        elif account_activation_required:
            activation_code = uuid.uuid4()
            cursor.execute('INSERT INTO accounts (username, password, email, activation_code) VALUES (%s, %s, %s, %s)',
                           (username, hashed_password, email, activation_code,))
            mysql.connection.commit()
            email_info = Message('Account Activation Required',
                                 sender=app.config['MAIL_USERNAME'], recipients=[email])
            activate_link = app.config['DOMAIN'] + \
                url_for('activate', email=email, code=str(activation_code))
            email_info.body = render_template(
                'activation-email-template.html', link=activate_link)
            email_info.html = render_template(
                'activation-email-template.html', link=activate_link)
            mail.send(email_info)
            return 'โปรดตรวจสอบอีเมลของคุณเพื่อเปิดใช้งานบัญชี!'
        else:
            cursor.execute('INSERT INTO accounts (username, password, email, activation_code) VALUES (%s, %s, %s, "activated")',(username, hashed_password, email,))
            mysql.connection.commit()
            return 'คุณได้ลงทะเบียนสำเร็จแล้ว!'
    elif request.method == 'POST':
        return 'กรุณากรอกแบบฟอร์ม!'
    return render_template('register.html', msg=msg)


@app.route('/login/activate/<string:email>/<string:code>', methods=['GET'])
def activate(email, code):
    msg = 'Account doesn\'t exist with that email or the activation code is incorrect!'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM accounts WHERE email = %s AND activation_code = %s', (email, code,))
    account = cursor.fetchone()
    if account:
        cursor.execute(
            'UPDATE accounts SET activation_code = "activated" WHERE email = %s AND activation_code = %s', (email, code,))
        mysql.connection.commit()
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        session['role'] = account['role']
        return redirect(url_for('home'))
    return render_template('activate.html', msg=msg)

@app.route('/login')
def goto():
    return render_template('login.html')

@app.route('/login/home')
def home():
    if loggedin():
        return render_template('home.html', username=session['username'], role=session['role'])
    return redirect(url_for('login'))


@app.route('/login/profile')
def profile():
    if loggedin():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account, role=session['role'])
    return redirect(url_for('login'))


@app.route('/login/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if loggedin():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            cursor.execute(
                'SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Email address ไม่ถูกต้อง!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username ต้องประกอบด้วยอักขระและตัวเลขเท่านั้น!'
            elif not username or not email:
                msg = 'กรุณากรอกแบบฟอร์ม!'
            elif session['username'] != username and account:
                msg = 'บัญชีนี้มีผู้ใช้แล้ว!'
            elif len(username) < 5 or len(username) > 20:
                return 'Username ต้องมีความยาวระหว่าง 5 ถึง 20 อักขระ!'
            elif len(password) < 5 or len(password) > 20:
                return 'Password ต้องมีความยาวระหว่าง 5 ถึง 20 อักขระ!'
            else:
                cursor.execute(
                    'SELECT * FROM accounts WHERE id = %s', (session['id'],))
                account = cursor.fetchone()
                current_password = account['password']
                if password:
                    hash = password + app.secret_key
                    hash = hashlib.sha1(hash.encode())
                    current_password = hash.hexdigest()
                cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s WHERE id = %s', (
                    username, current_password, email, session['id'],))
                mysql.connection.commit()
                msg = 'Updated!'
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        return render_template('profile-edit.html', account=account, role=session['role'], msg=msg)
    return redirect(url_for('login'))

@app.route('/login/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
	msg = ''
	if request.method == 'POST' and 'email' in request.form:
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
		account = cursor.fetchone()
		if account:
			# Generate unique ID
			reset_code = uuid.uuid4()
			# Update the reset column in the accounts table to reflect the generated ID
			cursor.execute('UPDATE accounts SET reset = %s WHERE email = %s', (reset_code, email,))
			mysql.connection.commit()
			# Change your_email@gmail.com
			email_info = Message('Password Reset', sender = app.config['MAIL_USERNAME'], recipients = [email])
			# Generate reset password link
			reset_link = app.config['DOMAIN'] + url_for('resetpassword', email = email, code = str(reset_code))
			# change the email body below
			email_info.body = 'โปรดคลิกลิงก์ต่อไปนี้เพื่อรีเซ็ตรหัสผ่านของคุณ: ' + str(reset_link)
			email_info.html = '<p>โปรดคลิกลิงก์ต่อไปนี้เพื่อรีเซ็ตรหัสผ่านของคุณ: <a href="' + str(reset_link) + '">' + str(reset_link) + '</a></p>'
			mail.send(email_info)
			msg = 'ลิงก์รีเซ็ตรหัสผ่านถูกส่งไปยังอีเมลของคุณแล้ว!'
		else:
			msg = 'ไม่มีบัญชีที่ใช้อีเมลนี้!'
	return render_template('forgotpassword.html', msg=msg)

@app.route('/login/resetpassword/<string:email>/<string:code>', methods=['GET', 'POST'])
def resetpassword(email, code):
	msg = ''
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	# Retrieve the account with the email and reset code provided from the GET request
	cursor.execute('SELECT * FROM accounts WHERE email = %s AND reset = %s', (email, code,))
	account = cursor.fetchone()
	# If account exists
	if account:
		# Check if the new password fields were submitted
		if request.method == 'POST' and 'npassword' in request.form and 'cpassword' in request.form:
			npassword = request.form['npassword']
			cpassword = request.form['cpassword']
			# Password fields must match
			if npassword == cpassword and npassword != "":
				# Hash new password
				hash = npassword + app.secret_key
				hash = hashlib.sha1(hash.encode())
				npassword = hash.hexdigest();
				# Update the user's password
				cursor.execute('UPDATE accounts SET password = %s, reset = "" WHERE email = %s', (npassword, email,))
				mysql.connection.commit()
				msg = 'รหัสผ่านของคุณถูกรีเซ็ตแล้ว <a href="' + url_for('login') + '">login</a>!'
			else:
				msg = 'รหัสผ่านต้องตรงกันและต้องไม่ว่างเปล่า!'
		return render_template('resetpassword.html', msg=msg, email=email, code=code)
	return 'อีเมลหรือรหัสไม่ถูกต้อง!'

@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    resp = make_response(redirect(url_for('login')))
    return resp


def loggedin():
    if 'loggedin' in session:
        return True
    return False


# หน้า admin


@app.route('/login/admin/', methods=['GET', 'POST'])
def admin():
    # เช็ค Admin login
    if not admin_loggedin():
        return redirect(url_for('login'))
    msg = ''
    # ดึงข้อมูลบัญชีทั้งหมดจากฐานข้อมูล
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    return render_template('admin/index.html', accounts=accounts)

# เพิ่ม ลบ แก้ไข ข้อมูลสมาชิก

@app.route('/login/admin/account/<int:id>', methods=['GET', 'POST'])
@app.route('/login/admin/account', methods=['GET', 'POST'], defaults={'id': None})
def admin_account(id):
    # เช็ค Admin login อยู่
    if not admin_loggedin():
        return redirect(url_for('login'))
    page = 'Create'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    account = {
        'username': '',
        'password': '',
        'email': '',
        'activation_code': '',
        'rememberme': '',
        'role': 'Member'
    }
    roles = ['Member', 'Admin']
    if id:
        page = 'Edit'
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        account = cursor.fetchone()
        if request.method == 'POST' and 'submit' in request.form:
            # เพิ่มข้อมูลบัญชี
            password = account['password']
            if account['password'] != request.form['password']:
                hash = request.form['password'] + app.secret_key
                hash = hashlib.sha1(hash.encode())
                password = hash.hexdigest()
            cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s, activation_code = %s, rememberme = %s, role = %s WHERE id = %s', (
                request.form['username'], password, request.form['email'], request.form['activation_code'], request.form['rememberme'], request.form['role'], id,))
            mysql.connection.commit()
            return redirect(url_for('admin'))
        if request.method == 'POST' and 'delete' in request.form:
            # ลบข้อมูลบัญชี
            cursor.execute('DELETE FROM accounts WHERE id = %s', (id,))
            mysql.connection.commit()
            return redirect(url_for('admin'))
    if request.method == 'POST' and request.form['submit']:
        # สร้างบัญชีผู้ใช้ใหม่
        hash = request.form['password'] + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        cursor.execute('INSERT INTO accounts (username,password,email,activation_code,rememberme,role) VALUES (%s,%s,%s,%s,%s,%s)', (
            request.form['username'], password, request.form['email'], request.form['activation_code'], request.form['rememberme'], request.form['role'],))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return render_template('admin/account.html', account=account, page=page, roles=roles)

def admin_loggedin():
    if loggedin() and session['role'] == 'Admin':
        return True
    return False


if __name__ == '__main__':
    app.run()
