from flask import Flask, render_template
from src.controller.ViewController import ViewController

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
    return render_template('/views/analyze.html', capture = enumerate(front_image), data=data)


app.run(debug=True)

