from base_server.diyMySql import *
from base_server.base_send import *

Db = DataBaseHandle("117.50.17.66", "mantis", "6EJt2RYnAYGPaL4z", "bugtracker", 3306)
S=Send_All()




def mantis_project_table_project():
    sql = "select `id` from `mantis_project_table` where `name` = '遗留/线上bug'"
    mantis_project_table_data = Db.selectDb(sql)
    if mantis_project_table_data[0] == 1:
        # print(mantis_project_table_data[1][0][0])
        return mantis_project_table_data[1][0][0]


def mantis_bug_history_table_dates():
    bug_name = ''
    note = ''
    old_value_status = ''
    new_value_status = ''
    bug_id = ''
    username = ''
    project_id = mantis_project_table_project()
    sql = "select `user_id`,`bug_id`,`field_name`,`old_value`,`new_value`,`type` from `mantis_bug_history_table` " \
          " where `date_modified` BETWEEN unix_timestamp(NOW())-360 AND unix_timestamp(NOW()) GROUP BY `id` desc"
    mantis_bug_history_table_date = Db.selectDb(sql)
    if mantis_bug_history_table_date[0] == 1:
        if mantis_bug_history_table_date[1] != '':
            for dates in mantis_bug_history_table_date[1]:
                # print(dates)
                sql = "select realname from mantis_user_table where id =" + str(
                    dates[0])
                mantis_bug_table_date = Db.selectDb(sql)
                if mantis_bug_table_date[0] == 1:
                    username = mantis_bug_table_date[1][0][0]
                sql = "select id,summary from mantis_bug_table where id =" + str(
                    dates[1]) + " and project_id =  " + str(project_id)
                mantis_bug_table_date = Db.selectDb(sql)
                if mantis_bug_table_date[0] == 1:
                    if mantis_bug_table_date[1] != ():
                        bug_name = mantis_bug_table_date[1][0][1]
                        bug_id = mantis_bug_table_date[1][0][0]
                if dates[2] == 'status':
                    sql = "select project_id from mantis_bug_table where id = " + str(dates[1])
                    mantis_bug_table_date = Db.selectDb(sql)
                    if mantis_bug_table_date[1][0][0] == 45:
                        old_value = dates[3]
                        new_value = dates[4]
                        if old_value == '80':
                            old_value_status = '已解决'
                        elif old_value == '30':
                            old_value_status = '重新打开'
                        elif old_value == '40':
                            old_value_status = '已确认'
                        elif old_value == '50':
                            old_value_status = '已分配'
                        elif old_value == '90':
                            old_value_status = '已关闭'
                        if new_value == '80':
                            new_value_status = '已解决'
                        elif new_value == '30':
                            new_value_status = '重新打开'
                        elif new_value == '40':
                            new_value_status = '已确认'
                        elif new_value == '50':
                            new_value_status = '已分配'
                        elif new_value == '90':
                            new_value_status = '已关闭'
                        message_dates = str(username) + ':修改了BUGid为[' + str(bug_id) + ']，BUG名称为{' + str(
                            bug_name) + '},将状态更改为："' + str(new_value_status) + '",原状态为："' + str(old_value_status) + '"'
                        # print(message_dates)
                        S.sending(
                            "https://oapi.dingtalk.com/robot/send?access_token=ae16a69d2290baa9207aec202b50106e2de37f67819cab355129da9ee4ba5947",
                            message_dates)
                if '00' in dates[3][:2]:
                    sql = "select project_id from mantis_bug_table where id = " + str(dates[1])
                    mantis_bug_table_date = Db.selectDb(sql)
                    if mantis_bug_table_date[1][0][0] == 45:
                        sql = "select * from mantis_bugnote_text_table where id = " + dates[3]
                        mantis_bugnote_text_table_date = Db.selectDb(sql)
                        if mantis_bugnote_text_table_date[0] == 1:
                            note = mantis_bugnote_text_table_date[1][0][1]
                        message_dates = str(username) + ':修改了BUGid为[' + str(bug_id) + ']，BUG名称为{' + str(
                            bug_name) + '},添加备注:"' + str(note) + '"'
                        # print(message_dates)
                        S.sending(
                            'https://oapi.dingtalk.com/robot/send?access_token=ae16a69d2290baa9207aec202b50106e2de37f67819cab355129da9ee4ba5947',
                            message_dates)

if __name__ == '__main__':
    mantis_bug_history_table_dates()
