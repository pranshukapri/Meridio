from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^register/$', views.UserFormView.as_view(),name='register'),
    url(r'^profile/$', views.profile,name='profile'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^login_user/change_password/$',views.change_password, name='change_password'),
    url(r'^profile/update_profile/$',views.update_profile, name='update_profile'),
    url(r'^profile/remove_request/(?P<decision>[a-z]+)$', views.remove_request,name='remove_request'),
    url(r'^profile/add_share/$',views.add_share, name='add_share'),
    url(r'^profile/remove_share/$',views.remove_share, name='remove_share'),
    url(r'^sharing_zone/(?P<page_id>[0-9]+)$', views.sharingzone, name='sharing_zone'),
    url(r'^sharing_zone/repo/(?P<user_id>[a-zA-Z0-9\t\n .<>?;:"\'`!@$%^&*()\[\]{}_+=|\\-]+)$', views.repository, name='repository'),
    url(r'^sharing_zone/repo/(?P<user_id>[a-zA-Z0-9\t\n .<>?;:"\'`!@$%^&*()\[\]{}_+=|\\-]+)/download/(?P<object_key>[0-9]+)$', views.download, name='download'),
    url(r'^sharing_zone/search$', views.search, name='search'),
    url(r'^sharing_zone/repo/(?P<user_id>[a-zA-Z0-9\t\n .<>?;:"\'`!@$%^&*()\[\]{}_+=|\\-]+)/preview/(?P<object_key>[0-9]+)$', views.preview, name='preview'),
    url(r'^sharing_zone/repo/(?P<user_id>[a-zA-Z0-9\t\n .<>?;:"\'`!@$%^&*()\[\]{}_+=|\\-]+)/request$', views.friend_request, name='friend'),
    url(r'^message_app/(?P<chat_id>[0-9]+)$',views.message_app,name='app_message'),
    url(r'^message_app/(?P<chat_id>[0-9]+)/chat/$',views.chat_insert,name='chat'),
    url(r'^message_app/(?P<chat_id>[0-9]+)/change_chat/$',views.chat_change,name='change_chat') 
]
