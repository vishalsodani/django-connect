from django.forms import ModelForm

from users.models import User


class SettingsForm(ModelForm):
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'birthday', 'gender', 
            'language', 'timezone',
        ]