from flask import Flask, render_template, request, redirect
from db_manager import emplyeemanager # Aapki file ka naam, update_employee

app = Flask(__name__)
mgr = emplyeemanager()
mgr.create_table()

@app.route('/')
def index():
    # Saare employees ko fetch karna
    employees = mgr.show_all()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add():
    # Form se data uthana
    eid = request.form['id']
    name = request.form['ename']
    salary = request.form['salary']
    mgr.add_emplyee(eid, name, salary)
    return redirect('/')

@app.route('/delete/<int:eid>')
def delete(eid):
    mgr.delete_employee(eid)
    return redirect('/')

@app.route('/search')
def search():
    name = request.args.get("search_name")
    results = mgr.search_records(name)
    return render_template('index.html',employees = results)
 
@app.route('/update',methods = ['POST'])
def update():
    eid = request.form['id']
    new_salary = request.form['salary']
    mgr.update_employee(eid,new_salary)
    return redirect('/') 

if __name__ == '__main__':
    app.run(debug=True)
