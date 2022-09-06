from flask import Flask, render_template

# flask read views in "templates" folder
# flask read asset in "static" folder


app = Flask(__name__)


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


@app.route('/analyze')
def analyze_page():
    return render_template('/views/analyze.html')


app.run(debug=True)
