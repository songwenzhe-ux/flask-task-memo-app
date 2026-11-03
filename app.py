from flask import Flask,request,jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
DATABASE = 'data.db'

#数据库初始化
def get_db():
    conn = sqlite3.connect(DATABASE) #数据库连接对象
    conn.row_factory = sqlite3.Row #查询返回为元组，设置为字典
    return conn

#数据库建表
def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                meaning TEXT NOT NULL,
                is_learned INTEGER DEFAULT 0
            )
        ''')

#查
@app.route('/api/tasks',methods=['GET'])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()#获取游标对象，执行具体sql命令
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall() #获取查到的所有记录结果
    result = [dict(row) for row in rows]
    return jsonify(result) #返回json数据
#增
@app.route('/api/tasks',methods=['POST'])
def add_task():
    data = request.get_json() #接受json数据
    title = data.get('title')
    meaning = data.get('meaning')
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title,meaning) VALUE (?,?)',(title,meaning))
        new_id = cursor.lastrowid
    return jsonify({'id':new_id,'title':title,'meaning':meaning,'is_learned':0}),201

#改
@app.route('/api/tasks/<int:id>',methods=['PUT'])
def update_task(id):
    data = request.get_json()
    is_learned = data.get('is_learned')
    with get_db() as conn:
        conn.execute('UPDATE tasks SET is_learned = ? WHERE id = ?',(is_learned,id))
        return jsonify({'message':'更新しました。','id':id,'is_learned':is_learned})

#删
@app.route('/api/words/<int:id>',methods=['DALETE'])
def delete_word(id):
    with get_db() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?',(id,))
    return jsonify({'message':'削除しました。'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True,port=5000)