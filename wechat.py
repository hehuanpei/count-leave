import itchat

class Wechat:

    def __init__(self):

        self.owner = itchat.auto_login(hotReload=True)
        
        # 自动心跳。
        itchat.run(blockThread=False)


    def get_groups(self, name:list=None) -> dict:
        """
            根据 name 返回找到的群。
            {'nickname': 'username',
            ...}
        """
        group_usernames = {}

        for i in name:
            searched_group = itchat.search_chatrooms(i)
            if searched_group:
                for j in searched_group:
                    group_usernames[j['NickName']] = j['UserName']

        return group_usernames

    def get_one_group_members(self, group_username) -> list:
        """
            根据 group_username 返回相应的群内的人员信息。
            返回相应的群人员详细信息：
            [<ChatroomMember: 
            {'MemberList': <ContactList: []>, 
            'Uin': 0, 
            'UserName': '@bb9423896b429c458ba08ce9d2eeb8928b7ae67f09fe98d62bd0bd67cbb8cf40', 
            'NickName': 'nickname', 
            'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@bb9423896b429c458ba08ce9d2eeb8928b7ae67f09fe98d62bd0bd67cbb8cf40&chatroomid=@bff13ab8d7fe93d62c017e7db97c084f&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 
            'Sex': 2, 'Signature': '咿呀哟喂。。。。。。。', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'KXPSPANCLASSEMOJIEMOJI1F433SPAN', 'PYQuanPin': 'kangxiaopaospanclassemojiemoji1f433span', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 233597, 'Province': '四川', 'City': '资阳', 'Alias': '', 'SnsFlag': 17, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 
            'EncryChatRoomId': '@bff13ab8d7fe93d62c017e7db97c084f', 'IsOwner': 0}>

            就是一个[{}, {}]。
        """

        return itchat.update_chatroom(group_username, detailedMember=True).get('MemberList', [])


# wechat = Wechat()
