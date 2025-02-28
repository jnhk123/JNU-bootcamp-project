import io
import json
import math
from flask import Flask, Response, send_file, request  # request 임포트 추가
from flask_cors import CORS
import matplotlib.pyplot as plt
import parking_provider
import visualization

parking = parking_provider.Parking()

app = Flask(__name__)
CORS(app)

def replace_nan(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    elif isinstance(obj, list):
        return [replace_nan(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: replace_nan(value) for key, value in obj.items()}
    else:
        return obj

# 예시: /data/all 엔드포인트에서 쿼리 파라미터 "gu"를 받아 해당 구의 데이터만 반환
@app.route('/data/all', methods=['GET'])
def get_all():
    gu = request.args.get('gu')  # URL 쿼리 파라미터 예: ?gu=동구
    type = request.args.get('type')  # URL 쿼리 파라미터 예: ?gu=동구

    data = parking.origin.to_dict(orient='records')

    if gu != 'ALL':
        data = [d for d in data if d.get("구") == gu]

    if type != 'ALL':
        data = [d for d in data if d.get("요금정보") == type]

    data = replace_nan(data)
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, mimetype='application/json; charset=utf-8')

@app.route('/data/has_coord', methods=['GET'])
def get_has_coord():

    gu = request.args.get('gu')  # URL 쿼리 파라미터 예: ?gu=동구
    type = request.args.get('type')  # URL 쿼리 파라미터 예: ?gu=동구

    data = parking.has_coord.to_dict(orient='records')

    if gu != 'ALL':
        data = [d for d in data if d.get("구") == gu]

    if type != 'ALL':
        data = [d for d in data if d.get("요금정보") == type]

    data = replace_nan(data)
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, mimetype='application/json; charset=utf-8')

@app.route('/data/non_coord', methods=['GET'])
def get_non_coord():
    gu = request.args.get('gu')  # URL 쿼리 파라미터 예: ?gu=동구
    type = request.args.get('type')  # URL 쿼리 파라미터 예: ?gu=동구

    data = parking.has_coord.to_dict(orient='records')

    if gu != 'ALL':
        data = [d for d in data if d.get("구") == gu]

    if type != 'ALL':
        data = [d for d in data if d.get("요금정보") == type]

    data = replace_nan(data)
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, mimetype='application/json; charset=utf-8')

@app.route('/bar-chart/gu')
def draw_bar_chart():
    df = parking.origin
    fig = visualization.get_group_by_gu_and_draw_bar(df)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/pie-chart/fee')
def draw_pie_chart():
    df = parking.origin
    fig = visualization.get_fee_info_pie_chart(df)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/bar-chart/fee/<string:gu>')
def draw_bar_chart_for_gu(gu):
    df = parking.origin
    fig = visualization.get_fee_by_gu(df, gu)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# @app.route('/charged/parking')
# def get_charged_parking():
#     df = parking.origin
#
#     fig = visualization.get_charged_parking(df)
#     buf = io.BytesIO()
#     fig.savefig(buf, format='png')
#     plt.close(fig)
#     buf.seek(0)
#     return send_file(buf, mimetype='image/png')
#     return None

if __name__ == '__main__':
    app.run(debug=True)


