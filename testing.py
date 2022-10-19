from src.controller.DataController import DataController
from src.controller.IdentificationController import IdentificationController
import pickle
import statistics
import json
import sys

# iden = IdentificationController()
# iden.load_data_image()
# iden.analyze_task()

# sys.exit()

datas = pickle.load(open('kombinasi.pkl', 'rb'))

kelompok = []
for data in datas:
    group = []
    labels = ["Akhlak Kamiswara", "Muhammad Iqbal Baqi", 'Andrea Ayunove Hutami', 'Toni Ismail', "Ridha Ayu Salsabila",
              "Rafiqo Rapitasari", "Arizli Romadhon", "Gege Ardiyansyah", "Fanny Yusuf", "Tiara Oktavian", "Tidak Diketahui"]
    for label in labels:
        current = list(filter(lambda x: x['label'] == label, data['data']))
        get_valid_status = list(map(lambda x: x['valid_result'], current))
        valid_call = list(filter(lambda x: x == True, get_valid_status))

        try:
            _exe_time = list(map(lambda x: x['identification_time'], current))
            avg_exe_time = round(statistics.fmean(_exe_time), 3)
            min_exe_time = min(_exe_time)
            max_exe_time = max(_exe_time)

            _orb_time = list(
                map(lambda x: x['average_orb_executiion'], current))
            avg_orb_time = round(statistics.fmean(_orb_time), 3)
            min_orb_time = min(_orb_time)
            max_orb_time = max(_orb_time)

            _similarity = list(map(lambda x: x['average_similarity'], current))
            avg_similarity = round(statistics.fmean(_similarity), 3)
            min_similarity = min(_similarity)
            max_similarity = max(_similarity)

            _akurasi = list(
                map(lambda x: x['identification_accuracy'], current))
            avg_akurasi = round(statistics.fmean(_akurasi), 3)
            min_akurasi = min(_akurasi)
            max_akurasi = max(_akurasi)

        except Exception as e:
            print(label)
            continue
        group.append({
            'Name': label,
            'valid_identification': "{} / {}".format(str(len(valid_call)), str(len(current))),
            'execution_time': {
                'average': avg_exe_time,
                'min': min_exe_time,
                'max': max_exe_time
            },
            'orb_time': {
                'average': avg_orb_time,
                'min': min_orb_time,
                'max': max_orb_time
            },
            'similarity': {
                'average': avg_similarity,
                'min': min_similarity,
                'max': max_similarity
            },
            'akurasi': {
                'average': avg_akurasi,
                'min': min_akurasi,
                'max': max_akurasi
            },
            'other': current
        })
    kelompok.append({
        'kombinasi': data['kombinasi'],
        'data': group
    })

with open('kombinasi.json', 'w', encoding='utf-8') as f:
    json.dump(kelompok, f, ensure_ascii=False, indent=4)
