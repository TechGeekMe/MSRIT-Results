from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update_db/(?P<usn_base>.{7})/(?P<first_usn>\d{3})-(?P<last_usn>\d{3})/$', views.update_db, name='update_db'),
    url(r'^pull/(?P<year>\d{2})/$', views.pull, name='pull'),
    url(r'^pull_dip/(?P<year>\d{2})/$', views.pull_dip, name='pull_dip'),
    url(r'^$', views.index, name='index'),
    url(r'^clean_db$', views.clean_db, name='clean_db'),
    url(r'^student_result/(?P<usn>.*)/$', views.student_result,  name='student_result'),
    url(r'^student_name_list$', views.student_name_list,  name='student_name_list'),
    url(r'^get_sem_results/$', views.get_sem_results,  name='get_sem_results'),
    url(r'^sem_results/([1-8]{1})/([A-Z]{2})/$', views.sem_results,  name='sem_results'),
    url(r'^usn_search/$', views.usn_search,  name='usn_search'),
    url(r'^get_subjects$', views.get_subjects, name='get_subjects'),
    url(r'^get_subject_results/$', views.get_subject_results, name='get_subject_results'),
    url(r'^subject_results/(\w+)/$', views.subject_results, name='subject_results'),
    url(r'^subject_results/(\w+)/([A-Z]{2})/$', views.subject_results, name='subject_results_fy'),
    url(r'^student_not_found/$', views.student_not_found, name='student_not_found'),
    url(r'^result_not_found/$', views.result_not_found, name='result_not_found'),
    url(r'^disclaimer/$', views.disclaimer, name='disclaimer')
]
