import queue
from ..utils.logger import Logger
from ..utils.WorkplaceApi import workplaceapi

class SendMsgWorkplaceBackground(object):
    def __init__(self):
        self.logger = Logger().logtoFile()
        self.q = queue.Queue()

    def send_msg(self, list_user_id , json_content_msg):
        try:
            if isinstance(list_user_id, list) and isinstance(json_content_msg, list):
                for msg in json_content_msg:
                    contetn_msg = msg.get("CampaingnContent")
                    self.msg_basic["message"]["attachment"]["payload"]["text"] = contetn_msg
                    for user in list_user_id:
                        self.msg_basic["recipient"]["id"] = user.get("user_id")
                        response_ = workplaceapi.send_msg_to_user(self.msg_basic)
                        print(response_)
        except Exception as err:
            self.logger.error("[SendMsgWorkplaceBackground][send_msg]: %s" %err, exc_info=True)
        else:
            pass
        finally:
            pass

