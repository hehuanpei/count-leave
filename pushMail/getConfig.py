import configparser


def base_cfg(name, encode):
    # 用于CSS读取可能会带上# 所以修改注释前缀。
    cfg = configparser.ConfigParser(comment_prefixes=('&*&', ';'))
    cfg.read_file(open(name, encoding=encode))

    return cfg


def get_mail_server_config(config_name='mailServer.cfg', encode='utf-8'):
    # 读取邮箱服务器设置信息。
    # 包括地址，端口，ssl连接。
    cfg = base_cfg(config_name, encode)
    server_address = cfg.get('mailServer', 'address')
    server_port = cfg.get('mailServer', 'port')
    server_ssl = cfg.getboolean('mailServer', 'ssl')

    return server_address, server_port, server_ssl


def get_rules(config_name='rules.cfg', encode='utf-8'):
    # 获取规则的设定。
    # 包括url, 规则和限制。
    cfg = base_cfg(config_name, encode)

    url = cfg.get('url', 'url')
    rules_limits = cfg.items('rules')

    return url, rules_limits
