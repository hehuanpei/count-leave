import time

from .mailFunction import *
from .editContent import *
from .getConfig import *


def get_server(server_address=0, port=0, isSSL=True):
    # 根据给定信息连接到服务器并返回。

    # 若为False则是用默认的server。
    # 默认为smtp.qq.com 465 SSL

    if not server_address and not port:
        server = start_server()
    else:
        server = start_server(server_address, port, isSSL)

    return server


def send_to_mail(server, From, to, title, information):
    # 发送指定内容到邮箱。
    # 可以指定发送的间隔。
    # for i in range(len(msgContent[1])):
    # title, information
    msg = edit_content(title, information)

    send_mail(server, From, to, msg)

        # time.sleep(interval)


if __name__ == '__main__':
    pass
    # server_config = getConfig.get_mail_server_config()
    # server = get_server(*server_config)
    #
    # mailFunction.login_server(server, 'cyrbuzz@foxmail.com', 'yvijpirgqatpbhif')

    # rules = getConfig.get_rules()
    # allText = find_content(*rules)

    # send_to_mail(server, 'cyrbuzz@foxmail.com', to=['b754048538@163.com', '754048538@qq.com'], msgContent='allText')
