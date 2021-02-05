from django.urls import path
from ecsl.webservice import get_calendar_json
from ecsl import charlas as speechviews
from ecsl import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('api/agenda.json', get_calendar_json, name="api_json"),
    path('agenda', speechviews.Charlas.as_view(), name="list_charlas"),
    path('edit-agenda', speechviews.EditCharlas.as_view(), name="edit_charlas"),
    path('miagenda', speechviews.MyAgenda.as_view(), name="mi_agenda"),

    path('charla/<int:pk>', speechviews.CharlaDetail.as_view(), name="detail_charla"),
    path('charla/registro/<int:pk>',
        speechviews.register_user_to_speech, name="registra_charla"),
    path('charla/desregistrar/<int:pk>',
        speechviews.desregistrar_charla, name="desregistrar_charla"),
    path('accounts/profile/', views.profile_view, name="profile"),
    path('register/profile/create',
            views.CreateProfile.as_view(), name='create_profile'),
    path('register/profile/update/<int:pk>', views.UpdateProfile.as_view(),
            name='edit_profile'),
    path('registro', views.payment_view, name='payment'),
    path('registro/create', views.CreateRegister.as_view(), name='create_payment'),
    path('registro/update/<int:pk>', views.PaymentUpdate.as_view(),
            name='edit_payment'),

    path('process-payment/<str:text>', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('sineventos/', views.noEvents, name='no-events'),
    path('becas/', views.BecasCreate.as_view(), name="becas-create"),
    path('becas/detail/<int:pk>', views.BecasDetail.as_view(), name="becas-detail"),
    path('contact/', views.contactUs, name='contact-us'),
    path('contact/send/', views.contact, name='contact'),
]