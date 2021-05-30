from flask import Flask, request
from datetime import datetime, timedelta
import asyncio

app = Flask(__name__)

"""
want to store time, value for each metric
need to purge times that are > WINDOW away

can purge on write -> could slow down write
can purge on read -> could slow down read
can purge in a background process -> how do we trigger this?

can use timeouts / async

generate a key based on timestamp
await WINDOW
delete key


"""

window = timedelta(hours=1)

sum_data = {}


@app.route("/metric/<key>", methods=['POST'])
def store_metric(key):

    value = request.json['value']

    now = datetime.now()

    if key in sum_data:
        sum_data[key].append((now, value))
    else:
        # data race could occur here!
        sum_data[key] = [(now, value)]

    return {}


@app.route("/metric/<key>/sum", methods=['GET'])
def sum(key):
    now = datetime.now()
    if key in sum_data:
        sum = 0
        for (time, value) in sum_data[key]:
            if now - time <= window:
                sum += value
            else: print("Excluding b/c too long ago")
            
        return {"value": sum}
    else:
        return {"value": 0}
