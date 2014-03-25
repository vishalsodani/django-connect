from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from users.models import User, Email, NewEmail

from .forms import SettingsForm


@login_required
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.session['django_language'] = form.cleaned_data['language']
            request.session['django_timezone'] = form.cleaned_data['timezone']
            return HttpResponseRedirect(reverse('account:settings'))
    else:
        form = SettingsForm(instance=request.user)

    return render(request, 'account/settings.html', {
        'form': form,
    })


@login_required
def verify_email(request):
    # Get new email
    try:
        new_email = NewEmail.objects.get(user=request.user)
    except NewEmail.DoesNotExist:
        messages.info(request, _('Your have already verified your email.'))
        return HttpResponseRedirect(reverse('users:me'))

    # Check key
    key = request.GET.get('key')
    if not key:
        messages.error(request, _('Your link is broken. Email key is missing.'))
        return HttpResponseRedirect(reverse('users:me'))

    # Verify key
    if new_email.key != key:
        messages.error(request, _('Email key is not valid.'))
        return HttpResponseRedirect(reverse('users:me'))

    # Create email
    Email.objects.create_email(user=new_email.user, email=new_email.email)
    messages.success(request, _('You have verified your email.'))
    return HttpResponseRedirect(reverse('users:me'))