from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    cases = db.relationship('Case', backref='client', lazy=True)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50))
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clients')
def clients():
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients)

@app.route('/clients/new', methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        client = Client(
            name=request.form['name'],
            email=request.form.get('email'),
            phone=request.form.get('phone')
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template('new_client.html')

@app.route('/cases')
def cases():
    all_cases = Case.query.all()
    return render_template('cases.html', cases=all_cases)

@app.route('/cases/new', methods=['GET', 'POST'])
def new_case():
    clients = Client.query.all()
    if request.method == 'POST':
        case = Case(
            case_number=request.form['case_number'],
            client_id=request.form['client_id'],
            status=request.form.get('status'),
            description=request.form.get('description')
        )
        db.session.add(case)
        db.session.commit()
        return redirect(url_for('cases'))
    return render_template('new_case.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
