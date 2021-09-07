# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import sklearn
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

app = Flask(__name__) # initializing a flask app

@app.route("/", methods=['GET'])
@cross_origin()

def homepage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()

def index():
    """'Try to read the data inputs given by the user and predict the
            result by using the loaded model(pickle file) and showing the
            result through a web UI """
    if request.method == 'POST':
        try:
            is_type = request.form['type_']
            if is_type == 'L':
                type_ = 0
            elif is_type == 'M':
                type_ = 1
            else:
                type_ = 2
            process_temp_k = float(request.form['process_temp'])

            rotational_speed_rpm = float(request.form['rotational_speed'])

            torque_nm = float(request.form['torque'])

            tool_wear_min = request.form['tool_wear']

            twf = request.form['twf']
            if twf == "0":
                twf = 0
            else:
                twf = 1

            hdf = request.form['hdf']
            if hdf == "0":
                hdf = 0
            else:
                hdf = 1

            pwf = request.form['pwf']
            if pwf == "0":
                pwf = 0
            else:
                pwf = 1

            osf = request.form['osf']
            if osf == "0":
                osf = 0
            else:
                osf = 1

            rnf = request.form['rnf']
            if rnf == "0":
                rnf = 0
            else:
                rnf = 1

            arr = sc.fit_transform([[type_, process_temp_k, rotational_speed_rpm, torque_nm, tool_wear_min, twf, hdf, pwf, osf, rnf]])

            file = "ai4i2020.pickle"

            loaded_model = pickle.load(open(file,'rb'))

            prediction = loaded_model.predict(arr)

            return render_template('results.html', prediction=round(prediction[0],2))

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')

if __name__  == "__main__":
    app.run(debug=True)



