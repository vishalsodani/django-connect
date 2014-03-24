from django.forms import ModelForm

from users.models import User


class UserAdminForm(ModelForm):
    
    class Meta:
        model = User