import datetime, time

from .models import CampaignHistory, Campaign, GroupCampaign, UserCampaign
from .utils.logger import Logger
from .data.workplace_msg import WorkplaceMessage
from .utils.WorkplaceApi import workplaceapi

logger = Logger().logtoFile()

def sync_status_report(campaign_id=None):
    list_reuslt_json = {}
    time_now = (datetime.datetime.now()).strftime("%Y-%m-%d")
    try:
        if campaign_id:
            h_ss = CampaignHistory.objects.filter(campaign_id=campaign_id, status=None)
            for history in h_ss:
                result = workplaceapi.get_msg_from_thread_id(history.user_id)
                if result.get('data'):
                    msg_alter_clear = clear_data_response(result.get('data'), history.campaign_content)
                    if msg_alter_clear:
                        list_reuslt_json[msg_alter_clear[0]] = msg_alter_clear[1]
        else:
            h_ss = CampaignHistory.objects.filter(time_send__range=[f"{time_now} 00:00:01", f"{time_now} 23:59:59"], status=None)
            for history in h_ss:
                result = workplaceapi.get_msg_from_thread_id(history.user_id)
                if result.get('data'):
                    msg_alter_clear = clear_data_response(result.get('data'), history.campaign_content)
                    if msg_alter_clear:
                        list_reuslt_json[msg_alter_clear[0]] = msg_alter_clear[1]
    except Exception as e:
        logger.error("[cron][sync_status_report]: %s" %e, exc_info=True)
        return False
    else:
        if list_reuslt_json != []:
            for i in h_ss:
                msg_update = list_reuslt_json.get(i.msg_id)
                if msg_update:
                    i.time_reply = datetime.datetime.strptime(msg_update.get('time_reply'), "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=7)
                    i.status = msg_update.get('status')
            CampaignHistory.objects.bulk_update(h_ss, ['time_reply', 'status'])
            return True
        return False
    
def clear_data_response(data, campaign_content):
    try:
        print(f"data {data}")
        msg_reply = data[0]
        msg_campaign = data[1]
        if msg_reply.get('from').get('id') != '102014301659855' and msg_campaign.get('message') == campaign_content:
            status = msg_reply.get('message')
            time_reply = msg_reply.get('created_time').replace("T", " ")[:-5]
            msg_id = msg_campaign.get('id')
            return [msg_id,{"status": status, "time_reply": time_reply}]
            
    except Exception as e:
        logger.error("[cron][clear_data_response]: %s" %e, exc_info=True)

def build_and_msg_send_campaign(list_content, list_user, data_campaing):
    msg_basic = WorkplaceMessage().msg_workplace_basic
    try:
        for msg in list_content:
            content_msg = msg.get("campaign_content")
            content_id = msg.get('content_id')
            msg_basic["message"]["attachment"]["payload"]["text"] = content_msg
            for user in list_user:
                user_id = user.get('user_id')
                user_receiver = user.get('user_name')
                msg_basic["recipient"]["id"] = user_id
                result = workplaceapi.send_msg_to_user(msg_basic)
                if result:
                    history_data_save = {
                    "campaign_id" : data_campaing.get('campaign_id'),
                    "campaing_name" : data_campaing.get('campaing_name'),
                    "campaign_content" : content_msg,
                    "content_id" :content_id,
                    "user_id" : user_id,
                    "user_receiver": user_receiver,
                    "time_send" : (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                    "msg_id" : result.get('message_id'),
                } 
                    print(f"history_data_save {history_data_save}")
                    CampaignHistory.objects.create(**history_data_save)
    except Exception as err:
        logger.error("[crontab][send_campaign]: %s" %err, exc_info=True)
        

def schedule_jobs_send_msg():
    time_check_schedule = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")
    date_check_schedule = time_check_schedule[:-9]
    hours_check_schedule = time_check_schedule[11:16]
    logger.info(f"Time schedule: {time_check_schedule}")
    try:
        c_ss = Campaign.objects.filter(Campaign_Starttime__lte=time_check_schedule, Campaign_Endtime__gte=time_check_schedule, Campaign_Status=1)
        logger.info(f"result query: {c_ss}")
        for campaign in c_ss:
            campaign_id = campaign.id
            group_id = campaign.Campaign_Group_id
            end_time = (campaign.Campaign_Endtime  + datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S") if campaign.Campaign_Endtime is not None else campaign.Campaign_Endtime
            date_end_campaign = end_time[:-9]
            hours_enable_campaign = end_time[11:16]
            logger.info(f"hours_enable_schedule: {hours_enable_campaign} vs hours_check_schedule:{hours_check_schedule}")
            #nếu time hiện tại = với time được set của campaign thì vào trong này
            if hours_enable_campaign == hours_check_schedule:
                logger.info(f"campaign running: {campaign.Campaign_Name}")
                h_ss = CampaignHistory.objects.filter(campaign_id=campaign_id, user_send='crontab').order_by('status')
                if len(h_ss) > 0:
                    list_compare =[]
                    list_user_id_in_workplace = []
                    for i in h_ss:
                        if i.user_id not in list_compare:
                            list_compare.append(i.user_id)
                            if i.status == None:
                                list_user_id_in_workplace.append({"user_id" : i.user_id, "user_name" : i.user_receiver})
                else:
                    g_ss = GroupCampaign.objects.get(pk=group_id)
                    list_user_id_in_workplace = [{"user_id" : i.user_id, "user_name" : i.username} for i in g_ss.user.all()]
                
                data_campaing ={"campaign_id" : campaign.id,
                                "campaing_name": campaign.Campaign_Name}
                list_content = [ {"content_id" : content.id, "campaign_content" :content.Campaign_Content}
                                    for content in campaign.Campaign_Content.all()
                                    ]
                
                if isinstance(list_user_id_in_workplace, list) and isinstance(list_content, list):
                    logger.info("Go to process build and send message")
                    if len(list_user_id_in_workplace) == 0:
                        campaign.Campaign_Status = 0
                        campaign.save()
                    else:
                        build_and_msg_send_campaign(list_content, list_user_id_in_workplace, data_campaing)
                    
                #check nếu end_day = ngày hiện tại. thì chạy xong đổi state = 0(disable)
                if date_end_campaign == date_check_schedule:
                    logger.info(f"Disable Status Campaign: {campaign.Campaign_Name}")
                    campaign.Campaign_Status = 0
                    campaign.save()
                
    except Exception as err:
        logger.error("[crontab][schedule_jobs]: %s" %err, exc_info=True)