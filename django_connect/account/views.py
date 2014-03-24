from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from users.models import User

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

# # Check email changes
# if form.cleaned_data['email'] != initial_user.email:

# # Check phone changes
# if form.cleaned_data['phone']:
#     if not initial_user.phone:
#         # create new phone
#         NewPhone.objects.create_new_phone(user, form.cleaned_data['phone'])
#         # send new phone email
#         pass
#     elif form.cleaned_data['phone'] != initial_user.phone:
#         # send change phone email
#         pass


def verify_email(request):
    return render(request, 'account/verify_email.html', {
        'email': request.GET.get('email'),
        'key': request.GET.get('key'),
    })