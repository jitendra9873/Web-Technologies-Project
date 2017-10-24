from django.conf.urls import url
from django.contrib import admin
from college import views, settings
from django.conf.urls.static import static

app_name = 'college'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.indexRedirect),
    url(r'^index/$', views.indexView, name="index"),
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^signout/$', views.signout, name="signout"),
    url(r'^user/(?P<username>[0-9]+)/attendance$', views.attendance, name="attendance"),
    url(r'^dashboard/$', views.dashboardRedirect),
    url(r'^user/(?P<username>[0-9]+)/dashboard$', views.dashboardView, name="dashboard"),
	url(r'^attendance/',views.attendance,name='attendance'),
    url(r'^user/(?P<username>[0-9]+)/followers/$', views.followersView, name="followers-list"),
    url(r'^user/(?P<username>[0-9]+)/following/$', views.followingsView, name="following-list"),
	url(r'^profile/',views.profile,name='profile'),
]
