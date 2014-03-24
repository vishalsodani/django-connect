import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def me(request):
	return render(request, 'users/me.html', {
        'user': request.user
    })