from flask import Flask, request, render_template, redirect, url_for, session
import datetime as dt
import pymysql

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "cla051063",
    "db": "abes",
    "charset": "utf8"
}
app = Flask(__name__, static_url_path='/static')


# @app.route('/', methods=['POST', 'GET'])
# def mysql():
#     equipments = getEquipments()
#     borrows = getBorrows()
#     books = getBook()
#     return render_template('home.html', equipment=equipments, borrow=borrows, book=books)


@app.route('/searchequipments', methods=['POST'])
def searchEquipment():
    name = request.form.get("name")
    equipments = searchEquipments(name)
    return render_template('home.html', equipment=equipments)


@app.route('/searchborrows', methods=['POST'])
def searchBorrow():
    name = request.form.get("name")
    borrows = searchBorrows(name)
    return render_template('home.html', borrow=borrows)


def getEquipments():
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        sql = "select * from equipment"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
    return rows


def getBorrows():
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        sql = "select * from borrow"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
    return rows


def getBook():
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        id = session['id']
        sql = "select * from book where userid=%s"
        cursor.execute(sql, id)
        rows = cursor.fetchall()
        cursor.close()
    return rows


def searchEquipments(name):
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        cursor.execute("select * from equipment where name like '%" + name + "%'")
        rows = cursor.fetchall()
        for row in rows:
            print(row[1])
        cursor.close()
        return rows


def searchBorrows(name):
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        cursor.execute("select * from borrow where userid like '%" + name + "%'")
        rows = cursor.fetchall()
        for row in rows:
            print(row[1])
        cursor.close()
        return rows


@app.route('/addbook', methods=['POST'])
def addbook():
    name = request.form.get("name")
    addBook(name)
    books = getBook()
    return render_template('home.html', book=books)


def addBook(name):
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        date = dt.datetime.now().strftime('%F')
        userid = session['id']
        sql = "INSERT INTO book VALUES('%s','%s','%s')" % (userid, name, date)
        sql1 = "UPDATE equipment SET amount=amount-1 WHERE name='%s'" % name
        cursor.execute(sql)
        cursor.execute(sql1)
        conn.commit()  # 提交数据库
        cursor.close()
    books = getBook()
    return render_template('login.html', book=books)


@app.route('/addequipment', methods=['POST'])
def addequipment():
    type = request.form.get("type")
    name = request.form.get("name")
    amount = request.form.get("amount")
    addEquipment(type, name, amount)
    equipments = getEquipments()
    return render_template('home.html', equipment=equipments)


def addEquipment(type, name, amount):
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        sql = "insert into equipment (type, name, amount) VALUES ('" + type + "','" + name + "'," + amount + ")"
        cursor.execute(sql)
        conn.commit()
        cursor.close()


@app.route('/')
def home():
    # borrows = getBorrows()
    # books = getBook()
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']

        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT * FROM user WHERE id=%s AND password=%s"
            cursor.execute(command, (id, password))
            # cursor.execute(command)
            user = cursor.fetchone()
            print(user)
            cursor.close()
        if len(user) > 0:
            session['id'] = id
            print("login")
            books = getBook()
            return render_template("home.html", book=books)
        else:
            return "Error user not found"
    else:
        return render_template("login.html")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        id = request.form['id']
        password = request.form['password']
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            sql = "INSERT INTO user (id, password, job) VALUES (%s,%s,%s);"
            new_data = (id, password, '0')
            cursor.execute(sql, new_data)
            conn.commit()

        session['id'] = request.form['id']
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run('127.0.0.1', 5002, True)
