from src.controller.DataController import DataController
from src.controller.IdentificationController import IdentificationController
import pickle

# data.clean_raw('Tiara_Oktavian')
identification = IdentificationController()

identification.load_data_image()
identification.analyze_task()
data = pickle.load(open('testing_data.pkl', 'rb'))

for i in data:
  print(i)


