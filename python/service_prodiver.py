import io
import json
from flask import Flask, Response, send_file
from flask_cors import CORS  # 추가
import matplotlib.pyplot as plt
import parking_provider
import visualization

parking = parking_provider.Parking()

app = Flask(__name__)
CORS(app)  # 추가: 모든 라우트에 대해 CORS 허용

@app.route('/data/has_coord', methods=['GET'])
def get_has_coord():
    data = parking.has_coord.to_dict(orient='records')
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, mimetype='application/json; charset=utf-8')

@app.route('/data/non_coord', methods=['GET'])
def get_non_coord():
    data = parking.non_coord.to_dict(orient='records')
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
