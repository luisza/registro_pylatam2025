from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from ecsl.models import EventECSL, Inscription
from ecsl.tests.general_set_up import GeneralSetUp


class UpdateProfileTestCase(GeneralSetUp, TestCase):
    user = None
    test_client = None

    def setUp(self):
        self.current_event = self.create_event()
        self.user = User.objects.create(username='userexample')
        self.user.set_password('password')
        self.user.save()
        self.test_client = Client()
        self.test_client.login(username="userexample", password='password')

    def test_updateProfile(self):
        """
            This test validate if the the profile is updated
        """
        updated_inscription = {'first_name': 'Pedro', 'last_name': 'Zuniga', 'identification': '155155155',
                               'direccion_en_su_pais':
                                   'Nicaragua', 'nationality': 'Nicaragua', 'other_nationality': 'Costa Rica',
                               'gender': 'Masculino', 'camiseta':
                                   'L', 'born_date': '29/06/1992', 'institution': 'UCR', 'encuentros':
                                   '3', 'alimentary_restriction': 'ninguna', 'health_consideration': 'ninguna',
                               'gustos_manias':
                                   '3', 'observacion_gustos_manias': 'ninguna', 'comentario_general': 'ninguno',
                               'hora_de_llegada':
                                   '8:00 am', 'hora_de_salida': '12:00 pm', 'medio_de_transporte': 'terrestre',
                               'lugar_de_arribo':
                                   'San Jose', 'observaciones_del_viaje': 'ninguno', 'aparecer_en_participantes': 'on'}

        inscription = self.create_inscription(event=self.current_event, user=self.user)
        self.test_client.post(reverse('edit_profile', kwargs={'pk': inscription.id}), updated_inscription)
        self.assertEqual('12:00 pm', Inscription.objects.all().first().hora_de_salida)

    def test_update_no_current_event(self):
        """
            The code below verify if an user can't sees any profile in the system if it does not have a current event
        """
        inscription = self.create_inscription(event=self.current_event, user=self.user)
        id = inscription.id
        event = EventECSL.objects.all().first()
        event.current = False
        event.save()
        response = self.test_client.get('/register/profile/update/{}'.format(id))
        self.assertEqual(response.status_code, 404)

    def test_updateProfile_two_event(self):
        """
            This test is useful to check when we have two event with current value equal True in other to validate that
            the inscription is updated with the correct event
        """
        updated_inscription = {'first_name': 'Pedro', 'last_name': 'Zuniga', 'identification': '155155155',
                               'direccion_en_su_pais':
                                   'Nicaragua', 'nationality': 'Nicaragua', 'other_nationality': 'Costa Rica',
                               'gender': 'Masculino', 'camiseta':
                                   'L', 'born_date': '29/06/1992', 'institution': 'UCR', 'encuentros':
                                   '3', 'alimentary_restriction': 'ninguna', 'health_consideration': 'ninguna',
                               'gustos_manias':
                                   '3', 'observacion_gustos_manias': 'ninguna', 'comentario_general': 'ninguno',
                               'hora_de_llegada':
                                   '8:00 am', 'hora_de_salida': '12:00 pm', 'medio_de_transporte': 'terrestre',
                               'lugar_de_arribo':
                                   'San Jose', 'observaciones_del_viaje': 'ninguno', 'aparecer_en_participantes': 'on'}

        inscription = self.create_inscription(event=self.current_event, user=self.user)
        self.test_client.post(reverse('edit_profile', kwargs={'pk': inscription.id}), updated_inscription)
        event_inscription = Inscription.objects.all().first().event
        self.assertEqual(EventECSL.objects.filter(current=True).first().id, event_inscription.id)

    def test_update_getting_a_profile_which_no_belong_us(self):
        """
            We send a request through url in order to get a profile that not belong us.
        """
        second_user = User.objects.create(username='userexample2')
        second_user.set_password('password')
        second_user.save()
        inscription = self.create_inscription(event=self.current_event, user=self.user)
        self.test_client.logout()
        self.test_client.login(username="userexample2", password='password')
        id = inscription.id
        response = self.test_client.get('/register/profile/update/{}'.format(id))
        self.assertEqual(response.status_code, 404)