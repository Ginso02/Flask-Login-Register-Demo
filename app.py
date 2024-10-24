from flask import Flask, render_template, request, render_template_string, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config  # 导入配置文件

app = Flask(__name__)
# 加载配置
app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/')
def Index_login():  # put application's code here
    return render_template('login.html')

@app.route('/res')
def Index_res():  # put application's code here
    return render_template('res.html')

# 注册路由
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('username')
    pwd = request.form.get('password')

    if not name or not pwd:
        return render_template_string("用户名和密码不能为空，<a href='/'>返回登录</a>"), 400

    # 检查用户名是否已经存在
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (name,))
    user = cur.fetchone()

    if user:
        return render_template_string("用户名已存在，<a href='/'>返回登录</a>"), 400

    # 将新用户添加到数据库
    hashed_pwd = generate_password_hash(pwd)
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (name, hashed_pwd))
    mysql.connection.commit()
    cur.close()

    return render_template_string("注册成功,<a href='/'>返回登录</a>"), 201


# 登录路由
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('username')
    pwd = request.form.get('password')

    if not name or not pwd:
        return render_template_string("用户名和密码不能为空，<a href='/'>返回注册</a>"), 400

        # 检查用户名和密码是否匹配
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (name,))
    user = cur.fetchone()

    if user and check_password_hash(user[2], pwd):  # user[2] 是密码字段
        # 登录成功，重定向到主页
        return redirect(url_for('home'))  # 'home' 是主页的路由函数名
    else:
        return "用户名或密码错误", 401

@app.route('/home')
def home():
    return render_template('index.html')  # 渲染主页模板

if __name__ == '__main__':
    app.run(debug=True)
