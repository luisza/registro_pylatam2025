"""ECSL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from ecsl import views
from proposal.views import get_participants  # , proposals
from ajax_select import urls as ajax_select_urls
from django.conf.urls.static import static
from django.conf import settings
from ecsl.charlas import Charlas, CharlaDetail, register_user_to_speech,\
    desregistrar_charla, MyAgenda
from ecsl.webservice import get_calendar_json
from ajax_select import urls as ajax_select_urls
from django.urls import include, path, re_path

urlpatterns = [
    path('ajax_select/', include(ajax_select_urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/agenda.json', get_calendar_json, name="api_json"),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^ajax_select/', include(ajax_select_urls)),

    re_path(r'accounts/profile/?$', views.profile_view, name="profile"),
    re_path(r'^accounts/', include('django_registration.backends.activation.urls')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^$', views.Index.as_view(), name="index"),
    re_path(r'^register/profile/create$',
        views.CreateProfile.as_view(), name='create_profile'),
    re_path(r'^register/profile/update/(?P<pk>\d+)$',  views.UpdateProfile.as_view(),
        name='edit_profile'),
    re_path(r'^registro$', views.payment_view, name='payment'),
    re_path(r'^registro/create$', views.CreateRegister.as_view(), name='create_payment'),
    re_path(r'^registro/update/(?P<pk>\d+)$',  views.PaymentUpdate.as_view(),
        name='edit_payment'),
    # re_path(r'^proposal/', include((proposals.get_urls(), 'speech'), namespace='speech')),
    re_path(r'^agenda$', Charlas.as_view(), name="list_charlas"),
    re_path(r'^miagenda$', MyAgenda.as_view(), name="mi_agenda"),
    re_path(r'participantes.js$', get_participants, name="participantes"),

    re_path(r'^charla/(?P<pk>\d+)$', CharlaDetail.as_view(), name="detail_charla"),
    re_path(r'^charla/registro/(?P<pk>\d+)$',
        register_user_to_speech, name="registra_charla"),
    re_path(r'^charla/desregistrar/(?P<pk>\d+)$',
        desregistrar_charla, name="desregistrar_charla"),


] #+ views.becas


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
