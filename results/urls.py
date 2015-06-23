from django.conf.urls import include, url, handler404, handler500
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'results.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('results_app.urls', namespace='results_app')),
]

handler404 = 'results_app.views.custom_404'
handler500 = 'results_app.views.custom_500'
