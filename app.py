from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from mlProject.pipeline.prediction import PredictionPipeline
 
 
app = Flask(__name__) # initializing a flask app
 
 
def get_quality_label(score):
    """
    Wine quality scores are typically 0-10.
    Classify into Bad / Average / Good based on score.
    """
    try:
        score = float(score)
    except:
        return "Unknown", "unknown"
 
    if score <= 4:
        return "Bad Quality", "bad"
    elif score <= 6:
        return "Average Quality", "average"
    else:
        return "Good Quality", "good"
 
 
@app.route('/', methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")
 
 
@app.route('/train', methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successful!"
 
 
@app.route('/predict', methods=['POST', 'GET'])  # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            # reading the inputs given by the user
            fixed_acidity        = float(request.form['fixed_acidity'])
            volatile_acidity     = float(request.form['volatile_acidity'])
            citric_acid          = float(request.form['citric_acid'])
            residual_sugar       = float(request.form['residual_sugar'])
            chlorides            = float(request.form['chlorides'])
            free_sulfur_dioxide  = float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])
            density              = float(request.form['density'])
            pH                   = float(request.form['pH'])
            sulphates            = float(request.form['sulphates'])
            alcohol              = float(request.form['alcohol'])
 
            data = [fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                    chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
                    density, pH, sulphates, alcohol]
            data = np.array(data).reshape(1, 11)
 
            obj = PredictionPipeline()
            predict = obj.predict(data)
 
            score = float(predict)
            quality_label, quality_class = get_quality_label(score)
 
            return render_template(
                'results.html',
                prediction=round(score, 2),
                quality_label=quality_label,
                quality_class=quality_class
            )
 
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
 
    else:
        return render_template('index.html')
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)