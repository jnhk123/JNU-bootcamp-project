import io
import json
from flask import Flask, Response, send_file
from flask_cors import CORS  # 추가
import matplotlib.pyplot as plt
import parking_provider
import visualization
import math

parking = parking_provider.Parking()

app = Flask(__name__)
CORS(app)  # 추가: 모든 라우트에 대해 CORS 허용

def replace_nan(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    elif isinstance(obj, list):
        return [replace_nan(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: replace_nan(value) for key, value in obj.items()}
    else:
        return obj

@app.route('/data/has_coord', methods=['GET'])
def get_has_coord():
    data = parking.has_coord.to_dict(orient='records')
    # NaN 값을 None (즉, JSON의 null)로 치환
    data = replace_nan(data)
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, mimetype='application/json; charset=utf-8')

@app.route('/data/non_coord', methods=['GET'])
def get_non_coord():
    data = parking.non_coord.to_dict(orient='records')
    data = replace_nan(data)
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, mimetype='application/json; charset=utf-8')

@app.route('/chart')
def chart():
    fig = visualization.group_by_gu_and_draw_bar(parking.origin)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
