import os

from flask import Flask, request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from flask_login import LoginManager, current_user, login_required

from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.models_db import db, User, Prediction
from src.auth.routes import auth_bp
from src.admin.routes import admin_bp
from src.analytics.aggregations import build_dashboard_data

application = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "artifacts", "app.db")
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
db.init_app(application)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(application)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


application.register_blueprint(auth_bp)
application.register_blueprint(admin_bp)

app= application

## Route for a home page

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()
    dashboard_data = build_dashboard_data(predictions)
    return render_template('dashboard.html', dashboard_data=dashboard_data)

@app.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    pagination = (
        Prediction.query.filter_by(user_id=current_user.id)
        .order_by(Prediction.created_at.desc())
        .paginate(page=page, per_page=10, error_out=False)
    )
    return render_template('history.html', pagination=pagination)

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method =='GET':
        return render_template('home.html')
    else:
        data=CustomData(
                gender=request.form.get('gender'),
                race_ethnicity= request.form.get('race_ethnicity'),
                parent_education= request.form.get('parent_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score')),
        ) 

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        predicted_score = float(results[0])

        saved_to_history = False
        if current_user.is_authenticated:
            prediction = Prediction(
                user_id=current_user.id,
                gender=data.gender,
                race_ethnicity=data.race_ethnicity,
                parental_education=data.parent_education,
                lunch=data.lunch,
                test_preparation_course=data.test_preparation_course,
                reading_score=data.reading_score,
                writing_score=data.writing_score,
                predicted_math_score=predicted_score,
            )
            db.session.add(prediction)
            db.session.commit()
            saved_to_history = True

        return render_template('home.html', results=predicted_score, saved_to_history=saved_to_history)
    
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
       
