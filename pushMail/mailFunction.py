import smtplib

# 设置邮箱服务器，包括建立连接，登陆服务器，发送邮件及退出服务器。

def start_server(server_address='smtp.qq.com', server_port=465, isSSL=True):
    # 建立连接。
    if isSSL:
        return smtplib.SMTP_SSL(server_address, server_port)

    return smtplib.SMTP(server_address, server_port)


def login_server(server, username, password):
    # 登陆到服务器。

    server.login(username, password)

    return server


def send_mail(Server, From, To, Mail):
    # from 为关键字，故此函数参数用大写开头。

    Server.sendmail(From, To, Mail)


def quit_server(server):
    # 退出服务器。
    server.quit()
