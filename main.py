from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import parser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tax_payments.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)


def convert_date(date_str):

    try:
        date_obj = parser.parse(date_str)
        # Format the datetime object to 'YYYY-MM-DD'
        return date_obj.strftime("%Y-%m-%d")
    except:
        return "NA"

# Database Model
class TaxPayment(db.Model):
    __tablename__ = 'tax_payment'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)
    # tax_rate = db.Column(db.Float, nullable=False)

def create_database():
    with app.app_context():
        db.create_all()

# Routes
@app.route('/')
def all_payments():
    # payments = TaxPayment.query.all()
    selected_due_date = request.args.get('due_date', '')
    if selected_due_date:
        try:
            due_date_obj = datetime.strptime(selected_due_date, '%m/%d/%Y').date()
            print(due_date_obj, selected_due_date)
            payments = TaxPayment.query.filter_by(due_date=due_date_obj).all()
        except ValueError:
            payments = []
    else:
        payments = TaxPayment.query.all()
    total_amount = sum(float(payment.amount) for payment in payments)
    #
    # total_amount = db.session.query(db.func.sum(TaxPayment.amount)).scalar() or 0
    return render_template('all_payments.html', current_year=datetime.now().year, payments=payments, total_amount=total_amount)

@app.route('/add', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        company = request.form['company']
        amount = float(request.form['amount'])
        payment_date = request.form['payment_date'] or None
        status = request.form['status']
        due_date = request.form['due_date']
        # tax_rate = float(request.form['tax_rate'])

        new_payment = TaxPayment(
            company=company, amount=amount,
            payment_date=convert_date(payment_date),
            status=status, due_date=convert_date(due_date))

        db.session.add(new_payment)
        db.session.commit()
        flash('Payment added successfully!', 'success')
        return redirect(url_for('all_payments'))

    return render_template('add_payment.html', current_year=datetime.now().year)

@app.route("/payments/edit/<int:payment_id>", methods=["GET", "POST"])
def update_payment(payment_id):
    """Edit an existing tax payment."""
    payment = TaxPayment.query.get_or_404(payment_id)

    if request.method == "POST":
        payment.company = request.form["company"]
        payment.amount = request.form["amount"]
        payment.payment_date = request.form["payment_date"] or "NA"
        payment.status = request.form["status"]
        due_date = request.form["due_date"] or "NA"
        payment.due_date = convert_date(due_date)
        db.session.commit()
        return redirect(url_for("all_payments"))

    return render_template("edit_payment.html", payment=payment)


@app.route("/payments/delete/<int:payment_id>", methods=["POST"])
def delete_payment(payment_id):
    payment = TaxPayment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return redirect(url_for("all_payments"))

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
