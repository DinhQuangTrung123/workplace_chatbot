from django.http.response import HttpResponse
from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

app_name = 'adminsite'
urlpatterns = [
    path('', views.home_index,name="home"),
    path('404', view=views.error),
    path('campaign', view=views.campaign_index, name="campaign"),
    path('content', view=views.content_index, name="content"),
    
    path('dologin/',view=views.Login,name="dologin"),
    path('login/', auth_views.LoginView.as_view(template_name='page/secure/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name = 'logout'),

    path('api/content/list_content/',views.GetallListContentCampaignAPIView.as_view(),name='list_content'),
    path('api/content/create_content/',views.GetallListContentPostAPIView.as_view(),name='create_content'),
    path('api/content/delete_content/<pk>',views.PutorDeleteContentCampaign.as_view(),name='delete_content'),
    path('api/content/edit_content/<pk>',views.PutorDeleteContentCampaign.as_view(),name='edit_content'),
    
    path('api/campaign/list_campaign_getall/',views.ListallCampaignAPIView.as_view(),name='list_campaign_all'),
    path('api/campaign/list_campaign/',views.GetallCampaignAPIView.as_view(),name='list_campaign'),
    path('api/campaign/create_campaign/',views.PostallCampaignAPIView.as_view(),name='create_campaign'),
    path('api/campaign/campaign_delete/<pk>',views.PutordeleteCampaignAPIView.as_view(),name='campaign_delete'),
    path('api/campaign/campaign_edit/<pk>',views.PutordeleteCampaignAPIView.as_view(),name='campaign_put'),
    
    
    # path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/login/',views.UserLogin.as_view(),name="apilogin"),
    path('user/APIListUser',views.Getlistuser.as_view(),name='APIListUser'),
    path('user/APIuserPushDelete/<pk>',views.Pushdeletelistuser.as_view(),name='APIPushDeleteuser'),

    
    path('api/user/groupcampaign',views.GetAllGroupCampaign.as_view(),name='groupcampaign'),
    path('api/user/group',views.GetallGroup.as_view(),name='group'),
    path('users/APIuserget',views.GetallListUserAPIView.as_view(),name='APIuserget'),


    
    #lanlt23
    path('setting/user_campaign', view=views.user_campaign, name="user_campaign"),
    path('setting/group_campaign', view=views.group_campaign,name="group_campaign"),
    path('report/', view=views.report, name="report"),
    
    path('send_messger/', view=views.send_messger.as_view(), name="send_messger"),
    path('setting/sync_user_campaign', view=views.sync_user_campaign.as_view(), name="sync_user_campaign"),
    path('setting/save_group', view=views.save_group.as_view(), name='save_group'),
    path('setting/all_user_campaign', view=views.all_user_campaign.as_view(), name='get_all_user_campaign'),
    path('setting/all_group_campaign', view=views.all_group_campaign.as_view(), name='get_all_group_campaign'),
    path('report/get_report', view=views.get_report_campaign.as_view(), name='get_report_campaign'),
    path('report/sync_status_msg_campaign', view=views.sync_status_msg.as_view(), name='sync_status_msg_campaign'),
]
