from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()
admin.site.index_template = "admin/payroll_index.html" 

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^p/', 'payroll.views.payroll_list'),
    (r'', include(admin.site.urls)),
)


