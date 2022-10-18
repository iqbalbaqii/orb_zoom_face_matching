from flask import Flask, render_template
import json
import pandas as pd
import statistics
import matplotlib.pyplot as plt
app = Flask(__name__)


@app.route('/')
def read():
    raw = json.load(
        open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/kombinasi.json'))
    nama = "Ridha Ayu Salsabila"
    section = list(filter(
        lambda x: x['kombinasi'] == 'nfeature: {}, hamming_tolerance: {}, k_knn: {}'.format(512, 64, 15), raw))
    label = list(filter(lambda x: x['Name'] == nama, section[0]['data']))

    rekap = []
    for key, data in label[0]['other'][0].items():
        aa = list(map(lambda x: x[key], label[0]['other']))
        rekap.append({
            'key': key,
            'data': aa
        })
    return json.dumps(rekap)

    # "base_path": "kombinasi_1/capture_7",
    # "valid_result": true,
    # "label": "Muhammad Iqbal Baqi",
    # "identification_result": "Muhammad Iqbal Baqi",
    # "keypoint_length": 425,
    # "average_similarity": 0.619,
    # "identification_accuracy": 0.857,
    # "identification_time": 1.783,
    # "average_orb_executiion": 0.004


@app.route('/bb')
def aa():

    # try:
        

    #     pengujian_7 = list(filter(
    #         lambda x: x['kombinasi'] == 'nfeature: 512, hamming_tolerance: 32, k_knn: 7', raw))
    #     temp = []
    #     for row in pengujian_7[0]['data']:
    #         for i,each in enumerate(row['other']):
    #             if i > 4: break
    #             temp.append(each)

    #     get_testing_name = list(map(lambda x: 'test_'+str(x[0]), enumerate(temp))) 
    #     get_just_akurasi = list(map(lambda x: round(x['identification_accuracy'] * 100, 2), temp))

    #     plt.rcParams["figure.figsize"] = (200,300)
    #     plt.plot(get_testing_name, get_just_akurasi, color='blue', marker='o')
    #     plt.title('Grafik Akurasi Data Test Di Pengujian 7')
    #     plt.xlabel('Test')
    #     plt.ylabel('Akurasi')
    #     plt.grid(True)
    #     plt.xticks(rotation=45)
    #     plt.show()
    #     return
    #     # return json.dumps(get_testing_name)
    # except Exception as e:
    #     return str(e)
    raw = json.load(
        open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/kombinasi.json'))
    kombinasis = list(map(lambda x: x['kombinasi'], raw))

    ret = []
    for jkot, kombinasi in enumerate(kombinasis):
        print(kombinasi)
        section = list(filter(lambda x: x['kombinasi'] == kombinasi, raw))[0]
        names = list(map(lambda x: x['Name'], section['data']))

        table = []
        for name in names:
            current = list(filter(lambda x: x['Name'] == name, section['data']))[
                0]['other']
            # 0 = data test
            # 1 = ext time
            # 2 = extrc time
            # 3 = similar
            # 4 = akurasi
            # 5 = label
            # 6 = kesimpulan
            for i, data in enumerate(current):
                if i > 4:
                    print(name)
                    break
                split_name = str(name).split(' ')
                bin_name = list(map(lambda x: x[0], split_name))
                file_name = "{}_{}.png".format(''.join(bin_name), i+1)

                result = "Tidak Diketahui" if float(
                    data['identification_accuracy']) < 0.500 else data['identification_result']
                isvalid = data['valid_result']
                if(result == 'Tidak Diketahui'):
                    isvalid = False
                    if(data['label'] == data['identification_result']):
                        isvalid =True
                table.append([
                    file_name,
                    data['identification_time'],
                    data['average_orb_executiion'],
                    data['average_similarity'],
                    data['identification_accuracy'],
                    result,
                    "Benar" if isvalid else "Salah"

                ])
            pd.DataFrame(table).to_excel(
                kombinasi+".xlsx", header=False, index=False)
            
        
        sumary = []
        _exe_time = list(map(lambda x: float(x[1]), table))
        avg_exe_time = round(statistics.fmean(_exe_time), 3)
        min_exe_time = min(_exe_time)
        max_exe_time = max(_exe_time)

        _orb_time = list(map(lambda x: float(x[2]), table))
        avg_orb_time = round(statistics.fmean(_orb_time), 3)
        min_orb_time = min(_orb_time)
        max_orb_time = max(_orb_time)

        _similarity = list(map(lambda x: float(x[3]), table))
        avg_similarity = round(statistics.fmean(_similarity), 3)
        min_similarity = min(_similarity)
        max_similarity = max(_similarity)

        _akurasi = list(map(lambda x: float(x[4]), table))
        avg_akurasi = round(statistics.fmean(_akurasi), 3)
        min_akurasi = min(_akurasi)
        max_akurasi = max(_akurasi)

        benar = list(filter(lambda x: x[6] == 'Benar', table))

        ret.append({
            'pengujian': "pengujian {}".format(jkot+1),
            'kombinasi': kombinasi,
            'sumary': {

                'execution_time': {
                   'min': min_exe_time,
                   'max': max_exe_time,
                   'average': avg_exe_time,
                   },
                'orb_time': {
                    'min': min_orb_time,
                    'max': max_orb_time,
                    'average': avg_orb_time,
                },

                'identificaation': {
                    'salah': len(table) - len(benar),
                    'benar': len(benar),
                    'persen': round(len(benar) / len(table) * 100, 3),
                }
            },
        })
    return json.dumps(ret)


# app.run(debug=True)
print(aa())
