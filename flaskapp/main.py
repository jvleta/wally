import os

from flask import Flask, render_template, request, redirect, url_for, session
from wally.fletcher import DIFF, DiffInput

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")


@app.route("/", methods=["GET", "POST"])
def step1():
    default_input = {
        "num_gridpoints": 11,
        "alpha": 0.00001,
        "s": 0.5,
        "max_time": 3500.0,
    }
    if request.method == "POST":
        session["num_gridpoints"] = int(request.form["num_gridpoints"])
        session["alpha"] = float(request.form["alpha"])
        session["s"] = float(request.form["s"])
        session["max_time"] = float(request.form["max_time"])
        return redirect(url_for("step2"))
    return render_template(
        "step1.html", default_input=default_input, session=session
    )


@app.route("/step2", methods=["GET", "POST"])
def step2():
    default_timesteps = "0.0,1500.0,3000.0"
    if request.method == "POST":
        session["output_timesteps"] = request.form["output_timesteps"]
        return redirect(url_for("results"))
    return render_template(
        "step2.html", default_timesteps=default_timesteps, session=session
    )


@app.route("/results")
def results():
    # Gather all data from session
    num_gridpoints = session.get("num_gridpoints", 11)
    alpha = session.get("alpha", 0.00001)
    s = session.get("s", 0.5)
    max_time = session.get("max_time", 3500.0)
    output_timesteps = [
        float(x)
        for x in session.get("output_timesteps", "0.0,1500.0,3000.0").split(",")
    ]
    diff_input = DiffInput(num_gridpoints, alpha, s, max_time, output_timesteps)
    results = DIFF(diff_input)
    return render_template("plots.html", results=results, default_input=session)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
