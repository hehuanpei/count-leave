import xlsxwriter

from pyecharts import Bar, Page, Pie
from db import wechatSqlOperations


startTime = input("请输入要查询的开始时间 例（2018-08-27）：")
endTime = input("请输入要查询的结束时间：")
# startTime = "2018-08-27"
# endTime = "2018-08-28"


def getEnterPeopleAndRate():
    """
        [
            {group_name: [(nickname, displayname), ...]},
            {group_name: %}
        ]
    """
    people = wechatSqlOperations.fetchEnterPeople(startTime, endTime)
    rate = wechatSqlOperations.fetchEnterRate(startTime, endTime)

    return [people, rate]


def getOutPeopleAndRate():
    """
        see getEnterPeopleAndRate
    """
    people = wechatSqlOperations.fetchOutPeople(startTime, endTime)
    rate = wechatSqlOperations.fetchOutRate(startTime, endTime)

    return [people, rate]


def writeXlsx(filename, data):
    """
        {
            group_name: [
                (nickname, displayname)...
        ] }
    """
    with xlsxwriter.Workbook(filename) as workbook:
        for x in data:
            worksheet = workbook.add_worksheet(x)
            for i, d in enumerate(data[x]):
                worksheet.write(i, 0, d[0])
                worksheet.write(i, 1, d[1])
        # for i, d in enumerate(data):
            # print(i, d)


def makeChartsAndWriteXlsx():
    a = Page()

    enter = getEnterPeopleAndRate()
    out = getOutPeopleAndRate()
    # print(enter)
    bar = Bar("入职离职信息", "{}-{}".format(startTime, endTime))
    bar.add("入职", [i for i in enter[0].keys()], [len(enter[0][i]) for i in enter[0].keys()])
    bar.add("离职", [i for i in enter[0].keys()], [len(out[0][i]) for i in enter[0].keys()])

    bar2 = Bar("入职离职率", "{}-{}".format(startTime, endTime))
    bar2.add("入职率", [i for i in enter[1].keys()], [enter[1][i] * 100 for i in enter[1].keys()], is_stack=True)
    bar2.add("离职率", [i for i in enter[1].keys()], [out[1][i] * 100 for i in enter[1].keys()], is_stack=True)


    
    a.add_chart(bar)
    a.add_chart(bar2)

    for i in enter[1].keys():
        rate = Pie()
        rate.add("{} 入职离职率饼图".format(i), ["入职", "离职"], 
            [enter[1][i] * 100, out[1][i] * 100], is_label_show=True)
        a.add_chart(rate)

    a.render()


    writeXlsx("{}-{}入职人员.xlsx".format(startTime, endTime), enter[0])
    writeXlsx("{}-{}离职人员.xlsx".format(startTime, endTime), out[0])

if __name__ == '__main__':
    makeChartsAndWriteXlsx()







