'''
Usage:
    MusicCodes.py run
    MusicCodes.py create <number>
    MusicCodes.py add <number>
    MusicCodes.py show
    MusicCodes.py voucher <from> <to>
    MusicCodes.py reset <code>
'''
import hashlib
import sqlite3
import os
from base64 import b64encode
from docopt import docopt
from flask import Flask, render_template, redirect, send_from_directory
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap


FILE_TO_SEND = 'foo.txt'
DB = 'test.db'


app = Flask(__name__)
app.secret_key = os.urandom(24)
Bootstrap(app)


def create():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE CODES
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CODE            TEXT    NOT NULL,
        USED            INT);''')

    for i in range(int(arguments['<number>'])):
        code = b64encode(os.urandom(6)).decode('utf-8')
        print('insert ' + code)
        conn.execute('INSERT INTO CODES (CODE, USED) \
                VALUES (?, ?)', (code, 0))

    conn.commit()
    conn.close()


def show():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM CODES''')
    for i in cur.fetchall():
        print(str(i[0]) + ' | ' + i[1] + ' | ' + str(i[2]))
    conn.close()


def reset():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''UPDATE CODES SET USED = 0 WHERE CODE = ?''',
        (arguments['<code>'], ))
    conn.commit()
    conn.close()


class CodeForm(Form):
    code = TextField('Code', validators=[Required()])


@app.route('/', methods=('GET', 'POST'))
def index():
    form = CodeForm()
    if form.validate_on_submit():
        return redirect('/' + form.code.data)

    return render_template('index.html', form=form)


@app.route('/<voucher_code>')
def code(voucher_code):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM CODES WHERE CODE = ?''',
        (voucher_code, ))
    entry = cur.fetchall()
    if len(entry) > 0:
        if entry[0][2] == 3:
            conn.close()
            error = 'ALL CODES USED'
            return render_template('code.html', error=error)
        else:
            count = entry[0][2] + 1
            cur.execute('''UPDATE CODES SET USED = ? WHERE CODE = ?''', (count,
                voucher_code))
            conn.commit()
            conn.close()
            return send_from_directory('.', FILE_TO_SEND)
    else:
        conn.close()
        error = 'WRONG CODE'
        return render_template('code.html', error=error)


if __name__ == '__main__':
    arguments = docopt(__doc__)

    if arguments['run']:
        app.run(host='0.0.0.0', debug=True)
    elif arguments['create']:
        create()
    elif arguments['show']:
        show()
    elif arguments['reset']:
        reset()
