from flask import Flask, request
from datetime import datetime, timedelta

app = Flask(__name__)
window = timedelta(hours=1)
cached_sums = {}
raw_values = {}


@app.route('/metric/<key>', methods=['POST'])
def store_metric(key):

    if not 'value' in request.json:
        return 'Malformed input', 400

    value = request.json['value']
    now = datetime.now()

    if key in cached_sums:
        cached_sums[key] += value
        raw_values[key].append((now, value))
    else:
        # data race could occur here!
        cached_sums[key] = value
        raw_values[key] = [(now, value)]

    return {}


@app.route('/metric/<key>/sum', methods=['GET'])
def sum(key):
    now = datetime.now()
    if key in cached_sums:
        i = 0
        while i < len(raw_values[key]):
            time, value = raw_values[key][i]
            if now - time > window:
                cached_sums[key] -= value
                i += 1
            else:
                break

        raw_values[key] = raw_values[key][i:]

        return {'value': cached_sums[key]}
    else:
        return {'value': 0}
