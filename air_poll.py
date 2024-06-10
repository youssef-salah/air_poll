
from flask import Flask, request, jsonify, make_response
import pandas as pd
import numpy as np
from keras.models import load_model


app = Flask(__name__)
air_poll = load_model('best_model.h5')
print(type(air_poll))


@app.route('/air', methods=['POST', 'GET'])
def handle_data():
   try:

      if request.method == 'POST':
         jdata = request.json
         jdata_df = pd.DataFrame([jdata])
         
      elif request.method == 'GET':
         # Get parameters from query string
         params = ["dew", "temp","press"
                   ,"wnd_dir" , "wnd_spd" ,
                     "snow" ,"rain"
                     ]
         jdata = {param : float (request.args.get(param , 0)) for param in params}
         jdata_df = pd.DataFrame([jdata])

      # Call predict on the model, reshape for single sample
      air_pollution_prediction = air_poll.predict(jdata_df)
      air_pollution_prediction = air_pollution_prediction.tolist()

# Create response with CORS headers
      response = make_response(jsonify({'Pollution': air_pollution_prediction[0]}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST'

      return response

   except Exception as e :
      response = make_response(jsonify({'error' : str(e)}), 400)

      return response

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port=3000)
