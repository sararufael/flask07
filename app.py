from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    people = Person.query.all()
    return render_template("index.html", people = people)

@app.route('/add')
def add():
    return render_template("form.html", person=None)

@app.route('/show/<int:id>')
def show(id):
    person = Person.query.get(id)
    return render_template("show.html", person = person)


@app.route('/edit/<int:id>')
def edit(id):
    person = Person.query.get(id)
    return render_template("form.html", person=person)

@app.route('/delete/<int:id>')
def delete(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/process', methods=['GET','POST'])
def process():

    id = request.form['id']
    firstname = request.form['first']
    lastname = request.form['last']

    if id:
        # updating the person
        person = Person.query.get(id)
        person.firstname = firstname
        person.lastname = lastname
    else:
        # adding a new person
        person = Person(firstname,lastname)
        db.session.add(person)

    db.session.commit()
    return redirect(url_for('index'))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname


if __name__ == '__main__':
    app.run()