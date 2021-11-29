import re
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets, permissions,authentication
from django.http import HttpResponse, JsonResponse
from .serializers import *
from rest_framework import generics,status
from .models import Campaign, GroupCampaign,List_Content_Campaign,User_Behavious,User_Group_Mapping,UserCampaign,CampaignHistory
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as User_Name
from django.shortcuts import redirect
from django.contrib.auth.models import Group as Groups_user
import datetime
import uuid
import hashlib
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view


##lt23
from .modules.sync_user_workplace import SyncUserWorkplace
from .utils.WorkplaceApi import workplaceapi
from .utils.logger import Logger
from .modules.build_msg_workplace import BuildMsgWorkplace
from .modules.get_data_from_db import GetDataPostgresql
from .data.workplace_msg import WorkplaceMessage
from .modules.send_msg_workplace import SendMsgWorkplaceBackground
from .cron import sync_status_report, schedule_jobs_send_msg

logger = Logger().logtoFile()

class GetallUserBehaviousAPIView(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallUserBehaviousSerializer
    queryset =User_Behavious.objects.all()

    def get(self, request, format=None): 
        queryset=User_Behavious.objects.all()
        serializer_class = GetallUserBehaviousSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


class GetAllGroupCampaign(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GroupCampaignFromID
    queryset =GroupCampaign.objects.all()

    def get(self, request, format=None): 
        queryset_get_group=GroupCampaign.objects.all()
        serializer_class_group = GroupCampaignFromID(queryset_get_group,many=True)
        return Response(serializer_class_group.data, status=status.HTTP_200_OK)


class GetallGroup(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallGroupSerializer
    queryset =Groups_user.objects.all()

    def get(self, request, format=None): 
        queryset_get_group=Groups_user.objects.all()
        serializer_class_group = GetallGroupSerializer(queryset_get_group,many=True)
        return Response(serializer_class_group.data, status=status.HTTP_200_OK)



class ListallCampaignAPIView(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    # queryset =Campaign.objects.all()
    def get(self, request, format=None):
        status_ = request.GET.get('status', None)
        print(f"status {status_}")
        queryset_get_campaign=Campaign.objects.filter(Campaign_Status=status_)
        serializer_class_campaign = GetallCampaignSerializer(queryset_get_campaign,many=True)
        return Response(serializer_class_campaign.data, status=status.HTTP_200_OK)


class GetallCampaignAPIView(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    queryset =Campaign.objects.all()
    def get(self,request,format=None):  
        queryset_get_campaign=Campaign.objects.all()
        queryset_get_content=List_Content_Campaign.objects.all()
        queryset_get_group=Groups_user.objects.all()
        serializer_class_campaign = GetallCampaignSerializer(queryset_get_campaign,many=True)
        serializer_class_content = GetallListContentCampaignSerializer(queryset_get_content,many=True)
        serializer_class_group = GetallGroupSerializer(queryset_get_group,many=True)
        list_campaign_group=[serializer_class_campaign.data,
                              serializer_class_group.data,
                              serializer_class_content.data]
        dictionnay={}
        dictionnay['Campaign']=list_campaign_group[0]
        dictionnay['group']=list_campaign_group[1]
        dictionnay['content']=list_campaign_group[2]
        return Response(dictionnay, status=status.HTTP_200_OK)
  
class PostallCampaignAPIView(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostCampaignSerializer
    queryset =Campaign.objects.all()
    
    def post(self, request, format=None):
        print(f"request.data {request.data}")
        serializer_class = PostCampaignSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({"data":request.data,"messges":"tạo thành công"}, status=status.HTTP_201_CREATED)
        return Response({"data":request.data,"messges":"tạo thất bại"}, status=status.HTTP_400_BAD_REQUEST)


class PutordeleteCampaignAPIView(
    generics.GenericAPIView,
    ):#destroy model
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostCampaignSerializer
    queryset =Campaign.objects.all()
   
    def get(self, request,pk,format=None):
        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response({"data": "không tìm thấy"},status=status.HTTP_404_NOT_FOUND)
        serializer_class = PostCampaignSerializer(campaign)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def put(self, request,pk,format=None):
        # print(request.data)
        get_user=request.data.get("Create_By")
        user_name=User_Name.objects.get(username=get_user)
        request.data['Create_By'] = user_name.id
        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response({"data": "không tìm thấy","status":False},status=status.HTTP_404_NOT_FOUND)

        serializer_class = PostCampaignSerializer(campaign,data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({"data":request.data,"messges":"bạn đã update thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk,format=None):
        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response({"messges": "không tìm thấy","status":False},status=status.HTTP_404_NOT_FOUND)
        campaign.delete()
        return Response({"messges": "đã xóa thành công","status":True})

class GetallListContentCampaignAPIView(
    generics.GenericAPIView,
    ):#destroy model
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallListContentCampaignSerializer
    queryset =List_Content_Campaign.objects.all()
    def get(self, request, format=None): 
        queryset=List_Content_Campaign.objects.all()
        serializer_class = GetallListContentCampaignSerializer(queryset, many=True)
        return Response(serializer_class.data)
       
class GetallListContentPostAPIView(
    generics.GenericAPIView,
    ):#destroy model
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallListContentpostSerializer
    queryset =List_Content_Campaign.objects.all()
    def post(self, request, format=None):
        # print(request.data)
        if request.data.get("action")=="updateContent":
            idcontent=request.data.get("id")
            contentCampaign = List_Content_Campaign.objects.filter(id=idcontent)
            contentCampaign.update( 
                        Campaign_Name=request.data.get("Campaign_Name"),
                        Campaign_Content=request.data.get("Campaign_Content"),
                        Modified_By=request.data.get("Modified_By"),
                        )
            return Response({"data":request.data,"state":True,"messges":"Update thành công"}, status=status.HTTP_201_CREATED)
        else:
            serializer_class = GetallListContentpostSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response({"data":serializer_class.data,"state":True,"messges":"Tạo thành công"}, status=status.HTTP_201_CREATED)   

class PutorDeleteContentCampaign(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallListContentpostSerializer
    queryset =List_Content_Campaign.objects.all()  
     
    def get(self,request,pk,format=None):
        # print(request.data)
        try:
            listcontentCampaign = List_Content_Campaign.objects.get(pk=pk)
        except List_Content_Campaign.DoesNotExist:
            return Response({"data": "không tìm thấy"},status=status.HTTP_404_NOT_FOUND)
        serializer_class = GetallListContentpostSerializer(listcontentCampaign)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def put(self, request,pk,format=None):
        try:
            listcontentCampaign = List_Content_Campaign.objects.get(pk=pk)
        except List_Content_Campaign.DoesNotExist:
            return Response({"data": "không tìm thấy"},status=status.HTTP_404_NOT_FOUND)
        serializer_class = GetallListContentpostSerializer(listcontentCampaign,data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({"data":request.data,"messges":"update thành công","status":True}, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk,format=None):
        try:
            listcontentCampaign = List_Content_Campaign.objects.get(pk=pk)
        except List_Content_Campaign.DoesNotExist:
            return Response({"data": "không tìm thấy"},status=status.HTTP_404_NOT_FOUND)
        listcontentCampaign.delete()
        return Response({"status":True,"messges":"xóa data thành công"})

class GetallListUserAPIView(
    generics.GenericAPIView,
    ):
    authentication_classes = (authentication.TokenAuthentication,)   
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallUserSerializer
    queryset =User_Name.objects.all()
    def post(self, request, format=None):
        tokenget=request.data.get("Token",None)
        token = get_object_or_404(Token, key=tokenget)
        return Response(
                        {
                         "data":token.user.username,
                         "messges": "thanh cong", 
                         "threadid":str(uuid.uuid1())
                         }, 
                         status=status.HTTP_201_CREATED
                        )

class UserLogin(APIView):
    queryset = User_Name.objects.all()
    serializer_class = GetallUserSerializer
    def post(self, request):
        username = request.data.get('username',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        usersearch = authenticate(username = username,password=password)
        user_password =authenticate(password=password)
        if usersearch is None:
            return Response({'status':False,"messge":"sai tên toàn khoản hoặc mật khẩu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'username':usersearch.username,'status':True,"messge":"Đăng nhập thành công"}, status=status.HTTP_201_CREATED)
    
class Getlistuser(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallUserSerializer
    queryset =User_Name.objects.all()
    def get(self, request, format=None):
        user =User_Name.objects.all()
        serializer_class = GetallUserSerializer(user,many=True)
        return Response(serializer_class.data,status=status.HTTP_201_CREATED)



class Pushdeletelistuser(
    generics.GenericAPIView,
    ):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetallUserSerializer   
    def get(self, request,pk,format=None):
        try:
            user = User_Name.objects.get(pk=pk)
        except User_Name.DoesNotExist:
            return Response({"data": "không tìm thấy"},status=status.HTTP_404_NOT_FOUND)
        serializer_class = GetallUserSerializer(user)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def put(self, request,pk,format=None):  
        try:
            user = User_Name.objects.get(pk=pk)
        except User_Name.DoesNotExist:
            return Response({"data": "không tìm thấy"},status=status.HTTP_404_NOT_FOUND)
        serializer_class = GetallUserSerializer(user,data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk,format=None):
        try:
            user = User_Name.objects.get(pk=pk)
        except User_Name.DoesNotExist:
            return Response({"data": "không tìm thấy"},status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response("xóa thành công")


@login_required
def home_index(request):
    print(f"request.user : {request.user}")
    return render(request, 'page/admin/admin_index.html', context={'username' : request.user, "userid":request.user.id})

@login_required
def campaign_index(request):
    return render(request, 'page/admin/campaign_index.html', context={'username' : request.user, "userid":request.user.id})

@login_required
def content_index(request):
    return render(request, 'page/admin/content_index.html')


def Login(request):
    return render(request, 'page/secure/login.html')


def User(request):
    return render(request, 'page/admin/campaign_index.html')


def Group(request):
    return render(request, 'page/admin/campaign_index.html')

#lanlt23
def error(request):
    return render(request,'html/error_code_page.html',{'msg': '404', 'code' : 404})

@login_required
def report(request):
    return render(request, 'page/admin/report_index.html', context={'username' : request.user, "userid":request.user.id})

def group_campaign(request):
    return render(request, 'page/admin/group_campaign_index.html', context={'username' : request.user, "userid":request.user.id})
    
def user_campaign(request):
    return render(request, 'page/admin/user_campaign_index.html', context={'username' : request.user, "userid":request.user.id})

class sync_user_campaign(APIView):
    def __init__(self):
        self.msg_rsp = {
        "status": False,
        "msg" : "No new data !!! ",
        "dt": []
    }
        
    def get(self, request):
        try:
            result = SyncUserWorkplace().sync_user_from_group_id()
            if result:
                self.msg_rsp['dt'] = result
                self.msg_rsp['status'] = True
            return Response(self.msg_rsp)
        except Exception as e:
            logger.error("[views][sync_user_campaign] %s" %e)    

class all_user_campaign(APIView):
    def __init__(self):
        self.msg_resp = {
            'status' : False,
            'dt' : {
            }
        }
    
    def get(self, request):
        try:
            data = UserCampaign.objects.all()
            serializer_data = AllUserCampaign(data=data, many=True)
            serializer_data.is_valid()
            self.msg_resp['status'] = True
            self.msg_resp['dt']['user'] = serializer_data.data
            return Response(self.msg_resp)
        except Exception as e:
            logger.error("[views][all_user_campaign] %s" %e, exc_info=True)

class all_group_campaign(APIView):
    def __init__(self):
        self.msg_resp = {
            'status' : False,
            'dt' : {
            }
        }
    
    def get(self, request):
        try:
            group_data = GroupCampaign.objects.all()
            user_data = UserCampaign.objects.all()
            serializer_data_all_group = AllGroupCampaign(data=group_data, many=True)
            serializer_data_all_group.is_valid()
            
            serializer_data_all_user = UserCampaignFromID(data=user_data, many=True)
            serializer_data_all_user.is_valid()
            self.msg_resp['status'] = True
            self.msg_resp['dt']['group'] = serializer_data_all_group.data
            self.msg_resp['dt']['user'] = serializer_data_all_user.data
            return Response(self.msg_resp)
        except Exception as e:
            logger.error("[views][all_group_campaign]: %s" %e, exc_info=True)
            return Response(self.msg_resp)
    
class save_group(APIView):
    def __init__(self):
        self.msg_resp = {
            'status' : False,
            'dt' : {
            }
        }
        
    def post(self, request):
        try:
            json_data = request.data
            logger.info(f"[views][save_group] Json data reciever  {json_data}")
            if json_data.get("action") == "add_group":
                g_ss_check_exist = GroupCampaign.objects.filter(group_name=json_data.get("groupname"))
                if len(g_ss_check_exist) == 0:
                    g_ss = GroupCampaign.objects.create(group_name=json_data.get("groupname"))
                    for i in json_data.get('user_id'):
                        g_ss.user.add(i)
                    self.msg_resp['status'] = True 
            elif json_data.get("action") == "edit_group":
                u_ss = UserCampaign.objects.filter(user_group_campaign_mapping=json_data.get('id'))
                g_ss = GroupCampaign.objects.get(pk=json_data.get('id'))
                for u_delete in u_ss:
                    g_ss.user.remove(u_delete)
                for u_add in json_data.get('user_id'):
                    g_ss.user.add(u_add)
                self.msg_resp['status'] = True 
            elif json_data.get("action") == "delete_group":
                g_ss = GroupCampaign.objects.get(pk=json_data.get("id"))
                if g_ss:
                    g_ss.delete()
                    self.msg_resp['status'] = True 
            return Response(self.msg_resp)
        except Exception as e:
            logger.error("[views][save_group]: %s" %e, exc_info=True)
            return Response(self.msg_resp)

class send_messger(APIView):
    def __init__(self):
        self.msg_basic = WorkplaceMessage().msg_workplace_basic
        self.response_data = {
                "state": False,
                "status": status.HTTP_302_FOUND,
                "msg": "Send Failed !!!!"
            }
        
    def post(self, request, format=None):
        try:
            json_data = request.data.get("data_send")
            logger.info(f"Json data send_messger: {json_data}")
            campaing_content = json_data.get("Campaign_Content")
            group_campaign = json_data.get("Campaign_Group")
            group_data = GroupCampaign.objects.get(pk=group_campaign)
            list_user_id_in_workplace = [{"user_id" : i.user_id, "user_name" : i.username} for i in group_data.user.all()]
        except Exception as e:
            logger.error("[views][send_messger]: %s" %e, exc_info=True)
        else:
            if isinstance(list_user_id_in_workplace, list) and isinstance(campaing_content, list):
                for msg in campaing_content:
                    content_msg = msg.get("Campaign_Content")
                    content_id = msg.get('id')
                    self.msg_basic["message"]["attachment"]["payload"]["text"] = content_msg
                    for user in list_user_id_in_workplace:
                        user_id = user.get('user_id')
                        user_receiver = user.get('user_name')
                        self.msg_basic["recipient"]["id"] = user_id
                        result = workplaceapi.send_msg_to_user(self.msg_basic)
                        if result:
                            history_data_save = {
                                "campaign_id" : json_data.get("campaign_id"),
                                "campaing_name" : json_data.get("campaign_name"),
                                "campaign_content" : content_msg,
                                "content_id" :content_id,
                                "user_id" : user_id,
                                "user_receiver": user_receiver,
                                "user_send" : json_data.get('session_user'),
                                "time_send" : (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                                "msg_id" : result.get('message_id'),
                                "created_at": json_data.get("CreatedAt"),
                                "created_by" : json_data.get("CreatedBy"),
                            } 
                            CampaignHistory.objects.create(**history_data_save)
                self.response_data = {
                    "state": True,
                    "status": status.HTTP_200_OK,
                    "msg": "Send Campaign Done !!!!"
                }
        finally:
            return Response(self.response_data)
        
class get_report_campaign(APIView):
    def __init__(self):
        self.response_data = {
                "status": False,
                "msg": "Get Report Failed!!!!",
                "dt" : []
        }
    def get(self, request):
        g_ss = Campaign.objects.all()
        group_campaing = [{'campaign_id': i.id, 'campaign_name': i.Campaign_Name} for i in g_ss]
        self.response_data['status'] = True
        self.response_data['dt'] = group_campaing
        return Response(self.response_data)
    
    def post(self, request):
        try:
            json_data = request.data
            h_ss = CampaignHistory.objects.filter(campaign_id=json_data.get('campaign_id'))
            if h_ss:
                for history in h_ss:
                    row = {
                        "campaign_name": history.campaing_name,
                        "campaign_content": history.campaign_content,
                        "user_send": history.user_send,
                        "time_send":  (history.time_send  + datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S") if history.time_send is not None else history.time_send,
                        "status": history.status,
                        "user_receiver": history.user_receiver,
                        "time_reply": (history.time_reply + datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S") if history.time_reply is not None else history.time_reply
                    }
                    self.response_data['status'] = True
                    self.response_data['dt'].append(row)
            return Response(self.response_data)
        except Exception as e:
            logger.error("[sync_status_campaign][post] : %s" %e)


class sync_status_msg(APIView):
    def __init__(self):
        self.response_data = {
                "status": False,
                "msg": "Sync Status Failed!!!!",
                "dt" : []
        }
    def get(self, request):
        schedule_jobs_send_msg()
        return Response(self.response_data)
    
    def post(self, request):
        try:
            json_data = request.data
            logger.info("json_data %s" %json_data)
            campaign_id = json_data.get('campaign_id')
            if campaign_id:
                result = sync_status_report(campaign_id)
                self.response_data['status'] = result
            else:
                result = sync_status_report()
                self.response_data['status'] = result
        except Exception as e:
            logger.error("[views][sync_status_msg]: %s" %e)
        finally:
            return Response(self.response_data)