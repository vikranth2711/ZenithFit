from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)
app.secret_key = '2004'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin30&'
app.config['MYSQL_DB'] = 'gym_db'


mysql = MySQL(app)
with app.app_context():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_plans (
            plan_id INT AUTO_INCREMENT PRIMARY KEY,
            member_email VARCHAR(255),
            plan_name VARCHAR(255),
            description TEXT,
            FOREIGN KEY (member_email) REFERENCES members(email) ON DELETE CASCADE
        )
    """)
    mysql.connection.commit()

with app.app_context():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_plans (
            plan_id INT AUTO_INCREMENT PRIMARY KEY,
            member_email VARCHAR(255),
            plan_name VARCHAR(255),
            description TEXT,
            FOREIGN KEY (member_email) REFERENCES members(email) ON DELETE CASCADE
        )
    """)
    mysql.connection.commit()

@app.route('/')
def home():
    if 'email' in session:
        return render_template('index.html')
    return redirect('/login')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM members WHERE email = %s AND password = %s', (email, password))
        member = cursor.fetchone()
        if member:
            session['email'] = email
            return redirect('/')
        else:
            return 'Invalid email or password'
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    startDate = request.form['startDate']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO members (name, email, password, startDate) VALUES (%s, %s, %s, %s)', (name, email, password, startDate))
    mysql.connection.commit()
    session['email'] = email
    return redirect('/')

@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM members WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS count FROM payments WHERE member_email = %s', (email,))
        payment_status = 'Active' if cursor.fetchone()['count'] > 0 else 'Inactive'
        cursor.execute('SELECT COUNT(*) AS count FROM attendance WHERE member_email = %s', (email,))
        attendance_count = cursor.fetchone()['count']
        return render_template('profile.html', user=user, payment_status=payment_status, attendance_count=attendance_count)
    return redirect('/login')


@app.route('/exercises', methods=['GET'])
def exercises():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM exercises WHERE member_email = %s', (email,))
        exercises = cursor.fetchall()
        return render_template('exercises.html', exercises=exercises)
    return redirect('/login')

@app.route('/add-exercise', methods=['POST'])
def add_exercise():
    if 'email' in session:
        email = session['email']
        exercise_name = request.form['exercise_name']
        sets = request.form['sets']
        reps = request.form['reps']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO exercises (member_email, exercise_name, sets, reps) VALUES (%s, %s, %s, %s)', (email, exercise_name, sets, reps))
        mysql.connection.commit()
        return redirect('/exercises')
    return redirect('/login')

@app.route('/edit-exercise/<int:exercise_id>', methods=['GET', 'POST'])
def edit_exercise(exercise_id):
    if 'email' in session:
        email = session['email']
        if request.method == 'POST':
            exercise_name = request.form['exercise_name']
            sets = request.form['sets']
            reps = request.form['reps']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE exercises SET exercise_name = %s, sets = %s, reps = %s WHERE exercise_id = %s AND member_email = %s', (exercise_name, sets, reps, exercise_id, email))
            mysql.connection.commit()
            return redirect('/exercises')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM exercises WHERE exercise_id = %s AND member_email = %s', (exercise_id, email))
            exercise = cursor.fetchone()
            return render_template('edit_exercise.html', exercise=exercise)
    return redirect('/login')

@app.route('/delete-exercise/<int:exercise_id>')
def delete_exercise(exercise_id):
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM exercises WHERE exercise_id = %s AND member_email = %s', (exercise_id, email))
        mysql.connection.commit()
        return redirect('/exercises')
    return redirect('/login')

@app.route('/meal-plans', methods=['GET'])
def meal_plans():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM meal_plans WHERE member_email = %s', (email,))
        meal_plans = cursor.fetchall()
        return render_template('meal_plans.html', meal_plans=meal_plans)
    return redirect('/login')

@app.route('/add-meal-plan', methods=['POST'])
def add_meal_plan():
    if 'email' in session:
        email = session['email']
        plan_name = request.form['plan_name']
        description = request.form['description']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO meal_plans (member_email, plan_name, description) VALUES (%s, %s, %s)', (email, plan_name, description))
        mysql.connection.commit()
        return redirect('/meal-plans')
    return redirect('/login')

@app.route('/edit-meal-plan/<int:plan_id>', methods=['GET', 'POST'])
def edit_meal_plan(plan_id):
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM meal_plans WHERE plan_id = %s AND member_email = %s', (plan_id, email))
        meal_plan = cursor.fetchone()
        if meal_plan:
            if request.method == 'POST':
                plan_name = request.form['plan_name']
                description = request.form['description']
                cursor.execute('UPDATE meal_plans SET plan_name = %s, description = %s WHERE plan_id = %s AND member_email = %s', (plan_name, description, plan_id, email))
                mysql.connection.commit()
                return redirect('/meal-plans')
            return render_template('edit_meal_plan.html', meal_plan=meal_plan)
    return redirect('/login')

