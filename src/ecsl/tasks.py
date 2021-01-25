from django.http import HttpResponse
from ecsl.models import EventECSL
from ECSL.celery import app
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, EmailMessage

from ECSL import settings


def send_period_email_notification(event, subject, email_body):
    user_emails = User.objects.all().values('email')
    to_emails = [email.get('email') for email in user_emails]
    email = EmailMessage(
        subject,
        email_body,
        event.email_event,
        to_emails,
        reply_to=[settings.DEFAULT_FROM_EMAIL]
    )
    try:
        email.send(fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


@app.task
def checking_proposal_date():
    event = EventECSL.objects.filter(current=True).first()
    date_result = event.checking_start_date
    if date_result:
        proposal_period_notification()


@app.task
def checking_becas_date():
    event = EventECSL.objects.filter(current=True).first()
    if event.check_becas_start_date:
        becas_period_notification()


def proposal_period_notification():
    event = EventECSL.objects.filter(current=True).first()
    subject = _('Proposal Speech Period ECSL-{}').format(event.start_date.strftime('%Y'))
    text_message = _('Dear user, we want to inform you that the speech proposals period for ECSL %(ecsl)s %(year)s'
                     ' is active from %(start)s to %(end)s.'
                     'Please follow this link to the speech from request:') \
                   % {'ecsl': event.location,
                      'year': event.start_date.strftime('%Y'),
                      'start': event.start_date_proposal.strftime('%x'),
                      'end': event.end_date_proposal.strftime('%x')}

    send_period_email_notification(event, subject, text_message)


def becas_period_notification():
    event = EventECSL.objects.filter(current=True).first()
    subject = _('Scholarship Application Period ECSL-{}').format(event.start_date.strftime('%Y'))
    email_body = _('Dear user, we want to inform you that the scholarship application period for ECSL %(ecsl)s %(year)s'
                   ' is active from %(start)s to %(end)s.'
                   'Please follow this link to submit your scholarship application:') \
                 % {'ecsl': event.location,
                    'year': event.start_date.strftime('%Y'),
                    'start': event.beca_start.strftime('%x'),
                    'end': event.beca_end.strftime('%x')}

    send_period_email_notification(event, subject, email_body)
