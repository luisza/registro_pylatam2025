from django.http import HttpResponse
from ecsl.models import EventECSL
from ECSL.celery import app
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, EmailMessage

from ECSL import settings


@app.task
def checking_proposal_date():
    event = EventECSL.objects.filter(current=True).first()
    date_result = event.checking_start_date
    if date_result:
        proposal_period_notification()


def proposal_period_notification():
    event = EventECSL.objects.filter(current=True).first()
    user_emails = User.objects.all().values('email')
    to_emails = [email.get('email') for email in user_emails]
    text_message = _('Dear user, we want to inform you that the speech proposals period for ECSL %(ecsl)s %(year)s'
                     ' is active from %(start)s to %(end)s.'
                     'Please follow this link to teh speech from request:') \
                      % {'ecsl': event.location,
                         'year': event.start_date.strftime('%Y'),
                         'start': event.start_date_proposal.strftime('%x'),
                         'end': event.end_date_proposal.strftime('%x')}


    subject = _('Proposal Speech Period ECSL-{}').format(event.start_date.strftime('%Y'))
    email = EmailMessage(
        subject,
        text_message,
        event.email_event,
        to_emails,
        reply_to=[settings.DEFAULT_FROM_EMAIL]
    )
    try:
        email.send(fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
