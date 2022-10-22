from flask import Flask, render_template
from src.controller.ViewController import ViewController
import json
import pickle
import statistics
app = Flask(__name__)
data_handler = ViewController()


@app.route('/')
def index():
    return render_template('/views/about.html')


@app.route('/about')
def to_about():
    return render_template('/views/about.html')

@app.route('/student')
def student():
    try:
        student = data_handler.loadstudent()
        return json.dumps(list(student))
    except Exception as e:
        return str(e)

@app.route('/faces/<id>')
def face(id):
    try:
        faces,name = data_handler.loadface(id)
        return render_template('/views/faces.html', data=faces, nama=name)
    except Exception as e:
        return str(e)



@app.route('/analyze/<meeting_id>')
def analyze_page(meeting_id):
    front_image, data = data_handler.front_analyze(meeting_id)
    student = data_handler.loadstudent()

    hasil = list(map(lambda x: x['label'], data))

    table = []
    hadir = 0
    for i, row in enumerate(student):
        kehadiran = row['nama'] in hasil
        if kehadiran:
            hadir = hadir+1
        kemunculan = list(filter(lambda x: x == row['nama'], hasil))
        table.append({
            'no' : i+1,
            'id': row['id'],
            'siswa': row['nama'],
            'kehadiran': 'Hadir' if kehadiran else "Tidak Hadir",
            'kemunculan': str(len(kemunculan))+" kali"
        })

    rekap = {
        'hadir': hadir,
        'total': len(student)
    }
    return render_template('/views/analyze.html', capture=enumerate(front_image), data=data, table=table, rekap=rekap)


@app.route('/testing')
def testing():
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
                'avg_akurasi': avg_akurasi
            })
        kelompok.append({
            'kombinasi': data['kombinasi'],
            'data': group
        })
    
    return json.dumps(kelompok)

app.run(debug=True)
