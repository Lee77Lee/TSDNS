from flask import Flask, jsonify, request, make_response
import csv
import io

app = Flask(__name__)


# 假设我们有一个测试桩接口，当被调用时返回预定义的结果
@app.route('/test/search/cases/reputation', methods=['GET'])
def test_reputation(null=None):
    # 这里是你想要返回的结果
    desired_result = {
        "status": 0,
        "result": [
            {
                "version": 1,
                "type": "1",
                "desc": "每周更新黄赌涉政域名情报，供云南-亚信使用"
            }
        ],
        "message": null,

    }
    return jsonify(desired_result)


# @app.route('/test/resource/data/download', methods=['POST'])
# def test_download():
#     # 获取请求体中的JSON数据
#     # data = request.get_json()  # 或者 use `request.json` (取决于Flask版本)
#
#     # if data and isinstance(data.get('version'), int) and isinstance(data.get('type'), str):
#     desired_result = {
#             "domain": "www.chongcuwoqie.com",
#         }
#     # else:
#     #     desired_result = {
#     #         "status": "error",
#     #         "message": "请求参数格式错误，version 应为整数，type 应为字符串"
#     #     }
#
#     return jsonify(desired_result)

@app.route('/test/resource/data/download', methods=['POST'])
def test_download():
    # 假设domains.txt文件存在于应用的同一目录下
    with open('domains.txt', 'r') as f:
        # 读取文件并过滤掉空行
        domains = [line.strip() for line in f.readlines() if line.strip()]

    # 创建CSV内容
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    # 写入列名（根据需要决定是否保留此行）
    # csv_writer.writerow(["Domain"])

    # 将非空域名列表写入CSV内容
    for domain in domains:
        if domain:  # 判断域名是否为空
            csv_writer.writerow([domain])

    # 将CSV内容转换为字节串并设置响应头
    csv_data.seek(0)  # 回到文件起始位置
    response = make_response(csv_data.getvalue().encode())
    response.headers['Content-Disposition'] = 'attachment; filename="domain.csv"'
    response.headers['Content-Type'] = 'text/csv'

    return response


if __name__ == '__main__':
    app.run(debug=True, port=9099)
