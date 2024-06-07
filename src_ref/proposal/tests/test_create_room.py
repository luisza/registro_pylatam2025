from unittest import skip
from django.test import TestCase, Client
from django.urls import reverse
from ecsl.tests.general_set_up import GeneralSetUp
from proposal.models import Room
from django.contrib.auth.models import User, Permission


# Create your tests here.

class CreateRoomTestCase(GeneralSetUp, TestCase):

    def test_createRoom(self):
        self.current_event = self.create_event()
        user = User.objects.create(username='userexample')
        user.set_password('password')
        user.user_permissions.add(Permission.objects.get(codename='add_room'))
        user.save()
        cliente = Client()
        cliente.login(username="userexample", password='password')
        room = {
            'name': 'myroom',
            'spaces': 30,
            'map': 'map.jpg',
        }
        cliente.post(reverse('proposal:create-room'), room)
        self.assertIsNotNone(Room.objects.all().first())


    def test_createRoom_with_out_permission(self):
        self.current_event = self.create_event()
        user = User.objects.create(username='userexample')
        user.set_password('password')
        user.save()
        cliente = Client()
        cliente.login(username="userexample", password='password')
        room = {
            'name': 'myroom',
            'spaces': 30,
            'map': 'map.jpg',
        }
        response = cliente.post(reverse('proposal:create-room'), room)
        self.assertEqual(response.status_code, 403)