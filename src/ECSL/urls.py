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
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from ajax_select import urls as ajax_select_urls
from django.urls import include, path, re_path



urlpatterns = [
    re_path(r'^ajax_select/', include(ajax_select_urls)),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^ajax_select/', include(ajax_select_urls)),
    re_path(r'^accounts/', include('django_registration.backends.activation.urls')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^paypal/', include('paypal.standard.ipn.urls')),
    re_path(r'', include('ecsl.urls')),
    re_path(r'^proposal/', include('proposal.urls')),
    path('captcha/', include('captcha.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #+ views.becas


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
