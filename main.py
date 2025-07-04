import os

from flask import Flask, render_template, request
from fletcher import DIFF, DiffInput

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def plot():
    # Default values
    default_input = {
        "jmax": 11,
        "nmax": 10,
        "alpha": 0.00001,
        "s": 0.5,
        "timax": 3500.0,
        "timesteps": "0.0,1500.0,3000.0",
    }
    if request.method == "POST":
        jmax = int(request.form["jmax"])
        nmax = int(request.form["nmax"])
        alpha = float(request.form["alpha"])
        s = float(request.form["s"])
        timax = float(request.form["timax"])
        timesteps = [float(x) for x in request.form["timesteps"].split(",")]
    else:
        jmax = default_input["jmax"]
        nmax = default_input["nmax"]
        alpha = default_input["alpha"]
        s = default_input["s"]
        timax = default_input["timax"]
        timesteps = [float(x) for x in default_input["timesteps"].split(",")]

    diff_input = DiffInput(jmax, nmax, alpha, s, timax, timesteps)
    results = DIFF(diff_input)
    return render_template("plots.html", results=results, default_input=default_input)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