@app.route('/delete-meal-plan/<int:plan_id>', methods=['GET'])
def delete_meal_plan(plan_id):
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM meal_plans WHERE plan_id = %s AND member_email = %s', (plan_id, email))
        mysql.connection.commit()
        return redirect('/meal-plans')
    return redirect('/login')

@app.route('/workout-plans', methods=['GET'])
def workout_plans():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM workout_plans WHERE member_email = %s', (email,))
        workout_plans = cursor.fetchall()
        return render_template('workout_plans.html', workout_plans=workout_plans)
    return redirect('/login')

@app.route('/add-workout-plan', methods=['POST'])
def add_workout_plan():
    if 'email' in session:
        email = session['email']
        plan_name = request.form['plan_name']
        description = request.form['description']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO workout_plans (member_email, plan_name, description) VALUES (%s, %s, %s)', (email, plan_name, description))
        mysql.connection.commit()
        return redirect('/workout-plans')
    return redirect('/login')

@app.route('/edit-workout-plan/<int:plan_id>', methods=['GET', 'POST'])
def edit_workout_plan(plan_id):
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM workout_plans WHERE plan_id = %s AND member_email = %s', (plan_id, email))
        workout_plan = cursor.fetchone()
        if workout_plan:
            if request.method == 'POST':
                plan_name = request.form['plan_name']
                description = request.form['description']
                cursor.execute('UPDATE workout_plans SET plan_name = %s, description = %s WHERE plan_id = %s AND member_email = %s', (plan_name, description, plan_id, email))
                mysql.connection.commit()
                return redirect('/workout-plans')
            return render_template('edit_workout_plan.html', workout_plan=workout_plan)
    return redirect('/login')

@app.route('/delete-workout-plan/<int:plan_id>', methods=['GET'])
def delete_workout_plan(plan_id):
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM workout_plans WHERE plan_id = %s AND member_email = %s', (plan_id, email))
        mysql.connection.commit()
        return redirect('/workout-plans')
    return redirect('/login')
@app.route('/trainers')
def trainers():
    if 'email' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trainers')
        trainers = cursor.fetchall()
        return render_template('trainers.html', trainers=trainers)
    return redirect('/login')

@app.route('/select-trainer', methods=['POST'])
def select_trainer():
    if 'email' in session:
        trainer_id = request.form['trainer_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM trainers WHERE trainer_id = %s', (trainer_id,))
        selected_trainer = cursor.fetchone()
        session['selected_trainer'] = selected_trainer
        return redirect('/payments')
    return redirect('/login')

@app.route('/payments')
def payments():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM payments WHERE member_email = %s', (email,))
        payments = cursor.fetchall()
        selected_trainer = session.get('selected_trainer')
        return render_template('payments.html', payments=payments, selected_trainer=selected_trainer)
    return redirect('/login')

@app.route('/process-payment', methods=['POST'])
def process_payment():
    if 'email' in session:
        email = session['email']
        membership_type = request.form['membership']
        amount = 0
        if membership_type == 'basic':
            amount = 50
        elif membership_type == 'premium':
            amount = 100
        elif membership_type == 'elite':
            amount = 150

        selected_trainer = session.get('selected_trainer')
        if selected_trainer:
            trainer_fee = float(selected_trainer['fee'])  # Convert trainer_fee to float
            amount += trainer_fee

        payment_date = datetime.now().date()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO payments (member_email, amount, payment_date) VALUES (%s, %s, %s)', (email, amount, payment_date))
        mysql.connection.commit()

        session.pop('selected_trainer', None)

        return redirect('/profile')
    return redirect('/login')

@app.route('/attendance')
def attendance():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM attendance WHERE member_email = %s', (email,))
        attendance_records = cursor.fetchall()
        return render_template('attendance.html', attendance_records=attendance_records)
    return redirect('/login')

@app.route('/record-attendance', methods=['POST'])
def record_attendance():
    if 'email' in session:
        email = session['email']
        class_id = request.form['class_id']
        attendance_date = request.form['attendance_date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO attendance (member_email, class_id, attendance_date) VALUES (%s, %s, %s)', (email, class_id, attendance_date))
        mysql.connection.commit()
        return redirect('/attendance')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('selected_trainer', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
