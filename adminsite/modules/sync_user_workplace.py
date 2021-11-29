from ..utils.postgresql import PostgresQL
from ..utils.WorkplaceApi import WorkPlaceAPI
from ..utils.logger import Logger
from ..models import UserCampaign
from ..serializers import UserCampaignFromID

class SyncUserWorkplace(object):
    def __init__(self):
        self.logger = Logger().logtoFile()

    def sync_user_from_group_id(self, data='1518689968432916'):
        self.logger.info(f"[SyncUserWorkplace][sync_user_from_group_id]: sync data from group_id {data}")
        result = None
        user_add_new = []
        try:
            result = WorkPlaceAPI().get_all_user_from_group_id(data)
            result_all_user = UserCampaign.objects.all()
            serializers_data = UserCampaignFromID(data=result_all_user, many=True)
            serializers_data.is_valid()
        except Exception as err:
            self.logger.error("[SyncUserWorkplace][sync_user_from_group_id] %s" %err, exc_info=True)
        else:
            if serializers_data.data:
                list_all_user = [i.get('user_id') for i in serializers_data.data]
                for i in result:
                    if i.get('id') not in list_all_user:
                        user_add_new.append({'username': i.get('name'), 'user_id': i.get('id')})
            else:
                user_add_new = result
            if user_add_new:
                obj_user_add_new = [UserCampaign(**i) for i in user_add_new]
                UserCampaign.objects.bulk_create(obj_user_add_new)
        finally:
            return result