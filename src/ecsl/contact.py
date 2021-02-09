from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.contrib import messages
from ecsl.forms import ProfileForm, PaymentForm, ContactForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from captcha.fields import CaptchaField
from django.core.mail import EmailMessage, send_mail


class CustomContactFormCaptcha(ContactForm):
    captcha = CaptchaField()


def contactUs(request):
    form = CustomContactFormCaptcha()

    if request.user.is_authenticated:
        form.fields['Name'].initial = request.user.username
        form.fields['Email'].initial = request.user.email
    context = {
        'form': form,
    }

    return render(request, 'contact/contact_us.html', context)


def contact(request):
    if request.method == 'POST':
        form = CustomContactFormCaptcha(request.POST)
        if form.is_valid():
            if (EmailMessage(
                    form.cleaned_data.get("Subject"),
                    'Nombre:' + form.cleaned_data.get('Name') + '\n' + form.cleaned_data.get("Message"),
                    request.POST['Email'],
                    [settings.DEFAULT_FROM_EMAIL],
                    headers={'Reply-To': request.POST['Email']},
            ).send()):
                messages.success(request, _('Thanks! Your message was sent successfully'))
        else:
            messages.success(request, _('Wrong captcha, try again'))
            form.captcha = ""
            return render(request, 'contact/contact_us.html', {'form': form})
    return redirect(reverse('contact-us'))
