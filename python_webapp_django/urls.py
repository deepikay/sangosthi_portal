"""
Definition of urls for python_webapp_django.
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
from django.contrib import admin
# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    #SendAudioTrailer
        url(r'^statistics', app.views.statistics, name='statistics'),  # <-- this one here
    url(r'^ajax/load_questions/', app.views.load_questions, name='load_questions'),  # <-- this one here

    url(r'^ajax/load-cities/', app.views.load_cities, name='ajax_load_cities'),  # <-- this one here
    url(r'^AshaAdd', app.views.ashaAdd, name='AshaAdd'),
    url(r'^ContentAdd', app.views.ContentAdd, name='ContentAdd'),
    url(r'^ShowAdd', app.views.ShowAdd, name='ShowAdd'),
    url(r'^TextMessageAdd', app.views.TextMessageAdd, name='TextMessageAdd'),
    url(r'^SendAudioTrailerAdd', app.views.SendAudioTrailerAdd, name='SendAudioTrailerAdd'),
    url(r'^ShowFeedbackAdd', app.views.ShowFeedbackAdd, name='ShowFeedbackAdd'),
    url(r'^ShowRecordingAdd', app.views.ShowRecordingAdd, name='ShowRecordingAdd'),

    url(r'^AudioFileAdd', app.views.AudioFileAdd, name='AudioFileAdd'),

    url(r'^ExpertAdd', app.views.ExpertAdd, name='ExpertAdd'),
    url(r'^CohortAdd', app.views.CohortAdd, name='CohortAdd'),
    url(r'^ContentCategoryAdd', app.views.ContentCategoryAdd, name='ContentCategoryAdd'),
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^admin', admin.site.urls),
    url(r'^profiles/(?P<id>\d+)/$', app.views.dashboard, name='lel'),
    url(r'^Asha', app.views.ashalist, name='Asha'),
    url(r'^Cohort', app.views.cohortlist, name='Cohort'),
    url(r'^RequestList', app.views.RequestList, name='RequestList'),
    url(r'^request/(?P<id>\d+)/$',app.views.request,name="requests"),
    url(r'^request/(?P<id>\d+)/send_mail',app.views.sendmail,name="sendmail"),
    url(r'^request/(?P<id>\d+)/deleteuser',app.views.deleteuser,name="deleteuser"),

    url(r'^ReqSignUp$', app.views.signup_view2,
 {
            'template_name': 'app/SignUpReq.html',

        },
        name='ReqSignUp'),

    url(r'^add/$',app.views.def_view, {'template_name': 'app/add.html',},name='def'),
    url(r'^signup2$',
        #django.contrib.auth.views.login,
        app.views.signup_view2,
        {
            'template_name': 'app/signup.html',
            'type':'signup2',
        },
        name='signup2'),
    url(r'^signup$',
        #django.contrib.auth.views.login,
        app.views.signup_view2,
        {
            'template_name': 'app/SignUpReq.html',
            'type':'signup2',


        },
        name='signup'),

    url(r'^signup3$',
        #django.contrib.auth.views.login,
        app.views.signup_view3,
        {
            'template_name': 'app/signup.html',
            'type':'signup3',


        },
        name='signup3'),

    url(r'^login/$',
        #django.contrib.auth.views.login,
        app.views.login_view,
        {
            'template_name': 'app/login.html',
            #'authentication_form': app.forms.BootstrapAuthenticationForm,
            #'extra_context':
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
