from flask import Flask, render_template
from src.controller.ViewController import ViewController
import json
import pickle
import statistics
app = Flask(__name__)
data_handler = ViewController()


@app.route('/')
def index():
    return render_template('/views/dashboard.html')


@app.route('/accordions')
def to_accordions():
    return render_template('/views/accordions.html')


@app.route('/gallery')
def to_gallery():
    return render_template('/views/gallery.html')


@app.route('/formcontrol')
def to_form():
    return render_template('/views/basic_elements.html')


@app.route('/about')
def to_about():
    return render_template('/views/about.html')


@app.route('/analyze/<meeting_id>')
def analyze_page(meeting_id):
    front_image, data = data_handler.front_analyze(meeting_id)
    return render_template('/views/analyze.html', capture=enumerate(front_image), data=data)


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
