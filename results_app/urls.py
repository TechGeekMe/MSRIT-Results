from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^update_db$', views.update_db, name='update_db'),
    url(r'^update_db/(?P<usn_base>.{7})/(?P<first_usn>\d{3})-(?P<last_usn>\d{3})/$', views.update_db, name='update_db'),
    url(r'^$', views.index, name='index'),
    url(r'^clean_db$', views.clean_db, name='clean_db'),
    url(r'^test$', views.test, name='test'),
]
