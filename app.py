from flask import Flask
import json
import znotherversion as z
app = Flask(__name__)

@app.route('/identificaiton2')
def test():
  data = z.identification_2()
  return json.dumps(data)
if __name__ == "__main__":
  app.run(debug=True)
