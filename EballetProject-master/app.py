from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import votegraph
import os
import sqlite3
from sqlalchemy import text


app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usersdata.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class userdata(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    roll = db.Column(db.String(15), unique=True, nullable=False)
    batch = db.Column(db.String(8), nullable=False)
    group = db.Column(db.String(8), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    course = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    psw= db.Column(db.String(100), nullable=False)
    can = db.Column(db.String(1), nullable=False, default='F')
    voted = db.Column(db.String(1), nullable=False, default='F')
    scope = db.Column(db.String(20))
    votes = db.Column(db.Integer, nullable=False, default=0)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('success'))
    else:
        return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('email')!=None and "admin0@eballet.in" in session.get('email'):
        # session.pop('email')
        conn = sqlite3.connect('instance/usersdata.db')
        c = conn.cursor()

# Update a column in a table
        old_value = 'Y'
        new_value = 'F'


        if request.method=='POST':
            if 'submit_btn' in request.form:
                course = request.form['course']
                year = request.form['year']
                batch = request.form['batch']
                group = request.form['group']
                nexte = request.form['upel']
                if(course!=" " and year==" " and batch==" " and group==" "):
                    election_type = course
                elif(course==" " and year!=" " and batch==" " and group==" "):
                    election_type = year
                elif(course!=" " and year!=" " and batch!=" " and group==" "):
                    election_type = batch
                elif(course!=" " and year!=" " and batch==" " and group!=" "):
                    election_type = group
                print(election_type)
                # Open the file in write mode
                elections = election_type+","+nexte
                with open('electn.txt', 'w') as file:
                    file.write(elections)

                # user = userdata.query.filter_by(can = 'Y')
                # print(user)
                # Connect to the database
                conn = sqlite3.connect('./instance/usersdata.db')
                c = conn.cursor()

                c.execute("SELECT can FROM userdata")
                rows = c.fetchall()
                batc = election_type.split(" ")[1]
                print(batc)
                # if 'Batch' in election_type:
                for row in rows:
                    c.execute("UPDATE userdata SET can = 'F', voted='F', votes=0, scope = '' ")
                    
                # elif 'Group' in election_type:
                #     for row in rows:
                #         # c.execute(f"UPDATE userdata SET can = 'F', voted='F', votes=0, scope = '' WHERE group = ?", (batc,))
                #         c.execute(f"UPDATE userdata SET can = 'F', voted='F', votes=0, scope = '' WHERE `group` = ?", (batc,))

                    
                # elif 'Year' in election_type:
                #     for row in rows:
                #         c.execute(f"UPDATE userdata SET can = 'F', voted='F', votes=0, scope = '' WHERE `year` = ?", (batc,))
                    
                # elif 'Course' in election_type:
                #     for row in rows:
                #         c.execute(f"UPDATE userdata SET can = 'F', voted='F', votes=0, scope = '' WHERE `course` = ?", (batc,))
                    


                # Commit the changes and close the connection
                conn.commit()
                conn.close()
                print("done")

                # Commit the changes to the database
                db.session.commit()
            elif 'post_results_btn' in request.form:
                result = db.session.execute(text("SELECT name, email, votes FROM userdata ORDER BY votes DESC LIMIT 3;"))
                rows = []
                for row in result:
                    for i in row:
                        if type(i)!=str:
                            i = f"{i}"
                        rows.append(i)
                my_str = ', '.join(rows)
                with open('electn.txt', 'r') as file:
                    # Read the contents of the file
                    election = file.read()
                my_string = election +", "+ my_str

                with open('results.txt', 'w') as file:
                    file.write(my_string)
        return render_template('admin.html')
    else:
        return redirect('login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        year = request.form['year']
        roll = request.form['roll']
        group = request.form['group']
        batch = request.form['batch']
        email = request.form['email']
        password = request.form['password']

        user = userdata(name=name,course=course,year=year,roll=roll,batch=batch,email=email,psw=password,scope=" ", group=group)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful, please log in')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('success'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email=='admin0@eballet.in' and password == '7890':
            session['email'] = email
            return redirect(url_for('admin'))
        user = userdata.query.filter_by(email=email).first()
        if user and password==user.psw:
            
            session['email'] = email
            session['name']=user.name
            session['course'] = user.course
            session['year'] = user.year
            session['roll'] = user.roll
            session['group'] = user.group
            session['batch'] = user.batch
            session['scope'] = user.scope
            session['email'] = user.email

            return redirect(url_for('success'))
    else:
        return render_template('login.html')

@app.route('/applycand', methods=['GET', 'POST'])
def applycand():
    if 'email' in session:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            scope = request.form['scope']
            user = userdata.query.filter_by(email=email).first()
            if user and password==user.psw:
                user.scope = scope
                user.can = 'Y'
                db.session.commit()
            return redirect(url_for('success'))

        return render_template('cand.html', name=session['name'], course=session['course'],year=session['year'],roll=session['roll'],batch=session['batch'], group=session['group'])
    else:
        return redirect(url_for('login'))

@app.route('/success', methods=['GET', 'POST'])
def success():
    names = ["No Candidates have applied yet!"]
    # Open the file in read mode
    fullresults = "Results are Not declared yet! Will be declared soon!"
    nexte = "No Elections Now"
    with open('electn.txt', 'r') as file:
    # Read the contents of the file
        elections = file.read()
        election = elections.split(",")[0]
        nexte = elections.split(",")[1]
    # Print the contents
        print(election)
        print(session.get('batch'))
        print(nexte)
    with open('results.txt', 'r') as file:
    # Read the contents of the file
        results = file.read()
        Election_res = results.split(", ")[0]
        w1_n = results.split(", ")[0]
        w1_id = results.split(", ")[1]
        w1_v = results.split(", ")[2]
        w2_n = results.split(", ")[3]
        w2_id = results.split(", ")[4]
        w2_v = results.split(", ")[5]
        w3_n = results.split(", ")[6]
        w3_id = results.split(", ")[7]
        w3_v = results.split(", ")[9]
        fullresults = [Election_res, w1_n, w1_id, w1_v, w2_n, w2_id, w2_v, w3_n, w3_id, w3_v]
    numpplvoted = 0
    total_count = 0
    part = election.split(" ")[1]
    if 'Batch'==election.split(" ")[0]:
        numpplvoted = userdata.query.filter_by(voted='Y', batch=part).count()
        total_count = userdata.query.filter_by(batch=part).count()
    elif 'Course'==election.split(" ")[0]:
        numpplvoted = userdata.query.filter_by(voted='Y', course=part).count()
        total_count = userdata.query.filter_by(course=part).count()
    elif 'Year'==election.split(" ")[0]:
        numpplvoted = userdata.query.filter_by(voted='Y', year=part).count()
        total_count = userdata.query.filter_by(year=part).count()
    elif 'Group'==election.split(" ")[0]:
        numpplvoted = userdata.query.filter_by(voted='Y', group=part).count()
        total_count = userdata.query.filter_by(group=part).count()

    candidates_applying = userdata.query.filter_by(can='Y', scope=election).all()
    names = [user.name for user in candidates_applying]

    print(numpplvoted, "voted out of ", total_count)
    print("current election", election)
    if 'email' in session and 'name' in session:
        if request.method == 'POST':
            scope=request.form['scope']
            session['scope'] = scope
            if 'Batch'==scope.split(" ")[0]:
                return redirect(url_for('batch'))
            elif 'Course'==scope.split(" ")[0]:
                return redirect(url_for('login'))
            elif 'Year'==scope.split(" ")[0]:
                return redirect(url_for('year'))
            elif 'Group'==scope.split(" ")[0]:
                return redirect(url_for('group'))
        return render_template('success.html', name=session['name'], election=election, 
        course=session['course'],year=session['year'],roll=session['roll'],
        batch=session['batch'], num1=numpplvoted, num2=total_count, nexte = nexte, fullresults=fullresults, cands = names)#, course=session['course'],year=session['year'],roll=session['roll'],batch=session['batch'], numberofpplvoted = pplvoted
    else:
        return redirect(url_for('login'))
@app.route('/batch', methods=['GET', 'POST'])
def batch():
    if 'email' in session:
        scope = session.get('scope')
        print(scope)
        candidates_names = userdata.query.filter_by(scope=scope)
        candidates = [candidates.name for candidates in candidates_names]
        if request.method == 'POST':
            cand = request.form['selected']
            user = userdata.query.filter_by(name=cand).first()
            voter = userdata.query.filter_by(email=session.get('email')).first()
            if voter.voted != 'Y':
                user.votes = user.votes+1
            else:
                print("Already voted in this section!")
            voter.voted = 'Y'
            db.session.commit()
            return redirect(url_for('success'))
        return render_template('batch.html', candidates=candidates)
    else:
        return redirect(url_for('login'))
@app.route('/group', methods=['GET', 'POST'])
def group():
    if 'email' in session:
        scope = session.get('scope')
        print(scope)
        candidates_names = userdata.query.filter_by(scope=scope)
        candidates = [candidates.name for candidates in candidates_names]
        if request.method == 'POST':
            cand = request.form['selected']
            user = userdata.query.filter_by(name=cand).first()
            voter = userdata.query.filter_by(email=session.get('email')).first()
            if voter.voted != 'Y':
                user.votes = user.votes+1
            else:
                print("Already voted in this section!")
            voter.voted = 'Y'
            db.session.commit()
            return redirect(url_for('success'))
        return render_template('group.html', candidates=candidates)
    else:
        return redirect(url_for('login'))
@app.route('/year', methods=['GET', 'POST'])
def year():
    if 'email' in session:
        scope = session.get('scope')
        print(scope)
        candidates_names = userdata.query.filter_by(scope=scope)
        candidates = [candidates.name for candidates in candidates_names]
        if request.method == 'POST':
            cand = request.form['selected']
            user = userdata.query.filter_by(name=cand).first()
            voter = userdata.query.filter_by(email=session.get('email')).first()
            if voter.voted != 'Y':
                user.votes = user.votes+1
            else:
                print("Already voted in this section!")
            voter.voted = 'Y'
            db.session.commit()
            return redirect(url_for('success'))
        return render_template('year.html', candidates=candidates)
    else:
        return redirect(url_for('login'))
@app.route('/course', methods=['GET', 'POST'])
def course():
    if 'email' in session:
        scope = session.get('scope')
        print(scope)
        candidates_names = userdata.query.filter_by(scope=scope)
        candidates = [candidates.name for candidates in candidates_names]
        if request.method == 'POST':
            cand = request.form['selected']
            user = userdata.query.filter_by(name=cand).first()
            voter = userdata.query.filter_by(email=session.get('email')).first()
            if voter.voted != 'Y':
                user.votes = user.votes+1
            else:
                print("Already voted in this section!")
            voter.voted = 'Y'
            db.session.commit()
            return redirect(url_for('success'))
        return render_template('course.html', candidates=candidates)
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/about')
def about():
    if 'email' in session:
        return render_template('about.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
