from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update_db/(?P<usn_base>.{7})/(?P<first_usn>\d{3})-(?P<last_usn>\d{3})/$', views.update_db, name='update_db'),
    url(r'^pull/(?P<year>\d{2})/$', views.pull, name='pull'),
    url(r'^pull_dip/(?P<year>\d{2})/$', views.pull_dip, name='pull_dip'),
    url(r'^$', views.index, name='index'),
    url(r'^clean_db$', views.clean_db, name='clean_db'),
    url(r'^student_details/(?P<usn>.*)/$', views.student_details,  name='student_details'),
    url(r'^student_name_list$', views.student_name_list,  name='student_name_list')
]
