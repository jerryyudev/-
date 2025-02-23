import ddddocr

# 初始化 OCR 识别器
ocr = ddddocr.DdddOcr()

# 读取验证码图片
with open("captcha.jpg", "rb") as f:
    img_bytes = f.read()

# 识别验证码
captcha_code = ocr.classification(img_bytes)

print(f"识别的验证码: {captcha_code}")
