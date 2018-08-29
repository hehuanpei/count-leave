import time
import logging

import wechat
from db import wechatSqlOperations
from pushMail import push

"""
1. 运行微信。
2. 获取指定的微信群的成员。
3. 与旧的做对比。
4. 更新旧的，同时根据发出邮件（未实现）。
5. 生成月份报表。（未实现）
"""
today = wechatSqlOperations.today

mailServer = input("请输入邮箱服务器：")
mailPort = input("请输入邮箱服务器端口：")
mailSSL = input("请选择是否是SSL传输（1 为是，其他不是）：")

if mailSSL == '1':
    mailSSL = True
else:
    mailSSL = False

mailAddress = input("请输入邮箱地址：")
mailPassword = input("请输入邮箱密码：")


try:
    server = push.get_server(mailServer, mailPort, mailSSL)
    push.login_server(server, mailAddress, mailPassword)
except:
    server = False
    logging.error("邮件服务器连接失败，邮件功能将无法使用。错误信息：", exc_info=True)


def runWechat():
    login = wechat.Wechat()

    return login


def getGroups(user, groups_nickname):
    groups = user.get_groups(groups_nickname)
    print("获取到的群：")
    print(groups.keys())
    # add groups into Groups
    wechatSqlOperations.insertTheNameOfGroupIntoGroups(groups.keys())
    print("若未获取到请检查是否将群存在了联系人目录里...")

    print("正在获取每个群的人员信息...")

    groups_members = getGroupsDetails(user, groups)

    print("正在获取已存储的人员信息...")

    # [(displayname), (displayname)]
    old_groups_members = getOldGroupsDetails(groups)



    print("进行对比...")
    makeCompare(groups, groups_members, old_groups_members)


def getGroupsDetails(user, groups):
    groups_members = {}

    for i in groups:
        
        members_dict = {}
        members = user.get_one_group_members(groups[i])
        
        # {'cyr': {'nickname': 'x', 'displayname': 'cyr'}}
        for x in members:
            if x.get('DisplayName'):
                members_dict[x.get('DisplayName')] = {'nickname': x.get('NickName'), 
                                    'displayname': x.get('DisplayName')}
    
        groups_members[i] = members_dict

    return groups_members


def getOldGroupsDetails(groups:dict):
    return wechatSqlOperations.fetchAllOldMember(groups.keys())


def enterCompany(groups, members):
    # members:
    #      [{
    #        nickname,
    #        displayname
    #      }, {}, {}]
    print("没有备注的不计算入内。")
    wechatSqlOperations.insertNewMemberIntoGroup(groups, members)


def outCompany(groups, members):
    # members
    # [displayname, displayname]

    wechatSqlOperations.deleteOldMemberIntoGroup(groups, members)


def makeCompare(groups, groups_members, old_groups_members):
    for i in groups:
        """
            _n:
            {
                'cyr': {
                            'nickname': 'x',
                            'displayname': 'cyr'
                       }
            }

            _o: [(displayname), (displayname)...]
        """
        _n = groups_members.get(i)
        _o = old_groups_members.get(i)

        new_members = set((_n[x]['displayname'] for x in _n))
        old_members = set((x[0] for x in _o)) if _o else set()

        # 
        enter = new_members - old_members
        out = old_members - new_members

        print("入职：")
        for t in enter:
            print(t)
        

        enterCompany(i, [_n[x] for x in enter])

        
        print("离职：")
        for t in out:
            print(t)

        outCompany(i, out)    

        send_mail("{} 入职人员".format(today()), '\n'.join(enter))

        send_mail("{} 离职人员".format(today()), '\n'.join(out))


def send_mail(title, information):
    if not information:
        return

    if server:
        try:
            push.send_to_mail(server, mailAddress, mailAddress, title, information)
        except:
            try:
                push.login_server(server, mailAddress, mailPassword)
                push.send_to_mail(server, mailAddress, mailAddress, title, information)
            except:
                logging.error("邮件服务器连接失败，邮件功能将无法使用。错误信息：", exc_info=True)


def main():
    user = runWechat()

    groups_nickname = input("输入指定的群名称，多个用英文逗号隔开：")
    groups_nickname = groups_nickname.split(',')
    while 1:
        getGroups(user, groups_nickname)
        time.sleep(3600)


if __name__ == '__main__':
    main()
    # send_mail("test", 'test')
    # pass

