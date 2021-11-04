from flask import Flask,render_template ,request ,redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #we create app first in this we start making web
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///todo.db" #this specify which data base we are going to use
app.config['SQLALCHEMY_ TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model): #this class specify the various fields in our database
    sno = db.Column(db.Integer, primary_key=True) #for seriol no
    title = db.Column(db.String(200), nullable=False) #for title max200
    desc = db.Column(db.String(500), nullable=False) #for description max 500
    date_created = db.Column(db.DateTime,default=datetime.now) #we keep the exact date of adding the data

    def __repr__(self) -> str: #it print todo objects
        return f"{self.sno} - {self.title}"



@app.route("/", methods=['GET','POST']) #this is for creating content for the web page
def hello_world():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title,desc=desc)#we make an instance of todo
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()

    return render_template("index.html", allTodo=allTodo)

@app.route("/show") #if we pup /product on link then this will show us
def name():
    allTodo = Todo.query.all() #here we print our all todo
    print(allTodo)
    return "saurabh mishra"

@app.route("/update/<int:sno>",methods=['get','POST']) #if we pup /product on link then this will show us
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()

        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first() #here we print our all todo
    
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:sno>") #this function is use for del the sno which we pass
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() #here we filter those todo which we pass on sno
    db.session.delete(todo)
    db.session.commit()

    return redirect("/")

@app.route("/about")    
def about():
    return render_template("about.html")





if __name__ =="__main__": #we use this for runnuing our file
    app.run(debug=True)    