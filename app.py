import os
from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import PredictPipeline, CustomData

application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                age=int(request.form.get('age')),
                sex=int(request.form.get('sex')),
                cp=int(request.form.get('cp')),
                trestbps=int(request.form.get('trestbps')),
                chol=int(request.form.get('chol')),
                fbs=int(request.form.get('fbs')),
                restecg=int(request.form.get('restecg')),
                thalach=int(request.form.get('thalach')),
                exang=int(request.form.get('exang')),
                oldpeak=float(request.form.get('oldpeak')),
                slope=int(request.form.get('slope')),
                ca=int(request.form.get('ca')),
                thal=int(request.form.get('thal'))
            )
            pred_df = data.get_data_as_data_frame()
            print(pred_df)
            print("Before Prediction")

            predict_pipeline = PredictPipeline()
            print("Mid Prediction")
            results = predict_pipeline.predict(pred_df)
            print("after Prediction")
            
            if int(results[0]) == 1:
                label = "Diagnosis Result: The Person has Heart Disease"
                result_class = "result-disease"
            else:
                label = "Diagnosis Result: The Person does not have Heart Disease"
                result_class = "result-healthy"
                
            return render_template('home.html', results=label, result_class=result_class)
        except Exception as e:
            return render_template('home.html', results=f"Error occurred: {str(e)}", result_class="result-error")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
