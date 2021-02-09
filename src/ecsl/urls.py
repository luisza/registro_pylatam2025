from django.urls import path

from ecsl import Profile
from ecsl import becas
from ecsl import charlas as speechviews
from ecsl import contact
from ecsl import payment
from ecsl import views
from ecsl.webservice import get_calendar_json

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
    path('accounts/profile/', Profile.profile_view, name="profile"),
    path('register/profile/create',
         Profile.CreateProfile.as_view(), name='create_profile'),
    path('register/profile/update/<int:pk>', Profile.UpdateProfile.as_view(),
         name='edit_profile'),
    path('registro', payment.payment_view, name='payment'),
    path('registro/create', Profile.CreateRegister.as_view(), name='create_payment'),
    path('registro/update/<int:pk>', payment.PaymentUpdate.as_view(),
         name='edit_payment'),

    path('process-payment/<str:text>', payment.process_payment, name='process_payment'),
    path('payment-done/', payment.payment_done, name='payment_done'),
    path('payment-cancelled/', payment.payment_canceled, name='payment_cancelled'),
    path('sineventos/', views.noEvents, name='no-events'),
    path('becas/', becas.BecasCreate.as_view(), name="becas-create"),
    path('becas/detail/<int:pk>', becas.BecasDetail.as_view(), name="becas-detail"),
    path('contact/', contact.contactUs, name='contact-us'),
    path('contact/send/', contact.contact, name='contact'),
    path('participantes.js', views.get_participants, name="participantes"),
]
