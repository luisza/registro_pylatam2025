'''
Created on 5 jul. 2017

@author: luis
'''
from proposal.models import Room
from django.http.response import JsonResponse

BASE = {
    "conferences": [
        {
            "short_title": "ECSL2017",
            "title": "Encuentro Centroamericano de Software Libre 2017",
            "description": "El Encuentro Centroamericano de Software Libre (E.C.S.L.) es una reunión anual de comunidades y grupos de usuarios afines a la temática del Software Libre y, en general, del Conocimiento Libre. Un punto de encuentro y espacio de articulación, educación, coordinación e intercambio de ideas para fortalecer acuerdos y formas de trabajo conjuntas, que faciliten la promoción de tecnologías libres y datos abiertos, así como el aporte de la misma comunidad a proyectos en torno a estos conceptos.",
            "start_date": "2017-07-21",
            "end_date": "2017-07-22",
            "picture_url": "/system/conferences/logos/000/000/001/original/RanaCirculo.png",
            "difficulty_levels": [
                {
                    "id": 1,
                    "title": "Cualquiera",
                    "description": "El evento es entendible por cualquiera sin conocimiento del tema.\r\n"
                },
                {
                    "id": 2,
                    "title": "Básico",
                    "description": "El evento requiere un conocimiento básico de los temas a tratar\r\n"
                },
                {
                    "id": 3,
                    "title": "Intermedio",
                    "description": "El evento requiere un conocimiento básico de los temas a tratar\r\n"
                },
                {
                    "id": 4,
                    "title": "Avanzado",
                    "description": "El evento requiere conocimiento avanzado del tema.\r\n"
                }
            ],
            "event_types": [
                {
                    "id": 4,
                    "title": "Panel",
                    "length": 30,
                    "description": "3 personas + una persona moderando. El panel debe conformarse con personas participantes del ECSL y la coordinación con ellas la realiza quien propone la sesión"
                },
                {
                    "id": 1,
                    "title": "Charla",
                    "length": 45,
                    "description": "Una persona facilitadora. Duración: 45 minutos (30 minutos de charla + 15 minutos para preguntas)"
                },
                {
                    "id": 2,
                    "title": "Taller técnico",
                    "length": 180,
                    "description": "Cuantas personas facilitadoras se requieran"
                },
                {
                    "id": 3,
                    "title": "Mesas de trabajo",
                    "length": 135,
                    "description": "Cuantas personas facilitadoras se requieran. Se sugiere explorar metodologías como panel rotativo, knowledge café o similares."
                },
                {
                    "id": 5,
                    "title": "Espacio de encuentro",
                    "length": 30,
                    "description": "Este espacio permitirá:  , Conectarse con personas con un interés común o un conocimiento que usted requiere , Compartir una charla relámpago , Presentar una idea para buscar colaboradores , Hacer una mesa del limón , Lo que se requiera y calce en el marc"
                }
            ],
            "rooms": [],
            "tracks": [
                {
                    "id": 4,
                    "name": "Liberemos el ciberespacio",
                    "description": "- Software libre para seguridad en infraestructura\r\n- Hardware e Internet de las Cosas (IoT)\r\n- Privacidad, vigilancia y uso de datos\r\n- Software libre y seguridad para personas usuarias"
                },
                {
                    "id": 1,
                    "name": "Aportemos al desarrollo de más y mejor Software y Hardware Libres",
                    "description": "- Frontend\r\n- Backend\r\n- UX\r\n- Web frameworks\r\n- Security by design\r\n- Aplicaciones móviles\r\n- Hardware FLOS"
                },
                {
                    "id": 3,
                    "name": "Seamos una comunidad más inclusiva y diversa",
                    "description": "- Género, identidades e inclusión\r\n- Violencia de género en Internet\r\n- Inclusión de más mujeres en ciencia y tecnología"
                },
                {
                    "id": 5,
                    "name": "Mejoremos las leyes y políticas públicas del ciberespacio",
                    "description": "- Uso de software libre en gobierno\r\n- Políticas de gobierno abierto\r\n- Políticas de acceso abierto"
                },
                {
                    "id": 2,
                    "name": "Analicemos casos y compartamos experiencias",
                    "description": "- Implementación con personas usuarias o en infraestructura\r\n- Emprendimiento y gestión empresarial\r\n- Políticas públicas y Software Libre\r\n- Aplicando FLOSSH en la educación"
                }
            ],
            "date_range": "July 21 - 22",
            "revision": 12
        }
    ],
    "version": 1
}


def get_events_list(room):
    events = []
    for schedule in room.speechschedule_set.order_by('start_time'):
        speech = schedule.speech
        events.append({
            "guid": str(speech.pk),
            "title": speech.title,
            "subtitle": '',
            "abstract": speech.speaker_information,
            "description": speech.description,
            "is_highlight": 'false',
            "require_registration": 'true',
            "start_time": schedule.start_time.strftime("%b %d %Y %H:%M:%S"),
            "end_time":  schedule.end_time.strftime("%b %d %Y %H:%M:%S"),
            "event_type_id": speech.speech_type.pk,
            "difficulty_level_id": speech.skill_level,
            "track_id": speech.topic.pk,
            "speaker_names": speech.user.get_full_name()
        })

    return events


def get_calendar_json(request):
    dev = {}
    dev.update(BASE)
    rooms = []
    for room in Room.objects.all():

        rooms.append({
            "id": room.pk,
            "name": room.name,
            "size": room.spaces,
            "map_url": room.map.url,
            "events": get_events_list(room)
        })
    dev["rooms"] = rooms
    return JsonResponse(dev)