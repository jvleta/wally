# TODO: create a basic Flask app that just displays Hello World
from flask import Flask, render_template
from fletcher import DIFF, DiffInput

app = Flask(__name__)

@app.route('/')
def hello_world():
    diff_input = DiffInput(jmax=11, nmax=10, alpha=0.1e-4, s=0.5, timax=3500.0, timesteps=[0.0, 1500.0, 3000.0])
    results = DIFF(diff_input)
    return render_template('plots.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)