from src.controller.DataController import DataController
from src.controller.IdentificationController import IdentificationController
import pickle
import statistics
import json
import pandas as pd
import sys


def old():
    # iden = IdentificationController()
    # iden.load_data_image()
    # iden.analyze_task()

    # sys.exit()

    datas = json.load(
        open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/loc_50.json'))

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
                _exe_time = list(
                    map(lambda x: x['identification_time'], current))
                avg_exe_time = round(statistics.fmean(_exe_time), 3)
                min_exe_time = min(_exe_time)
                max_exe_time = max(_exe_time)

                _orb_time = list(
                    map(lambda x: x['average_orb_executiion'], current))
                avg_orb_time = round(statistics.fmean(_orb_time), 3)
                min_orb_time = min(_orb_time)
                max_orb_time = max(_orb_time)

                _similarity = list(
                    map(lambda x: x['average_similarity'], current))
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
                'name': label,
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
            'combo': data['combo'],
            'data': group
        })

    with open('group.json', 'w', encoding='utf-8') as f:
        json.dump(kelompok, f, ensure_ascii=False, indent=4)
    # testing()


def sift_compare():
    # iden = IdentificationController()
    # iden.load_data_image()
    # with open('siftcompare.json', 'w', encoding='utf-8') as f:
    #     json.dump(iden.compare_with_sift(), f, ensure_ascii=False, indent=2)
    # return
    datas = json.load(
        open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/siftcompare.json'))
    valid_identification = list(
        filter(lambda x: x['valid_result'] is True, datas))
    invalid_identification = list(
        filter(lambda x: x['valid_result'] is False, datas))

    _exe_time = list(map(lambda x: x['identification_time'], datas))
    avg_exe_time = round(statistics.fmean(_exe_time), 3)
    min_exe_time = min(_exe_time)
    max_exe_time = max(_exe_time)

    _orb_time = list(
        map(lambda x: x['average_sift_executiion'], datas))
    avg_orb_time = round(statistics.fmean(_orb_time), 3)
    min_orb_time = min(_orb_time)
    max_orb_time = max(_orb_time)

    _similarity = list(map(lambda x: x['average_similarity'], datas))
    avg_similarity = round(statistics.fmean(_similarity), 3)
    min_similarity = min(_similarity)
    max_similarity = max(_similarity)

    _akurasi = list(
        map(lambda x: x['identification_accuracy'], datas))
    avg_akurasi = round(statistics.fmean(_akurasi), 3)
    min_akurasi = min(_akurasi)
    max_akurasi = max(_akurasi)

    end = {
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
        'akurasi': {
            'salah': len(invalid_identification),
            'benar': len(valid_identification),
            'average': round(len(valid_identification) / (len(valid_identification) + len(invalid_identification)) * 100, 2),

        },
    }

    with open('zresult.json', 'w', encoding='utf-8') as f:
        json.dump(end, f, ensure_ascii=False, indent=4)


def testing():
    raw = json.load(
        open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/group.json'))
    kombinasis = list(map(lambda x: x['kombinasi'], raw))

    ret = []
    for jkot, kombinasi in enumerate(kombinasis):
        print(kombinasi)
        section = list(filter(lambda x: x['kombinasi'] == kombinasi, raw))[0]

        loc = section['combo']['loc']

        names = list(map(lambda x: x['name'], section['data']))

        table = []
        for name in names:
            current = list(filter(lambda x: x['name'] == name, section['data']))[
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
                    data['identification_accuracy']) < loc else data['identification_result']
                isvalid = data['valid_result']
                if(result == 'Tidak Diketahui'):
                    isvalid = False
                    if(data['label'] == data['identification_result']):
                        isvalid = True
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
            'summary': {

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

                'identification': {
                    'salah': len(table) - len(benar),
                    'benar': len(benar),
                    'persen': round(len(benar) / len(table) * 100, 3),
                }
            },
        })

    rekap = []
    for key, row in enumerate(ret):
        temp = []
        temp.append(row['kombinasi'])
        temp.append(key+1)
        for x, summary in row['summary'].items():
            item = list(summary.values())
            temp.append(item[0])
            temp.append(item[1])
            temp.append(item[2])

        rekap.append(temp)

    pd.DataFrame(rekap).to_excel(
        "rekap.xlsx", header=False, index=False)


def revisi():
    raw = json.load(
        open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/kombinasi.json'))

    replicate = []
    for i, row in enumerate(raw):
        data = row['data']
        _exe_time = list(map(lambda x: float(x['identification_time']), data))
        avg_exe_time = round(statistics.fmean(_exe_time), 3)
        min_exe_time = min(_exe_time)
        max_exe_time = max(_exe_time)

        _orb_time = list(
            map(lambda x: float(x['average_orb_executiion']), data))
        avg_orb_time = round(statistics.fmean(_orb_time), 3)
        min_orb_time = min(_orb_time)
        max_orb_time = max(_orb_time)

        _similarity = list(map(lambda x: float(x['average_similarity']), data))
        avg_similarity = round(statistics.fmean(_similarity), 3)
        min_similarity = min(_similarity)
        max_similarity = max(_similarity)

        _akurasi = list(
            map(lambda x: float(x['identification_accuracy']), data))
        avg_akurasi = round(statistics.fmean(_akurasi), 3)
        min_akurasi = min(_akurasi)
        max_akurasi = max(_akurasi)

        benar = list(filter(lambda x: x['valid_result'] == True, data))

        replicate.append({
            "kombinasi": row['kombinasi'],
            "combo": row['combo'],
            "summary": {
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

                'identification': {
                    'salah': len(data) - len(benar),
                    'benar': len(benar),
                    'persen': round(len(benar) / len(data) * 100, 3),
                }
            },
            'data': data
        })

    filter_by_loc = list(
        filter(lambda x: x['combo']['loc'] == 0.50, replicate))

    with open('group_latest.json', 'w', encoding='utf-8') as f:
        json.dump(replicate, f, ensure_ascii=False, indent=4)


def loc_df():
    raw = json.load(
        open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/group_latest.json'))

    nfeature = [512, 1024, 3072]
    hamming = [32, 50, 64]
    k_knn = [7, 15, 30]

    ret = []
    pg = 1
    for f in nfeature:
        for hamm in hamming:
            for k in k_knn:
                print(f, hamm, k)
                per_loc = list(filter(lambda x:
                                      x['combo']['nfeature'] == f and
                                      x['combo']['hamming_tolerance'] == hamm and
                                      x['combo']['k_knn'] == k, raw))
                kombinasi = per_loc[0]['kombinasi']
                for i, row in enumerate(per_loc):
                    del per_loc[i]['data']

                rekap = []
                rekap.append([
                    'Kombinasi',
                    'Threshold',
                    'Salah',
                    'Benar',
                    'Dalam Persen'
                ])
                for key, row in enumerate(per_loc):
                    temp = []
                    temp.append(kombinasi)
                    temp.append(row['combo']['loc'])
                    temp.append(row['summary']['identification']['salah'])
                    temp.append(row['summary']['identification']['benar'])
                    temp.append(row['summary']['identification']['persen'])
                    rekap.append(temp)

                pd.DataFrame(rekap).to_excel(
                    "rekap_loc_pengujian_{}.xlsx".format(pg), header=False, index=False)
                pg = pg+1
                

    # with open('print.json', 'w', encoding='utf-8') as f:
    #     json.dump(per_loc, f, ensure_ascii=False, indent=4)


loc_df()
