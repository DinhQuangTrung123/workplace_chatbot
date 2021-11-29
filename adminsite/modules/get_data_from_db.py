from ..utils.postgresql import PostgresQL
from ..utils.WorkplaceApi import WorkPlaceAPI
from ..utils.logger import Logger


class GetDataPostgresql(object):
    def __init__(self):
        self.logger = Logger().logtoFile()
        self.rsp = {
            "status": False,
            "msg" : "Failed",
            "dt" : []
        }

    def get_id_user_from_group_name(self, data):
        sql = f"""select uc.username , uc.user_id, uc.thread_id, gc.group_name from user_campaign uc
left join user_group_campaign_mapping ugcm  on uc.user_id  = ugcm.user_id
left join group_campaign gc on gc.group_id = ugcm.group_id
where gc.group_name  = '{data}'"""
        print(sql)
        result = PostgresQL().select_query(sql=sql)
        return result

    def get_all_campaign_user(self):
        self.logger.info("get_all_campaign_user  data")
        result = None
        try:
            sql = f"""select uc.username , uc.user_id, uc.thread_id, STRING_AGG(gc.group_name, ', ') group_name, uc.email from user_campaign uc
        left join user_group_campaign_mapping ugcm  on uc.user_id  = ugcm.user_id
        left join group_campaign gc on gc.group_id = ugcm.group_id
        group by uc.user_id"""
            result = PostgresQL().select_query(sql=sql)
        except Exception as err:
            self.logger.error(f"[GetDataPostgresql][get_all_campaign_user]: %s" %err, exc_info=True)
        finally:
            return result
        
    def get_all_campaign_group(self):
        result = None
        try:
#             sql = f"""SELECT gc.group_id ,gc.group_name, 
# to_char(COALESCE(gc.modified_at, gc.created_at), 'YYYY-MM-DD HH24:MM:SS') modified_at, 
# COALESCE(gc.modified_by, gc.created_by) modified_by, 
# STRING_AGG(uc.user_id||';'||uc.username, ', ') list_user 
# from group_campaign gc
# left join user_group_campaign_mapping ugcm  on gc.group_id  = ugcm.group_id 
# left join user_campaign uc on uc.user_id = ugcm.user_id
# group by gc.group_id"""
            sql = f"""SELECT gc.group_id ,gc.group_name, 
STRING_AGG(uc.user_id||';'||uc.username, ', ') list_user 
from group_campaign gc
left join user_group_campaign_mapping ugcm  on gc.group_id  = ugcm.group_id 
left join user_campaign uc on uc.user_id = ugcm.user_id
group by gc.group_id"""
            result = PostgresQL().select_query(sql=sql)
        except Exception as err:
            self.logger.error(f"[GetDataPostgresql][get_all_campaign_user]: %s" %err, exc_info=True)
        finally:
            return result

    def get_all_data_group_campaign(self):
        pass

    def add_group_campaign(self, data):
        self.logger.info(f"[GetDataPostgresql][add_group_campaign]: {data}")
        try:
            if data:
                sql_get_id_group = f"""SELECT group_id FROM group_campaign where group_name = '{data.get("groupname")}'"""
                result_select = PostgresQL().select_query(sql=sql_get_id_group)
                if result_select == []:
                    sql_insert = f"""INSERT INTO group_campaign (group_name) VALUES ('{data.get("groupname")}')"""
                    result = PostgresQL().excute_query(sql=sql_insert)
                    if result:
                        sql_get_id_group = f"""SELECT group_id FROM group_campaign where group_name = '{data.get("groupname")}'"""
                        result_select = PostgresQL().select_query(sql=sql_get_id_group)
                        group_id = result_select[0].get("group_id")
                        sql_insert_mapping = "INSERT INTO user_group_campaign_mapping( group_id, user_id) VALUES( %(group_id)s, %(user_id)s)"
                        dict_user = [{'group_id': group_id,  "user_id": i} for i in data.get('user_id')]
                        result_insert_mapping = PostgresQL().excute_query(sql=sql_insert_mapping, data=dict_user)
                        return result_insert_mapping
                return False
        except Exception as err:
            self.logger.error(f"[GetDataPostgresql][add_group]: %s", exc_info=True)

    
    def edit_group_campaign(self, data):
        try:
            if data:
                # INSERT INTO user_campaign(user_id, username) VALUES (%(id)s, %(name)s)
                sql_delete = "DELETE FROM user_group_campaign_mapping WHERE group_id = %(group_id)s"
                result = PostgresQL().excute_query(sql=sql_delete, data = {"group_id" : data.get("id")})
                if result:
                    sql_insert_mapping = "INSERT INTO user_group_campaign_mapping( group_id, user_id) VALUES( %(group_id)s, %(user_id)s)"
                    for i in data.get("user_id"):
                        dict_user = [{'group_id': data.get("id"),  "user_id": i} for i in data.get('user_id')]
                    result_insert_mapping = PostgresQL().excute_query(sql=sql_insert_mapping, data=dict_user)
        except Exception as err:
            self.logger.error(f"[GetDataPostgresql][edit_group_campaign]: %s", exc_info=True)
        else:
            if result_insert_mapping:
                return result_insert_mapping
            
    def delete_group_campaign(self, data):
        try:
            if data:
                data = {"group_id" : data.get("id")}
                sql_delete = "DELETE FROM user_group_campaign_mapping WHERE group_id = %(group_id)s"
                result_delete_mapping = PostgresQL().excute_query(sql=sql_delete, data = data)
                if result_delete_mapping:
                    sql_delete_group = "DELETE FROM group_campaign WHERE group_id = %(group_id)s"
                    result_delete_group = PostgresQL().excute_query(sql=sql_delete_group, data=data)
        except Exception as err:
            self.logger.error(f"[GetDataPostgresql][delete_group_campaign]: %s", exc_info=True)
        else:
            if result_delete_group:
                return result_delete_group
