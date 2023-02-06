from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class EmployeeModel(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def __init__(self, id, first_name, last_name, email, gender, salary):
        self.id= id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.salary = salary

@app.route('/')
def Index():
    all_data = EmployeeModel.query.all()
    return render_template('index.html', employee_details=all_data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        salary = request.form.get('salary')

        my_data = EmployeeModel(id, first_name, last_name, email, gender, salary) 
        db.session.add(my_data) #insert into employee (id, first_name, last_name, email, gender, salary) values(1,'abc','xyz','a@gmail.com','others',100000)
        db.session.commit()

        flash ("Congratulations record added to database")
        
        return redirect(url_for('Index'))

@app.route('/update', methods = ['GET','POST'])
def  update():
    if request.method == 'POST':
        my_data = EmployeeModel.query.get(request.form.get('id')) # select * from employee where id=1

        my_data.first_name = request.form.get('first_name')
        my_data.last_name = request.form.get('last_name')
        my_data.email = request.form.get('email')
        my_data.salary = request.form.get('salary')  # update employee set first_name='', last_name='', email='', salary=='' where id =1

        db.session.commit()
        flash ("Congratulations record updated to database")

        return redirect(url_for('Index'))


@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
    my_data = EmployeeModel.query.get(id)
    db.session.delete(my_data)  # delete from employee where id=1
    db.session.commit()
    flash ("Congratulations record deleted from database")

    return redirect(url_for('Index'))


if __name__=='__main__':
    app.run(debug=True)
    