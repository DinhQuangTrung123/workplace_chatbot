from rest_framework import serializers
from .models import Campaign,List_Content_Campaign,User_Behavious,UserCampaign,GroupCampaign
from django.contrib.auth.models import User as User_Name
from django.contrib.auth.models import Group as Groups_user
from django.contrib.auth.hashers import make_password


class GetallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Name
        fields = ('id','username','password')
    

class GetallGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups_user
        fields = ('id','name')

class GetallUserBehaviousSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Behavious
        # fields = "__all__"
        fields = ('Campaign_User_Behavious','user','status')
    
    CampaignUserBehavious = serializers.SerializerMethodField('get_CampaignUserBehavious_name')
    def get_CampaignUserBehavious_name(self, obj):
        return obj.CampaignUserBehavious.Campaign_Name

    user = serializers.SerializerMethodField('get_user_name')
    def get_user_name(self, obj):
        return obj.user.username



class GetallListContentCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = List_Content_Campaign
        fields = "__all__"

    Create_By = serializers.SerializerMethodField('get_createby_name')
    def get_createby_name(self, obj):
        return obj.Create_By.username

    Modified_By = serializers.SerializerMethodField('get_updateby_name')
    def get_updateby_name(self, obj):
        try:
            if obj.Modified_By is not None:
                return obj.Modified_By.username
            return None
        except Exception as e:
            print("%s" %e)


class GetallListContentpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = List_Content_Campaign
        fields = "__all__"

class PostCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"
    
class GetallCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        # fields = "__all__"
        fields = ('id','Campaign_Name','Campaign_Starttime','Campaign_Endtime','Campaign_Content','Campaign_Status','Campaign_Group','Create_By','Create_At','Modified_By','Modified_At')# các thông tin trả về cho client thì định ngĩa ở trong field lấy ra từ model
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["Campaign_Content"] = GetallListContentCampaignSerializer(instance.Campaign_Content.all(), many=True).data
        return rep

    # def get_group_name(self, instance):
    #     rep_group = super().get_group_name(instance)
    #     rep_group['Campaign_Group'] = GetallGroupSerializer(instance.Campaign_Group.name,many=True).data
    #     return rep_group

    # def get_group_name(self, instance):
    #     rep_group = super().get_group_name(instance)
    #     rep_group['Campaign_Group'] = GetallGroupSerializer(instance.Campaign_Group.name,many=True).data
    #     return rep_group

    Create_By = serializers.SerializerMethodField('get_createby_name')
    def get_createby_name(self, obj):
        return obj.Create_By.username

    # Campaign_Group = serializers.SerializerMethodField('get_campaigngroup_name')
    # def get_campaigngroup_name(self, obj):
    #     return obj.Campaign_Group.name
    
    Modified_By = serializers.SerializerMethodField('get_updateby_name')
    def get_updateby_name(self, obj):
        try:
            if obj.Modified_By is not None:
                return obj.Modified_By.username
            return None
        except Exception as e:
            print("%s" %e)

class GroupCampaignFromID(serializers.ModelSerializer):
    class Meta:
        model = GroupCampaign
        fields = ('id' ,'group_name')

class UserCampaignFromID(serializers.ModelSerializer):
    class Meta:
        model = UserCampaign
        fields = "__all__"

class AllUserCampaign(serializers.ModelSerializer):
    class Meta:
        model = UserCampaign
        fields = "__all__"
    user_group_campaign_mapping = GroupCampaignFromID(many=True, read_only=True)


class AllGroupCampaign(serializers.ModelSerializer):
    class Meta:
        model = GroupCampaign
        fields = "__all__"
    user_group_campaign_mapping = UserCampaignFromID(many=True, read_only=True)


  