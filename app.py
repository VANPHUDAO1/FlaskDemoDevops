from flask import Flask, render_template, redirect, url_for, request
from models import db, App

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_tables():
    db.create_all()
    if App.query.count() == 0:
        sample_apps = [
            App(name='CRM System', version='v1.2.3', status='Running',
                logs='Build OK. Test OK.', monitor_link='http://monitoring.local/crm'),
            App(name='Inventory System', version='v2.0.1', status='Deploying',
                logs='Build running...', monitor_link='http://monitoring.local/inventory'),
            App(name='Payment Gateway', version='v1.0.0', status='Failed',
                logs='Test failed at step 3.', monitor_link='http://monitoring.local/payment')
        ]
        db.session.add_all(sample_apps)
        db.session.commit()

with app.app_context():
    create_tables()

@app.route('/')
def index():
    apps = App.query.all()
    return render_template('index.html', apps=apps)

@app.route('/delete/<int:id>')
def delete(id):
    app_to_delete = App.query.get_or_404(id)
    db.session.delete(app_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    version = request.form['version']
    status = request.form['status']
    logs = request.form['logs']
    monitor_link = request.form['monitor_link']
    new_app = App(name=name, version=version, status=status,
                  logs=logs, monitor_link=monitor_link)
    db.session.add(new_app)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    app_to_update = App.query.get_or_404(id)
    if request.method == 'POST':
        app_to_update.name = request.form['name']
        app_to_update.version = request.form['version']
        app_to_update.status = request.form['status']
        app_to_update.logs = request.form['logs']
        app_to_update.monitor_link = request.form['monitor_link']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', app=app_to_update)

if __name__ == '__main__':
    app.run(debug=True)
