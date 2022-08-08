from flask import Flask
from src.bll.Data import Data
from src.controller.IdentificationController import IdentificationController
import json
import operator
app = Flask(__name__)
data_handler = Data()
controller = IdentificationController()
@app.route('/loadimg')
def load_image():
  data = controller.load_data_image()
  return json.dumps(data)


@app.route('/checkimg')
def checking_image():
  x = 0
  y = 0
  width = 545
  height = 468

  region = x,y,width,height
  controller.load_data_image()
  controller.identification_task(region)
  x = controller.get_result()
  hasil = json.dumps(x)
  return hasil
if __name__ == "__main__":
  app.run(debug=True)
