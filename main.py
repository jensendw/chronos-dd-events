from checks import *
from settings import *
import time
from flask import Flask, jsonify
from multiprocessing import Process, Value

def run_loop():
    while True:
        if CHRONOS_URL:
            get_chronos_services_health(CHRONOS_URL)
        if MARATHON_URL:
            get_marathon_services_health(MARATHON_URL)


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
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
    send_events.join()
