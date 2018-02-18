from flask import Flask, render_template, request, redirect, url_for
import lab_funcs


app = Flask(__name__)


@app.route('/')
def start():
    return render_template('input.html')


@app.route('/input', methods=["POST", "GET"])
def input():
    if request.method == "POST":
        name = request.form['fname']
        lab_funcs.json_create(str(name))
        lab_funcs.map_b(lab_funcs.get_dict(lab_funcs.json_read_new('data.json', ['screen_name', 'location'])))
        return render_template('Res_Map.html')
    else:
        return render_template('input.html')


if __name__ == "__main__":
    app.run(debug=True)
