from src.controller.DataController import DataController
from src.controller.IdentificationController import IdentificationController
import pickle
import statistics
import json

# iden = IdentificationController()
# iden.load_data_image()
# iden.analyze_task()
datas = pickle.load(open('kombinasi.pkl', 'rb'))

kelompok = []
for data in datas:
    group = []
    labels = ["Akhlak Kamiswara", "Muhammad Iqbal Baqi", 'Andrea Ayunove Hutami', 'Toni Ismail', "Ridha Ayu Salsabila",
              "Rafiqo Rapitasari", "Arizli Romadhon", "Gege Ardiyansyah", "Fanny Yusuf", "Tiara Oktavian"]
    for label in labels:
        current = list(filter(lambda x: x['label'] == label, data['data']))
        get_valid_status = list(map(lambda x: x['valid_result'], current))
        valid_call = list(filter(lambda x: x == True, get_valid_status))

        try:
            avg_exe_time = round(statistics.fmean(
                list(map(lambda x: x['identification_time'], current))), 3)
            avg_orb_time = round(statistics.fmean(
                list(map(lambda x: x['average_orb_executiion'], current))), 3)

            avg_similarity = round(statistics.fmean(
                list(map(lambda x: x['average_similarity'], current))), 3)
            avg_akurasi = round(statistics.fmean(
                list(map(lambda x: x['identification_accuracy'], current))), 3)
        except Exception as e:
            print(label)
            continue
        group.append({
            'Name': label,
            'valid_identification': "{} / {}".format(str(len(valid_call)), str(len(current))),
            'avg_execution_time': avg_exe_time,
            'avg_orb_time': avg_orb_time,
            'avg_similarity': avg_similarity,
            'avg_akurasi': avg_akurasi,
            'other': current
        })
    kelompok.append({
        'kombinasi': data['kombinasi'],
        'data': group
    })

with open('kombinasi.json', 'w', encoding='utf-8') as f:
    json.dump(kelompok, f, ensure_ascii=False, indent=4)
