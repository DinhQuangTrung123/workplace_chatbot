import requests, json, threading
from requests.structures import CaseInsensitiveDict
from .logger import Logger

class WorkPlaceAPI(threading.Thread):
    def __init__(self):
        self.logger = Logger().logtoFile()
        self.access_token = 'DQVJ0d0lxQ1VuYThWeEI5TU5hMFh2TWJHWjJ0dXNOeUxBbFl5cVRhSjRlMVpkajRqajBWc044OE5NYjU0aVc5bVJxTDkyMW1qSnhtNkQyZAkhhTjFVXzNGSVNHUzkzWVRMNTJRX1psTlUweDhlc2tGOVpCWFBrODJ6a2k2TlhobDVQcDBOWHY5My1sMl9GRm9zUVlRdUNEN3ZA1RV9jdElOVTNqVV9TdFZAzalBYZAUlBaHRvYzdmS1YtVWFRNEVSbV96SXQyazEtQzlySjBsT1NhUAZDZD'
        self.my_headers = CaseInsensitiveDict()
        self.my_headers["Accept"] = "*/*"
        self.my_headers["Authorization"] = f"Bearer {self.access_token}"
        self.url = 'https://graph.workplace.com/'

    def get_all_user_from_group_id(self, group_id):
        list_user = []
        result = None
        try:
            url = self.url + f'{group_id}/members?fields=name,id&limit=1000'
            result = requests.request("GET", url=url, headers=self.my_headers)
        except Exception as e:
            self.logger.error("[WorkPlaceAPI][get_all_user_from_group_id]: %s" %e, exc_info=True)
        else:
            if result.status_code == 200:
                json_data = result.json()
                if 'data' in json_data:
                    list_user = list_user + json_data.get("data")
                while True:
                    if 'next' in json_data.get("paging"):
                        next_url = json_data.get("paging").get('next')
                        result = requests.request("GET", url=next_url, headers=self.my_headers)
                        json_data = result.json()
                        if 'data' in json_data:
                            list_user = list_user + json_data.get("data")
                    break
        finally:
            return list_user

    def get_data_from_msg_id(self, msg_id):
        url_get_msg = f"{self.url}{msg_id}?fields=message,created_time,id,tags"
        result = requests.request("GET", url=url_get_msg, headers=self.my_headers)

    def send_msg_to_user(self, msg):
        result = None
        try:
            url_post_msg = "https://graph.workplace.com/me/messages/"
            result = requests.request("POST",
                                      url=url_post_msg,
                                      json=msg,
                                      headers=self.my_headers)
        except Exception as err:
            self.logger.error("[WorkPlaceAPI][send_msg_from_thread_id]: %s" %err, exc_info=True)
        finally:
            return result.json()

    def send_msg_from_user_id(self, msg):
        result = None
        try:
            url_post_msg = "https://graph.workplace.com/me/messages/"
            result = requests.request("POST",
                                      url=url_post_msg,
                                      json=msg,
                                      headers=self.my_headers)
        except Exception as err:
            self.logger.error("[WorkPlaceAPI][send_msg_from_user_id]: %s" %err, exc_info=True)
        finally:
            return result.json()
    
    def get_msg_from_thread_id(self, thread_id):
        result = None
        try:
            url_get_msg = f"{self.url}t_{thread_id}/messages?fields=message,created_time,from&limit=2"
            result = requests.request("GET", url=url_get_msg, headers=self.my_headers)
        except Exception as err:
            self.logger.error("[WorkPlaceAPI][send_msg_from_user_id]: %s" %err, exc_info=True)
        finally:
            return result.json()
        

workplaceapi = WorkPlaceAPI()
