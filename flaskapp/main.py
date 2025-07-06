import os

from flask import Flask, render_template, request
from wally.fletcher import DIFF, DiffInput

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def plot():
    # Default values
    default_input = {
        "num_gridpoints": 11,
        "alpha": 0.00001,
        "s": 0.5,
        "max_time": 3500.0,
        "output_timesteps": "0.0,1500.0,3000.0",
    }
    if request.method == "POST":
        num_gridpoints = int(request.form["num_gridpoints"])
        alpha = float(request.form["alpha"])
        s = float(request.form["s"])
        max_time = float(request.form["max_time"])
        output_timesteps = [
            float(x) for x in request.form["output_timesteps"].split(",")
        ]
    else:
        num_gridpoints = default_input["num_gridpoints"]
        alpha = default_input["alpha"]
        s = default_input["s"]
        max_time = default_input["max_time"]
        output_timesteps = [
            float(x) for x in default_input["output_timesteps"].split(",")
        ]

    diff_input = DiffInput(num_gridpoints, alpha, s, max_time, output_timesteps)
    results = DIFF(diff_input)
    return render_template("plots.html", results=results, default_input=default_input)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
