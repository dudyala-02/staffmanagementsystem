import flask,sqlalchemy
from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

 #initialize flask
app=Flask(__name__)
#database configuration
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:admin123@localhost/staffmanagementsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

#initailize database
db =SQLAlchemy(app)

#define staff model
class staff(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    designation=db.Column(db.String(100),nullable=False)
    dept=db.Column(db.String(100),nullable=False)
    salary=db.Column(db.Float(10,2),nullable=False)

    def __str__(self)->str:
        return super().__str__()


#route to home
@app.route('/')
def home():
    staffData=staff.query.all()
    return render_template('index.html',sData=staffData)

@app.route('/add',methods=['POST'])
def add_staff():
    #add to database
    sname=request.form['name']
    sdeg=request.form['designation']
    sdept=request.form['dept']
    ssalary=request.form['salary']

    #create new staff
    new_staff=staff(name=sname,designation=sdeg,dept=sdept,salary=ssalary)
    db.session.add(new_staff)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_staff(id):
    sData=staff.query.get_or_404(id)
    if request.method=='POST':
        sData.name=request.form['name']
        sData.designation=request.form['designation']
        sData.dept=request.form['dept']
        sData.salary=request.form['salary']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',staff=sData)

@app.route('/delete/<int:id>',methods=['POST'])
def delete_staff(id):
    sData=staff.query.get_or_404(id) 
    db.session.delete(sData)
    db.session.commit()
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)

