# 成绩查询工具
这是一个基于 Python 的成绩查询工具，可以通过学生的姓名和身份证号批量查询成绩，支持通过验证码识别和代理服务器进行网络请求。

功能：
获取当前 IP 地址和地理位置信息（国家、城市）。
自动获取验证码并通过 OCR 识别验证码。
批量查询学生成绩并将结果输出到 CSV 文件。
支持查询失败重试机制，如果查询失败 3 次，会跳过该学生并记录失败信息。
# 目录结构

.

├── captcha_images/        # 存储验证码图片

├── name.txt               # 学生姓名列表（每行一个姓名）

├── id.txt                 # 学生身份证号列表（每行一个身份证号）

├── result.csv             # 查询结果输出的文件

├── query_scores.py        # Python 程序

└── README.md              # 本文件

# 环境要求
确保你已经安装了以下 Python 库：

requests：用于发送 HTTP 请求。

ddddocr：用于验证码 OCR 识别。

csv：用于处理 CSV 文件。

time：用于控制程序等待时间。

可以通过以下命令安装依赖：


pip install requests ddddocr
# 使用步骤
# 1. 准备学生数据
你需要提供两个文件：

name.txt：每行一个学生的姓名。

id.txt：每行一个学生的身份证号码。

注意：name.txt 和 id.txt 文件的行数必须一致，每个学生的姓名和身份证号对应。

# 2. 运行程序
使用以下命令运行程序：


python query_scores.py
# 3. 程序执行流程
获取当前 IP 信息： 程序将首先通过请求 https://qifu-api.baidubce.com/ip/local/geo/v1/district 获取当前的 IP 地址和所在地区的国家与城市，输出到控制台。

等待 2 秒： 在获取完 IP 信息后，程序会等待 2 秒钟，然后开始批量查询学生成绩。

验证码识别： 程序会自动请求验证码图片并使用 ddddocr 进行 OCR 识别。若验证码识别不成功，将会重新获取验证码并尝试重新识别，直到成功识别为止。

查询成绩： 程序会使用学生姓名、身份证号和验证码向指定的查询接口发送请求，获取学生成绩。

结果输出： 查询成功的成绩会被保存到 result.csv 文件中，格式如下：


subject,Chinese,Math,Foreign Language,History,Geography,Political Science,Biology,Chemistry,Physics
110105200801214818,pass,fail,pass,pass,fail,pass,fail,pass,pass

失败的学生： 如果学生查询失败，程序会在控制台输出 查询失败 的学生姓名，并跳过该学生。如果某个学生查询失败 3 次，则会被标记为失败。

# 4. 查询结果
查询结果会以 CSV 格式保存在 result.csv 文件中，每一行记录一个学生的成绩信息。文件内容的示例：


subject,Chinese,Math,Foreign Language,History,Geography,Political Science,Biology,Chemistry,Physics
110105200801214818,pass,fail,pass,pass,fail,pass,fail,pass,pass
110105200801214819,pass,pass,fail,fail,pass,fail,pass,fail,pass
# 5. 输出失败学生
程序在查询完成后，会输出查询失败的学生列表，显示每个查询失败的学生姓名。

# 6. 代理设置
程序支持通过 SOCKS5 代理进行查询。代理设置在代码中已经预先配置为：

socks5://127.0.0.1:10809

无代理版本:xuekao.py

有代理版本:xuekao-proxy.py

如果你需要使用不同的代理，可以修改代码中的 proxies 配置。

# 7. 配置文件
name.txt：每行一个学生的姓名。
id.txt：每行一个学生的身份证号码。
result.csv：程序会将查询结果保存到该文件。
# 示例文件格式
name.txt：


张三
李四
王五
id.txt：


11010119900101001X
11010119900202002X
11010119900303003X
# 可能出现的问题
验证码识别错误： 程序会尝试重新获取验证码并识别，直到识别成功。

查询失败： 如果查询失败 3 次，程序会跳过该学生，并在控制台输出 查询失败 的信息。

IP 地址获取失败： 如果 ip-api.com 请求失败，程序会输出提示信息并继续执行查询。

# 结束语
这个工具可以批量查询学生成绩，并通过验证码自动识别进行查询。如果有任何问题或改进建议，欢迎提问！
