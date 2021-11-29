from django.db import models
from django.contrib.auth.models import User,Group
from django.utils import timezone
from datetime import datetime, time, date, timedelta
import uuid

def today_start():
    d = date.today() 
    t = time(0, 30)
    return datetime.combine(d, t)

def today_at():
    day_now = datetime.now()
    return datetime.day_now

def today_modified():
    day_now = datetime.now()
    return datetime.day_now


def tomorrow():
    d = date.today() + timedelta(days=1)
    t = time(0, 0)
    return datetime.combine(d, t)

class User_Group_Mapping(models.Model):
    class Meta:
        db_table = "user_group_mapping"
    Users=models.ManyToManyField(User,related_name='user')
    Groups=models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.Groups.name

class List_Content_Campaign(models.Model):
    class Meta:
        db_table = "list_conten_campaign"
    Campaign_Name= models.CharField(max_length=255)
    Campaign_Content = models.CharField(max_length=255)
    Create_At =models.DateTimeField(auto_now_add=True)
    Create_By=models.ForeignKey(User, on_delete=models.CASCADE,related_name='Create_By_Usercontent')
    Modified_At=models.DateTimeField(auto_now=True)
    Modified_By=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='Modified_By_User_Content')

    def __str__(self):
        return self.Campaign_Name

class User_Room(models.Model):
    class Meta:
        db_table = "user_room"
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room_id= models.CharField(max_length=255)


class Campaign(models.Model):
    class Meta:
        db_table = "campaign"
    # models.ManyToManyField('ListContentCampaign', related_name='ListContentCampaign')
    Campaign_Name =  models.CharField(max_length=255)
    Campaign_Content = models.ManyToManyField('List_Content_Campaign', related_name='List_Content_Campaign')
    # CampaignOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    Campaign_Status =  models.IntegerField()
    Campaign_Group = models.ForeignKey('GroupCampaign', on_delete=models.CASCADE)
    Campaign_Starttime =models.DateTimeField(default=today_start)
    Campaign_Endtime = models.DateTimeField(default=tomorrow)
    Create_At =models.DateTimeField(auto_now_add=True)
    Create_By= models.ForeignKey(User, on_delete=models.CASCADE,related_name='Create_By_User_Campaign')
    Modified_At= models.DateTimeField(auto_now=True)
    Modified_By= models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='Modified_By_User_Campaign')


    def __str__(self):
        return self.Campaign_Name

class User_Campaign_Mapping(models.Model):
    class Meta:
        db_table = "user_Campaign_mapping"
    Campaigns= models.ForeignKey(Campaign, on_delete=models.CASCADE)
    Users = models.ForeignKey(User, on_delete=models.CASCADE)
    messages_id= models.CharField(max_length=255)

class User_Behavious(models.Model):
    class Meta:
        db_table = "user_behavious"
    Campaign_User_Behavious = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    status= models.IntegerField()

    def __str__(self):
        return self.user.username
    
    #########
class UserCampaign(models.Model):
    class Meta:
        db_table = "campaign_user"
    user_id= models.CharField(max_length=255)
    thread_id = models.CharField(max_length=255, null=True)
    username= models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    
    def __int__(self):
        return self.id


class GroupCampaign(models.Model):
    class Meta:
        db_table = "campaign_group"
        
    group_name = models.CharField(max_length=255)
    user = models.ManyToManyField('UserCampaign', related_name="user_group_campaign_mapping", blank=True, null=True)
    
    def __str__(self):
        return self.group_name

class CampaignHistory(models.Model):
    class Meta:
        db_table = 'campaign_history'
        
    campaign_id = models.IntegerField()
    campaing_name = models.CharField(max_length=255)
    campaign_content = models.CharField(max_length=255)
    content_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    user_receiver = models.CharField(max_length=255, null=True)
    user_send = models.CharField(max_length=100, default='crontab')
    time_send = models.DateTimeField(default=today_start)
    msg_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=255,null=True)
    time_reply = models.DateTimeField(null=True)