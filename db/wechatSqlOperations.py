from datetime import datetime

from .sqlManager import *

__dbaddress__ = "db/groups.sql"


def today():
    return datetime.strftime(datetime.today(), "%Y-%m-%d")


def customDate(year, month, day):
    return datetime.strftime(datetime(year=year, month=month, day=day), "%Y-%m-%d")


def createGroups():
    with SqlManager(__dbaddress__) as s:
        # try:
            s.execute('''CREATE TABLE Groups(
             id INTEGER primary key autoincrement,
             nickname TEXT UNIQUE)''')
        # except sqlite3.OperationalError:
            # pass


def insertTheNameOfGroupIntoGroups(groups_nickname: iter):
    # if not exist Groups table then create it.
    createGroups()
    with SqlManager(__dbaddress__) as s:
        for i in groups_nickname:
            # try:
                s.execute('INSERT INTO Groups (nickname) values (?)', (i,))
            # except:
                # pass


def fetchAllGroupName()->list:
    """
        return all saved group nickname
    """
    with SqlManager(__dbaddress__) as s:
        result = s.execute('SELECT * from Groups').fetchall()

    return [i[1] for i in result if i]


def createDetailGroup(groups_nickname: list):
    """
        Create table based on group nickname.
        [group, group, group]
    """
    with SqlManager(__dbaddress__) as s:
        for i in groups_nickname:
            try:
                s.execute('''CREATE TABLE {}(
                    id INTEGER primary key autoincrement,
                    nickname TEXT,
                    displayname TEXT,
                    enterTime DATE,
                    outTime DATE DEFAULT Null
                    );'''.format(i))
            except sqlite3.OperationalError:
                pass


def insertNewMemberIntoGroup(group_nickname, member_detail: list):
    """
        insert memebr into a group
        member_detail:
          [{
            nickname,
            displayname
          }, {}, {}]
    """
    with SqlManager(__dbaddress__) as s:
        for i in member_detail:
            # print('''INSERT INTO {} (nickname, displayname, enterTime) VALUES ("{}", "{}", "{}")'''.format(group_nickname,
            #         i.get('nickname'), i.get('displayname'), today()))
            # print('''INSERT INTO {} (nickname, displayname, enterTime) VALUES ("{}", "{}", "{}")'''.format(group_nickname,
            #         i.get('nickname').replace('"', '\"'), i.get('displayname').replace('"', '\"'), today()))
            s.execute('''INSERT INTO {} (nickname, displayname, enterTime) VALUES (?, ?, ?)'''.format(group_nickname),
                    (i.get('nickname'), i.get('displayname'), today()))


def deleteOldMemberIntoGroup(group_nickname, memebr_detail: iter):
    """
        set outTime to today the condition is displayName and nickname.
        member_detail: [displayname, displayname...]
    """    
    with SqlManager(__dbaddress__) as s:
        for i in memebr_detail:
            s.execute('''UPDATE {} SET outTime="{}" WHERE displayname=?'''.format(group_nickname,
             today()), (i,))


def fetchAllOldMember(groups_nickname:iter)->dict:
    """
        return all saved member
    """
    result = {}
    with SqlManager(__dbaddress__) as s:
        for i in groups_nickname:
            # [(), ()]
            try:
                oldMember = s.execute('''SELECT displayname FROM {}'''.format(i))
                result[i] = oldMember.fetchall()
            except sqlite3.OperationalError:
                createDetailGroup([i])
                return {}

    return result


def fetchEnterPeople(start_time, end_time, groups_nickname=None):
    """
        groups_nickname:
            if None then all groups.

        return Type:
        {group_nickname: [(nickname, displayname)], ....}
    """
    result = {}

    with SqlManager(__dbaddress__) as s:
        if groups_nickname is None:
            # [(nickname), (), ()]
            groups_nickname = s.execute("SELECT nickname FROM Groups").fetchall()

        for i in groups_nickname:
            if i:
                x = s.execute("SELECT nickname, displayname FROM {} WHERE (?) <= enterTime AND enterTime < (?)".format(i[0]), (start_time, end_time))
                
                result[i[0]] = x.fetchall()

    return result


def fetchOutPeople(start_time, end_time, groups_nickname=None):
    """
        see fetchEnterRate.
    """

    result = {}

    with SqlManager(__dbaddress__) as s:
        if groups_nickname is None:
            # [(nickname), (), ()]
            groups_nickname = s.execute("SELECT nickname FROM Groups").fetchall()

        for i in groups_nickname:
            if i:
                x = s.execute("SELECT nickname, displayname FROM {} WHERE (?) <= outTime AND outTime < (?)".format(i[0]), (start_time, end_time))
                result[i[0]] = x.fetchall()

    return result


def fetchEnterRate(start_time, end_time, groups_nickname=None):
    """
        see fetchEnterPeople
        rate:
            比如要计算8月份的入职率：
            统计入职时间 < 8月初的人数 / 统计入职时间 > 8月初的人数 
            select count(\*) from group nickname where enterTime < currentTime
            select count(\*) from group nickname where enterTime > currentTime

        return Type:
          {group_name: %, ...}
    """

    result = {}

    with SqlManager(__dbaddress__) as s:
        if groups_nickname is None:
            # [(nickname), (), ()]
            groups_nickname = s.execute("SELECT nickname FROM Groups").fetchall()

        for i in groups_nickname:
            if i:
                # calcute people count between start_time and end_time
                x = s.execute("SELECT count(*) FROM {} WHERE (?) <= enterTime AND enterTime < (?)".format(i[0]), (start_time, end_time)).fetchall()
                # calcute people count that still live here.

                y = s.execute("SELECT count(*) FROM {} WHERE outTime is NULL OR ? < outTime".format(i[0]), (end_time,)).fetchall()

                # x / y
                result[i[0]] = x[0][0] / y[0][0]
    return result


def fetchOutRate(start_time, end_time, groups_nickname=None):
    """
        see fetchEnterPeople
        rate:
            统计入职时间 < 8月初的人数 / 统计离职时间 > 8月初的人数
            select count(\*) from group nickname where enterTime < currentTime
            select count(\*) from group nickname where outTime > currentTime

        return Type:
          {group_name: %, ...}
    """

    result = {}

    with SqlManager(__dbaddress__) as s:
        if groups_nickname is None:
            # [(nickname), (), ()]
            groups_nickname = s.execute("SELECT nickname FROM Groups").fetchall()

        for i in groups_nickname:
            if i:
                # calcute people count between start_time and end_time
                x = s.execute("SELECT count(*) FROM {} WHERE ? <= outTime AND outTime < ?".format(i[0]), (start_time, end_time)).fetchall()
                # calcute people count that still live here.
                y = s.execute("SELECT count(*) FROM {} WHERE outTime is NULL OR ? < outTime".format(i[0]), (end_time,)).fetchall()


                # x / y
                # x: out people
                # y: still lived people.
                result[i[0]] = x[0][0] / y[0][0]

    return result

