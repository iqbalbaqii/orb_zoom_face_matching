from flask import Flask
import json

from src.bll.Data import Data
from src.controller.IdentificationController import IdentificationController


app = Flask(__name__)


@app.route('/wajah')
def test():
    iden = IdentificationController()
    lo = iden.load_data_image()
    return json.dumps(lo)

if __name__ == "__main__":
    app.run(debug=True)
