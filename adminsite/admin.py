from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin_group(admin.ModelAdmin):
    list_display =['GroupName','CreateAt']

class PostAdmin_user_campains(admin.ModelAdmin):
    list_display =['username','user_id']



admin.site.register(User_Group_Mapping)
admin.site.register(Campaign)
admin.site.register(User_Campaign_Mapping)
admin.site.register(List_Content_Campaign)
admin.site.register(User_Behavious)

######
admin.site.register(UserCampaign,PostAdmin_user_campains)
admin.site.register(GroupCampaign)
