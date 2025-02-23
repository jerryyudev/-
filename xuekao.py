import os
import requests
import ddddocr
import csv
import time

# 获取当前 IP 地址和地理位置信息
def get_ip_info():
    try:
        response = requests.get("https://qifu-api.baidubce.com/ip/local/geo/v1/district")
        data = response.json()
        if data["code"] != "Success":
            print("无法获取 IP 信息")
            return None
        ip = data.get("ip", "未知")
        country = data.get("data", {}).get("country", "未知")
        city = data.get("data", {}).get("city", "未知")
        return ip, country, city
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 创建文件夹保存验证码图片
if not os.path.exists("captcha_images"):
    os.makedirs("captcha_images")

# 设置请求头，模拟浏览器请求
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.1.126339802.1689387430; _ga_34B604LFFQ=GS1.1.1707802848.5.0.1707802848.60.0.0; Hm_lvt_039f809469476768f6767b8c695863ec=1737620723; JSESSIONID1=kTUx5BXDbnQek2zVP0Y6CybwQAm8qT1-AkKuwqeuLGTHxZtwQBle!-477624045",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15 Edg/131.0.0.0",
}

# 映射学科字段
subject_map = {
    "Chinese": "yw",
    "Math": "sx",
    "Foreign Language": "wy",
    "History": "ls",
    "Geography": "dl",
    "Political Science": "sxzz",
    "Biology": "sw",
    "Chemistry": "hx",
    "Physics": "wl",
}

# 学科列表
subjects = list(subject_map.keys())

# 准备将结果写入 CSV 文件
with open("result.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["subject"] + subjects
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 写入标题行

    failed_students = []  # 用来记录查询失败的学生

    # 获取 IP 和位置
    ip_info = get_ip_info()
    if ip_info:
        ip, country, city = ip_info
        print(f"当前 IP 地址: {ip}")
        print(f"所在国家: {country}")
        print(f"所在城市: {city}")
    else:
        print("无法获取 IP 信息，继续执行查询...")

    # 等待 2 秒后开始批量查询
    print("\n等待 2 秒后开始查询...\n")
    time.sleep(2)

    # 读取 name.txt 和 id.txt，逐行读取每个学生信息
    with open("name.txt", "r", encoding="utf-8") as name_file, open("id.txt", "r", encoding="utf-8") as id_file:
        names = name_file.readlines()
        ids = id_file.readlines()

        # 确保 name.txt 和 id.txt 文件行数一致
        if len(names) != len(ids):
            print("错误：name.txt 和 id.txt 文件行数不匹配。")
            exit()

        # 遍历每个学生，查询成绩
        for name, report_no in zip(names, ids):
            name = name.strip()
            report_no = report_no.strip()

            retry_count = 0  # 初始化重试次数

            while retry_count < 3:
                # 重新获取验证码并识别，直到识别到四位数字
                while True:
                    # 获取验证码图片
                    captcha_url = "https://query.bjeea.cn/captcha.jpg"
                    response = requests.get(captcha_url, headers=headers)
                    response.raise_for_status()  # 如果请求失败，抛出异常

                    # 保存验证码图片到本地
                    captcha_path = "captcha_images/captcha.jpg"
                    with open(captcha_path, "wb") as f:
                        f.write(response.content)

                    # 使用 ddddocr 识别验证码
                    ocr = ddddocr.DdddOcr()
                    with open(captcha_path, "rb") as f:
                        img_bytes = f.read()

                    captcha = ocr.classification(img_bytes)  # 直接识别验证码图片
                    print(f"识别的验证码: {captcha}")

                    # 检查验证码是否为四位数字
                    if captcha.isdigit() and len(captcha) == 4:
                        break  # 如果验证码正确，退出循环
                    else:
                        print("验证码识别错误，正在重新获取验证码...")

                # 构建请求数据
                data = {
                    "modeId": "136",
                    "examId": "4921",
                    "name": name,
                    "reportNo": report_no,
                    "captcha": captcha
                }

                # 查询成绩
                query_url = "https://query.bjeea.cn/queryService/rest/score/136"
                response = requests.post(query_url, data=data, headers=headers)

                # 解析返回的数据
                try:
                    response_json = response.json()
                    score_data = response_json.get("heGeKaoList", [])

                    if not score_data:
                        print(f"没有找到 {name} 的成绩数据，请检查请求是否成功。")
                        retry_count += 1  # 如果查询失败，重试次数加1
                        if retry_count >= 3:
                            failed_students.append(name)  # 记录查询失败的学生
                            print(f"{name} 查询失败，跳过此学生。")
                        continue  # 如果没有成绩，跳过当前学生

                    # 获取每个学科的合格情况
                    subject_status = {}
                    for subject, key in subject_map.items():
                        subject_status[subject] = "pass" if score_data[0].get(key) == "合格" else "fail"

                    # 写入查询结果到 CSV 文件
                    writer.writerow({"subject": report_no, **subject_status})

                    break  # 如果查询成功，跳出重试循环

                except Exception as e:
                    print(f"解析返回数据时出错: {e}")
                    retry_count += 1  # 如果发生错误，重试次数加1
                    if retry_count >= 3:
                        failed_students.append(name)  # 记录查询失败的学生
                        print(f"{name} 查询失败，跳过此学生。")

    # 在所有查询完成后输出查询失败的学生
    if failed_students:
        print("\n查询失败的学生：")
        for student in failed_students:
            print(f"{student} 查询失败")
