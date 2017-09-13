from checks import *
from settings import *
import time
from flask import Flask, jsonify
from multiprocessing import Process, Value

def run_loop():
    while True:
        get_services_health(CHRONOS_URL)
        time.sleep(UPDATE_INTERVAL)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def get_health():
    if send_events.is_alive():
        return jsonify({'status': 'OK'})
    else:
        return jsonify({'status': 'We lost track of the background process'}), 500


if __name__ == "__main__":
    send_events = Process(target=run_loop, args=())
    send_events.start()
    app.run(debug=True, use_reloader=False)
    send_events.join()
