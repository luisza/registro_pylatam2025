from datetime import datetime
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import AnonymousUser, User
from .models import EventECSL, Inscription, Payment, PaymentOption, Package, Becas
from .views import Index

import tempfile


class TestViews(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.user = User.objects.create_user(username='daniel', email='daniel@mail.com', password='daniel')
        self.event = EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                               location='Panama',
                               description='description',
                               start_date=datetime(2021, 1, 15),
                               end_date=datetime(2021, 1, 15),
                               current=True,
                               start_date_proposal=datetime(2021, 1, 15),
                               end_date_proposal=datetime(2021, 1, 15))

        self.inscription = Inscription(user=self.user,
                                       status=2,
                                       gender='Masculino',
                                       nationality='Costa Rica',
                                       identification='123456789',
                                       direccion_en_su_pais='San Jose',
                                       born_date=datetime(1997, 8, 14),
                                       institution='Solvo')

        self.paymentOption = PaymentOption(name='PagoOption',
                                           tipo='Deposito',
                                           email='email@mail.com')

        self.package = Package(name='Package',
                               description='Description',
                               price=5.00)

        self.payment = Payment(user=self.user,
                               confirmado=True,
                               event=self.event,
                               option=self.paymentOption,
                               package=self.package)

        self.becas = Becas(user=self.user,
                           razon='none',
                           aportes_a_la_comunidad='none',
                           tiempo='1 mes',
                           observaciones='no',
                           estado=2,
                           event=self.event)

    def test_index_no_event(self):
        request = self.cliente.get(reverse('index'))
        response = Index.as_view()(request)

        self.assertRedirects(response, '/sineventos/', status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_index_with_event(self):
        self.event.save()
        response = self.cliente.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

    def test_index_context(self):
        self.event.save()
        self.user.save()
        self.inscription.save()
        self.package.save()
        self.paymentOption.save()
        self.payment.save()
        response = self.cliente.get(reverse('index'))
        current_event = EventECSL.objects.filter(current=True).first()

        self.assertEqual(response.context['event_name'], str(current_event))
        self.assertEqual(response.context['event_logo'], current_event.logo)
        self.assertEqual(response.context['event_location'], current_event.location)
        self.assertEqual(response.context['event_description'], current_event.description)
        self.assertEqual(response.context['numparticipantes'], 1)
        self.assertEqual(response.context['genero'], {'masculino': 1, 'femenino': 0, 'otro': 0})

    def test_contact(self):
        response = self.cliente.get(reverse('contact'))
        self.assertRedirects(response, reverse('contact-us'), status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_contact_form(self):
        response = self.cliente.post(reverse('contact'), {'name': 'daniel','email':'daniel@mail.com', 'subject': 'something' ,'message':'message'})
        self.assertEqual(response.status_code,200)