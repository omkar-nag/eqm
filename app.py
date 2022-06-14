import json
from flask import Flask, request, Response, render_template

app = Flask(__name__, static_url_path='')

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/visualise/<metric>')
def airquality(metric):
    f = open('database/data.json')
    data = json.load(f)

    if metric == 'aq':

        ind_data = data['day']['airquality']['industrial']
        res_data = data['day']['airquality']['residential']

        return render_template('graph.html', name='Air Quality Index', y_axis='Air Quality Index (AQI)', res_data=res_data, ind_data=ind_data, id=metric)

    if metric == 'hm':

        ind_data = data['day']['humidity']['industrial']
        res_data = data['day']['humidity']['residential']

        return render_template('graph.html', name='Humidity', y_axis='Humidity (%)', res_data=res_data, ind_data=ind_data, id=metric)

    if metric == 'tm':

        ind_data = data['day']['temperature']['industrial']
        res_data = data['day']['temperature']['residential']

        return render_template('graph.html', name='Temperature', y_axis='Celsius (°C)', res_data=res_data, ind_data=ind_data, id=metric)

    if metric == 'nl':

        res_data = data['day']['noise']['residential']
        ind_data = data['day']['noise']['industrial']

        return render_template('graph.html', name='Noise Level', y_axis='Decibels (dB)', res_data=res_data, ind_data=ind_data, id=metric)

    return render_template("404.html")


@app.route('/fetch')
def fetch():
    f = open('database/data.json')
    data = json.load(f)
    return json.dumps(data['realtime'])


@app.route('/data', methods=['POST'])
def process_json():
    data = json.loads(request.data)
    f = open("database/data.json", "r")
    j = json.load(f)
    f.close()
    # print(data)
    # return Response({'success': 'success'}, status=201)

    if data['realtime']:
        j['realtime'] = data['data']
        print("HIIIIIII")
    else:
        j['day'] = data['day']
    f = open("database/data.json", "w")
    json.dump(j, f)
    f.close()

    return Response({'success': 'success'}, status=201)



@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
