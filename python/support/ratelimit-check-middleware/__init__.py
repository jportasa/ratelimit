from flask import Flask, request, json
import requests

app = Flask(__name__)


@app.route('/api-rate-limit', methods=['POST'])
def api_rate_limit():
    request_data = request.get_json()

    path = request_data['path']
    nameprefix = request_data['nameprefix']
    json_data = {"domain": "support-dashboard",
                 "descriptors":
                     [
                         {"entries":
                             [
                                {"key": "endpoint", "value": path}
                             ]
                         },
                         {"entries":
                             [
                                 {"key": "endpoint", "value": path},
                                 {"key": "user", "value": nameprefix}
                            ]
                         }
                    ]
                 }
    r = requests.get('http://ratelimit:8080/json', json_data)
    if r.status_code == "429":
        error = {
            "message": "error",
            "code": "You are throttling the API",
        }
        return json.dumps(error)
    if r.status_code == "200":
        r = requests.get('http://support-dashboard-api:8000' + path + "?nameprefix=" + nameprefix)
        return json.dumps(r)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
