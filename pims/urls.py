from django.conf.urls import patterns, include, url
from system import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pims4.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/login/$', views.login_view, name="login_view"),
    url(r'^accounts/logout/$', views.logout_view, name='log_out'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^system/', include('system.urls')),
)
