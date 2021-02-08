from django.test import TestCase, Client
from .shared_methods import create_user, create_eventECSL, not_logged_in_user, create_payment, create_package, \
    create_payment_option, create_inscription as create_event_inscription
from ecsl.models import EventECSL, Inscription, Encuentros_Anteriores, Gustos, Package, Payment, PaymentOption
from http import HTTPStatus
from django.urls import reverse, reverse_lazy

USER_NAME = 'test2'
USER_EMAIL = 'test2@mail.com'
PASSWORD = 'testtest2'


def create_gustos():
    return Gustos.objects.create(name="Gusto Test")


def create_encuentros_anteriores():
    return Encuentros_Anteriores.objects.create(name="ECSL Test")


def create_inscription(self):
    return self.client.post(reverse('create_profile'), data={
        'first_name': 'Tester',
        'last_name': 'Testing',
        'identification': '11230456',
        'direccion_en_su_pais': 'San José, Costa Rica',
        'nationality': 'Costa Rica',
        'gender': 'Masculino',
        'camiseta': 'M',
        'born_date': '2000-01-01',
        'institution': 'UCR',
        'encuentros': self.encuentros.pk,
        'alimentary_restriction': 'Ninguna',
        'health_consideration': 'Ninguna',
        'gustos_manias': self.gustos.pk,
        'observacion_gustos_manias': 'Ninguna',
        'comentario_general': 'Ninguno',
        'aparecer_en_participantes': 1,
    })


class CreateProfileTest(TestCase):
    """
        This view displays a form to get registered as an event participant. The user has to fill this form with
        his/her personal information. Once the form is submitted, the data is recorded in the database and the
        user is taken as an event participant. The user should get redirected to the main page after the form submitting.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.event = create_eventECSL()
        self.gustos = create_gustos()
        self.encuentros = create_encuentros_anteriores()

    def test_create_profile(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('create_profile'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        inscriptions = Inscription.objects.filter(user=self.user).count()
        self.assertEqual(inscriptions, 0)

        response = create_inscription(self)
        self.assertRedirects(response, reverse('index'))

        inscriptions = Inscription.objects.filter(user=self.user).count()
        self.assertEqual(inscriptions, 1)
        Inscription.objects.filter(user=self.user).delete()

    def test_create_profile_not_logged_in_user(self):
        target = '/register/profile/create'
        redirect_to = '/accounts/login/?next=/register/profile/create'
        not_logged_in_user(self, target, redirect_to)

    def test_create_profile_empty_form(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.post(reverse('create_profile'))  # Posting an empty form
        self.assertEqual(response.status_code, HTTPStatus.OK)
        inscriptions = Inscription.objects.filter(user=self.user).count()  # Checking no inscription were created
        self.assertEqual(inscriptions, 0)

    def test_create_profile_no_active_event(self):
        EventECSL.objects.filter(pk=self.event.pk).update(current=False)
        self.client.login(username=USER_NAME, password=PASSWORD)

        response = create_inscription(self)
        inscriptions = Inscription.objects.filter(user=self.user).count()  # Checking no inscription were created
        # inscriptions 0 due to user should not be able to register for an event that does not exist
        self.assertEqual(inscriptions, 0)
        self.assertRedirects(response, reverse('no-events'))

        Inscription.objects.filter(user=self.user).delete()
        EventECSL.objects.filter(pk=self.event.pk).update(current=True)

    def test_create_profile_existing_profile(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = create_inscription(self)
        response = self.client.get(reverse('create_profile'))
        profile = Inscription.objects.filter(user=self.user).first()
        self.assertRedirects(response, reverse('edit_profile', args=(profile.pk,)))

        Inscription.objects.filter(user=self.user).delete()
