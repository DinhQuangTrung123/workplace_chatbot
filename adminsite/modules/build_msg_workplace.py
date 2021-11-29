from ..data.workplace_msg import WorkplaceMessage
from ..utils.WorkplaceApi import WorkPlaceAPI
from ..utils.logger import Logger

class BuildMsgWorkplace(object):
    def __init__(self):
        self.logger = Logger().logtoFile()
        self.button_web = WorkplaceMessage().button_web_url
        self.button_postback = WorkplaceMessage().button_postback
        self.button_call = WorkplaceMessage().button_call_phonenumber
        self.msg_basic = WorkplaceMessage().msg_workplace_basic
        self.list_msg = []

    def build_msg_to_thread_id(self, data):
        # print(f"build_msg_to_thread_id {data}")
        try:
            if isinstance(data, list):
                for content in data:
                    content_campaign = content.get("CampaingnContent")
                    WorkplaceMessage().msg_workplace_basic["message"]["attachment"]["payload"]["text"] = content_campaign
                    self.list_msg.append(WorkplaceMessage().msg_workplace_basic)
                print(self.list_msg)
        except Exception as err:
            self.logger.error(f"[BuildMsgWorkplace][build_msg]: %s" %err, exc_info=True)
        else:
            pass
        finally:
            return self.list_msg