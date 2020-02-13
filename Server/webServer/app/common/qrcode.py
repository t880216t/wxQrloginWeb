# -*- coding:utf-8 -*-

from io import BytesIO
import qrcode, base64

def set_qrcode(url):
    """
    根据传入的url 生成 二维码对象
    :param url:
    :return:
    """
    qr = qrcode.QRCode(version=5,  # 二维码大小 1～40
                       error_correction=qrcode.constants.ERROR_CORRECT_L,  # 二维码错误纠正功能
                       box_size=5,  # 二维码 每个格子的像素数
                       border=3)     # 二维码与图片边界的距离

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    qrcode_str = b"data:image/png;base64," + base64.b64encode(byte_io.getvalue())
    # return byte_io
    return qrcode_str