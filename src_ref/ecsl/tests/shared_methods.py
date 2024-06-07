from django.contrib.auth.models import User
from ecsl.models import EventECSL, Package, Payment, PaymentOption, Inscription
from proposal.models import Speech, SpeechType, SpeechSchedule, Topic, BlockSchedule, Room
from datetime import datetime, date

start_time = datetime(2021, 1, 13, hour=12, minute=0, second=0)
end_time = datetime(2021, 1, 13, hour=13, minute=30, second=0)
start_date = date(2021, 1, 12)
end_date = datetime.today().date()
beca_start = date(2021, 1, 12)
beca_end = datetime.today().date()
proposal_start = date(2021, 1, 12)
proposal_end = datetime.today().date()


def not_logged_in_user(self, target, redirect_to):
    response = self.client.get(target)
    return self.assertRedirects(response, redirect_to)


def create_user(user_name, user_email, password):
    if User.objects.filter(username=user_name).first():
        return User.objects.filter(username=user_name).first()
    return User.objects.create_user(username=user_name, email=user_email, password=password)


def create_eventECSL():
    if EventECSL.objects.all().first():
        return EventECSL.objects.all().first()
    return EventECSL.objects.create(logo='src/media/img/logos/RanaCirculo.png',
                                    start_date=start_date,
                                    end_date=end_date,
                                    location='San José, Costa Rica',
                                    description='Evento de prueba',
                                    current=True,
                                    organizer1='Guillermo Suárez',
                                    organizer2='Catalina Vargas',
                                    phone_event='2546-5542',
                                    start_date_proposal=proposal_start,
                                    end_date_proposal=proposal_end,
                                    email_event='ecsl@mail.com',
                                    beca_start=beca_start,
                                    beca_end=beca_end,
                                    max_inscription=50)


def create_payment_option(event):
    if PaymentOption.objects.all().first():
        return PaymentOption.objects.all().first()
    return PaymentOption.objects.create(name="Ejemplo",
                                        identification='123456',
                                        tipo='SINPE',
                                        email='ejemploSinpe@mail.com',
                                        event=event)


def create_package(event):
    if Package.objects.all().first():
        return Package.objects.all().first()
    return Package.objects.create(name='Premium',
                                  description='Alojamiento, transporte y alimentación',
                                  price=50,
                                  event=event)


def create_payment(user, payment_option, event, package):
    if Payment.objects.filter(user=user, option=payment_option).first():
        return Payment.objects.filter(user=user, option=payment_option).first()
    return Payment.objects.create(user=user,
                                  option=payment_option,
                                  codigo_de_referencia='1234',
                                  invoice='invoices/invoice.pdf',
                                  confirmado=True,
                                  event=event,
                                  package=package)


def create_inscription(user, event):
    if Inscription.objects.all().first():
        return Inscription.objects.all().first()
    return Inscription.objects.create(user=user,
                                      status=2,
                                      identification='11780354',
                                      direccion_en_su_pais='SJ',
                                      born_date=date(1996, 1, 4),
                                      institution='UCR',
                                      nationality='Costa Rica',
                                      camiseta='M',
                                      event=event)


def create_speech(user, event, topic, speech_type):
    return Speech.objects.create(user=user,
                                 speaker_information="Speaker Info",
                                 title="Speech f Testing",
                                 description="Description",
                                 audience="Audience",
                                 skill_level=2,
                                 speech_type=speech_type,
                                 topic=topic,
                                 event=event,
                                 is_scheduled=True)


def create_topic(event):
    return Topic.objects.create(name="Test Topic",
                                color="#ccffaa",
                                event=event)


def create_type(event):
    if SpeechType.objects.all().first():
        return SpeechType.objects.all().first()
    return SpeechType.objects.create(name="Test Type",
                                     time=30,
                                     event=event,
                                     is_special=0)


def create_paypal_option(event):
    return PaymentOption.objects.create(name="Paypal", identification="Paypal", tipo="Paypal", email='paypal@gmail.com',
                                        event=event)


def create_paypal_payment(user, event, package, option):
    return Payment.objects.create(option=option, user=user, confirmado=True, event=event, package=package)


def create_block_schedule():
    if BlockSchedule.objects.all().first():
        BlockSchedule.objects.all().first()
    return BlockSchedule.objects.create(start_time=start_time,
                                        end_time=end_time,
                                        is_speech=True,
                                        text='Block',
                                        color='#fff')

def create_room(event):
    if Room.objects.all().first():
        return Room.objects.all().first()
    return Room.objects.create(name="Test Room",
                               spaces=2,
                               event=event)


def create_speech_schedule(speech, room):
    if SpeechSchedule.objects.all().first():
        SpeechSchedule.objects.all().delete()
    return SpeechSchedule.objects.create(start_time=start_time,
                                         end_time=end_time,
                                         speech=speech,
                                         special=None,
                                         room=room)

