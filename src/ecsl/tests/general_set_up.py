from django.contrib.auth.models import User
from django.utils import timezone
from ecsl.models import Encuentros_Anteriores, Gustos, Package, PaymentOption, Payment, Inscription, EventECSL
from proposal.models import BlockSchedule, SpeechSchedule, Speech, SpecialActivity, SpeechType, Topic, Room


class GeneralSetUp():

    topic = {
        'name': 'mytopic',
        'color': 'red',
        'event': "",

    }

    speech_type = {

        'name': "speech type 1",
        'time': "30",
        'event': "",
        'is_special': "",
    }

    room = {
        'name': 'myroom',
        'spaces': 30,
        'map': 'map.jpg',
        'event': "",
    }

    user = {
        'username': 'userexample',
        'email': 'user@example.com',
        'password': 'password',
    }

    event = {

        'logo': 'logo.png',
        'start_date': (timezone.now() + timezone.timedelta(days=-1)).date(),
        'end_date': (timezone.now() + timezone.timedelta(days=-1)).date() + timezone.timedelta(days=5),
        'location': 'San Jose, Costa Rica',
        'description': 'esta es mi prueba',
        'current': True,
        'organizer1': 'Juanito Perez Rondo',
        'organizer2': 'Carla Matus Ruiz',
        'certificate_Header': 'header.png',
        'certificate_Footer': 'footer.png',
        'phone_event': '0000000',
        'start_date_proposal': timezone.now().date(),
        'end_date_proposal': (timezone.now() + timezone.timedelta(days=-1)).date(),
        'email_event': 'test@example.com',
        'beca_start': timezone.now(),
        'beca_end': (timezone.now() + timezone.timedelta(days=1)).date(),
        'max_inscription': 3,

    }

    activity = {

        'user': None,
        'speaker_information': 'profesor',
        'title': 'Testing',
        'description': 'description',
        'topic': 'testing',
        'audience': 'audiencia',
        'skill_level': 1,
        'notes': 'pc',
        'speech_type': None,
        'presentation': 'presentation',
        'event': None,

    }

    speech_schedule = {

        'start_time': timezone.now().date(),
        'end_time': (timezone.now() + timezone.timedelta(days=1)).date(),
        'speech': None,
        'room': None,
    }

    special_activity = {

        "name": "special 1",
        "type": "",
        "message": "message 1",
        "room": "",
        "event": "",
        "is_scheduled": False,
    }

    block_schedule = {

        'start_time': timezone.now().date(),
        'end_time': (timezone.now() + timezone.timedelta(days=1)).date(),
        'is_speech': True,
        'text': 'texto block',
        'color': 'red',
        'room': '',
    }

    inscription = {
        "user": "",
        "status": 0,
        "identification": "115511551155",
        "direccion_en_su_pais": "San Jose",
        "born_date": timezone.datetime(1998, 6, 29),
        "institution": "UCR",
        "gender": "Masculino",
        "nationality": "Costa Rica",
        "other_nationality": "Nicaragua",
        "encuentros": Encuentros_Anteriores.objects.first(),
        "alimentary_restriction": "ninguna",
        "health_consideration": "ninguna",
        "gustos_manias": "ninguno",
        "observacion_gustos_manias": "ninguno",
        "comentario_general": "ninguno",
        "camiseta": 'L',
        "hora_de_llegada": "8 am",
        "hora_de_salida": "11 pm",
        "medio_de_transporte": "tierra",
        "lugar_de_arribo": "san jose",
        "observaciones_del_viaje": "ninguna",
        "aparecer_en_participantes": True,
        "event": "",
    }

    payment_option = {
        "name": "opcion 1",
        "identification": "1111111",
        "tipo": "tipo 1",
        "email": "opcion1@example.com",
        "event ": "",
    }

    package = {
        "name": "primer paquete",
        "description": "paquete de 200",
        "price": "200",
        "event": "",
    }

    payment = {
        "user": "",
        "option": "",
        "codigo_de_referencia": "111111",
        "invoice": "invoice.jpg",
        "confirmado": False,
        "event": "",
        "package": "",
    }

    becas = {
        "razon": "mi razon",
        "aportes_a_la_comunidad": "mis aportes",
        "tiempo": "mi tiempo",
        "observaciones": "mis observaciones",
    }

    def create_event(self):
        return EventECSL.objects.create(logo=self.event['logo'], start_date=self.event['start_date'],
                                        end_date=self.event['end_date'], location=self.event['location'],
                                        description=self.event['description'], current=self.event['current'],
                                        organizer1=self.event['organizer1'], organizer2=self.event['organizer2'],
                                        certificate_Header=self.event['certificate_Header'],
                                        certificate_Footer=self.event['certificate_Footer'],
                                        phone_event=self.event['phone_event'],
                                        start_date_proposal=self.event['start_date_proposal']
                                        , end_date_proposal=self.event['end_date_proposal'],
                                        email_event=self.event['email_event']
                                        , beca_start=self.event['beca_start'], beca_end=self.event['beca_end'],
                                        max_inscription=self.event['max_inscription'], )

    def create_room(self):
        self.room['event'] = self.current_event
        return Room.objects.create(name=self.room['name'], spaces=self.room['spaces'], map=self.room['map'],
                                   event=self.room['event'])

    def create_user(self):
        return User.objects.create_user(username=self.user['username'], email=self.user['email'],
                                        password=self.user['password'])

    def create_topic(self):
        self.topic['event'] = self.current_event
        return Topic.objects.create(name=self.topic['name'], color=self.topic['color'], event=self.topic['event'])

    def create_type_activity(self):
        self.speech_type['event'] = self.current_event
        self.speech_type['is_special'] = False
        return SpeechType.objects.create(name=self.speech_type['name'], time=self.speech_type['time'],
                                         event=self.speech_type['event'], is_special=self.speech_type['is_special'])

    def create_special_activity(self):
        self.special_activity['event'] = self.current_event
        self.special_activity['type'] = self.create_type_activity()
        self.special_activity['room'] = self.create_room()
        return SpecialActivity.objects.create(name=self.special_activity['name'], type=self.special_activity['type'],
                                              message=self.special_activity['message'],
                                              room=self.special_activity['room'],
                                              event=self.special_activity['event'],
                                              is_scheduled=self.special_activity['is_scheduled'])

    def create_activity(self, event=None, user=None, topic=None, type=None, scheduled=False):
        if event:
            event = event
        else:
            event = self.current_event
        if user:
            user = user
        else:
            user = self.create_user()
        if topic:
            topic = topic
        else:
            topic = self.create_topic()
        if type:
            type = type
        else:
            type = self.create_type_activity()

        return Speech.objects.create(user=user, speaker_information=self.activity['speaker_information'],
                                     title=self.activity['title'], description=self.activity['description'],
                                     topic=topic, audience=self.activity['audience'],
                                     skill_level=self.activity['skill_level'], notes=self.activity['notes'],
                                     speech_type=type, presentacion=self.activity['presentation'],
                                     event=event, is_scheduled=scheduled)

    def create_speechSchedule(self, room=None, speech=None):
        if room:
            room = room
        else:
            room = self.create_room()
        if speech:
            speech = speech
        else:
            speech = self.create_activity()

        return SpeechSchedule.objects.create(start_time=self.speech_schedule['start_time'],
                                             end_time=self.speech_schedule['end_time'], speech=speech,
                                             special=None,
                                             room=room)

    def create_block_schedule(self, room=None):
        if room:
            self.block_schedule['room'] = room
        else:
            self.block_schedule['room'] = self.create_room()
        return BlockSchedule.objects.create(start_time=self.block_schedule['start_time'],
                                            end_time=self.block_schedule['end_time'],
                                            is_speech=self.block_schedule['is_speech'],
                                            text=self.block_schedule['text'], color=self.block_schedule['color'],
                                            room=self.block_schedule['room'])

    def create_inscription(self, event=None, user=None):
        if event:
            event = event
        else:
            event = self.create_event()
        if user:
            user = user
        else:
            user = self.create_user()
        self.inscription['user'] = user
        self.inscription['event'] = event
        instance = Inscription.objects.create(user=self.inscription['user'], status=self.inscription['status'],
                                              identification=self.inscription['identification'],
                                              born_date=self.inscription['born_date'],
                                              institution=self.inscription['institution'],
                                              gender=self.inscription['gender'],
                                              nationality=self.inscription['nationality'],
                                              other_nationality=self.inscription['other_nationality'],
                                              alimentary_restriction=self.inscription['alimentary_restriction'],
                                              health_consideration=self.inscription['health_consideration'],
                                              observacion_gustos_manias=self.inscription['observacion_gustos_manias'],
                                              comentario_general=self.inscription['comentario_general']
                                              , camiseta=self.inscription['camiseta'],
                                              hora_de_llegada=self.inscription['hora_de_llegada'],
                                              hora_de_salida=self.inscription['hora_de_salida'],
                                              medio_de_transporte=self.inscription['medio_de_transporte'],
                                              lugar_de_arribo=self.inscription['lugar_de_arribo'],
                                              observaciones_del_viaje=self.inscription['observaciones_del_viaje'],
                                              aparecer_en_participantes=self.inscription['aparecer_en_participantes'],
                                              event=self.inscription['event']
                                              )
        encuentros = Encuentros_Anteriores.objects.all()
        instance.encuentros.set(encuentros)
        instance.gustos_manias.set(Gustos.objects.all())
        instance.save()
        return instance

    def create_package(self, event=None):
        if event:
            event = event
        else:
            event = self.create_event()
        self.package['event'] = event
        return Package.objects.create(name=self.package['name'], description=self.package['description'],
                                      price=self.package['price'], event=self.package['event'])

    def create_payment_option(self, event=None):
        if event:
            event = event
        else:
            event = self.create_event()
        self.payment_option['event'] = event
        return PaymentOption.objects.create(name=self.payment_option['name'],
                                            identification=self.payment_option['identification'],
                                            tipo=self.payment_option['tipo'],
                                            email=self.payment_option['email'], event=self.payment_option['event'])

    def create_payment(self, user=None, event=None, package=None, option=None):
        if event:
            event = event
        else:
            event = self.create_event()
        if user:
            user = user
        else:
            user = self.create_user()
        if package:
            package = package
        else:
            package = self.create_package()
        if option:
            option = option
        else:
            option = self.create_payment_option()
        self.payment['user'] = user
        self.payment['event'] = event
        self.payment['package'] = package
        self.payment['option'] = option
        return Payment.objects.create(user=self.payment['user'], option=self.payment['option'],
                                      codigo_de_referencia=self.payment['codigo_de_referencia'],
                                      invoice=self.payment['invoice'], confirmado=self.payment['confirmado'],
                                      event=self.payment['event'], package=self.payment['package'])

    def control_test(self):
        self.current_event = self.create_event()
        self.create_speechSchedule()
        self.create_block_schedule()