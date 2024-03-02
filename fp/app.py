from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np


app = Flask(__name__)
m = pickle.load(open('xgboost.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(float(x)) for x in request.form.values()]
    print("intial values -->", int_features)
    pre_final_features = [np.array(int_features)]
    prediction = m.predict(pre_final_features)   
    print('prediction value is ', prediction[0])
    if (prediction[0] == 1):
        output = "Demented"
    elif(prediction[0] == 2):
        output = "NonDemented"
    else:
        output = "Converted"
        

    return render_template('index.html', prediction_text='The person is effected to  {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)