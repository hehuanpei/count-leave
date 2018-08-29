# edit html.
# 返回发送邮件需要的格式。
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def edit_content(header, content, types='html', encode='utf-8'):
    # 编辑邮件的内容。

    # 编写邮件内容。
    msg = MIMEMultipart()
    # 邮件正文内容。
    msg.attach(MIMEText(content, types, encode))

    # 邮件标题。
    msg['Subject'] = Header(header, encode).encode()

    return msg.as_string()
