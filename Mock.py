import argparse
from flask import Flask, jsonify, request, make_response
import csv
import io


app = Flask(__name__)


def generate_default_result(args):
    result_list = [{"version": 1, "type": args.type, "desc": "每周更新黄赌涉政域名情报，供云南-亚信使用"}]

    if args.version > 1:
        for version in range(2, args.version + 1):
            result_list.append(
                {"version": version, "type": args.type, "desc": "每周更新黄赌涉政域名情报，供云南-亚信使用"})

    default_result = {
        "status": 0,
        "result": result_list,
        "message": None,
    }

    return default_result

# 命令行参数处理
parser = argparse.ArgumentParser(description='Test stub parameters')
parser.add_argument('--version', '-v', type=int, default=1, help='Version number (default: 1)')
parser.add_argument('--type', '-t', type=str, default="25", help='Type value (default: "25")')
parser.add_argument('--domains-file', '-df', type=str, default="domains.txt", help='Domains file path (default: "domains.txt")')
args = parser.parse_args()

# 根据args.version生成默认结果
default_result = generate_default_result(args)

# # 默认结果
# default_result = {
#     "status": 0,
#     "result": [
#         {
#             "version": args.version,
#             "type": args.type,
#             "desc": "每周更新黄赌涉政域名情报，供云南-亚信使用"
#         }
#     ],
#     "message": None,
# }

# 测试桩接口
@app.route('/test/search/cases/reputation', methods=['GET'])
def test_reputation(null=None):
    return jsonify(default_result)

@app.route('/test/resource/data/download', methods=['POST'])
def test_download():
    # 假设domains.txt文件存在于指定路径下
    with open(args.domains_file, 'r') as f:
        # 读取文件并过滤掉空行
        domains = [line.strip() for line in f.readlines() if line.strip()]

    # 创建CSV内容
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data, delimiter='|')
    # 写入列名（根据需要决定是否保留此行）
    # csv_writer.writerow(["Domain"])

    # 将非空域名列表写入CSV内容
    for domain in domains:
        if domain:  # 判断域名是否为空
            csv_writer.writerow([domain,  '2'])

    # 将CSV内容转换为字节串并设置响应头
    csv_data.seek(0)  # 回到文件起始位置
    response = make_response(csv_data.getvalue().encode())
    response.headers['Content-Disposition'] = 'attachment; filename="domain.csv"'
    response.headers['Content-Type'] = 'text/csv'

    return response

if __name__ == '__main__':
    app.run(debug=True, port=9099)