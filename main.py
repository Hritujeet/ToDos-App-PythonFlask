from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///toDo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(50000), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} -> {self.title}"

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        ttl = request.form['ttle']
        desc = request.form['desc']

        todo = ToDo(title=ttl, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = ToDo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        ttl = request.form['ttle']
        desc = request.form['desc']
        allTodo = ToDo.query.filter_by(sno=sno).first()

        allTodo.title = ttl
        allTodo.desc = desc
        db.session.add(allTodo)
        db.session.commit()
        return redirect("/")

    allTodo = ToDo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    allTodo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
