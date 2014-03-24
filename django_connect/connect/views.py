import base64
import hashlib

from allaccess.views import OAuthRedirect, OAuthCallback
from allaccess.compat import smart_bytes, force_text
from allaccess.models import AccountAccess

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from auth import emails as auth_emails
from account import emails as account_emails
from users.choices import Genders
from users.models import User, NewEmail


class CustomOAuthRedirect(OAuthRedirect):

    def get_additional_parameters(self, provider):
        # if provider.name == 'facebook':
        #     # Request permission to see user's email
        #     return {'scope': 'email'}
        return super(CustomOAuthRedirect, self).get_additional_parameters(provider)


class CustomOAuthCallback(OAuthCallback):

    def get_or_create_user(self, provider, access, info):
        "Create a shell auth.User."
        digest = hashlib.sha1(smart_bytes(access)).digest()
        # Base 64 encode to get below 30 characters
        # Removed padding characters
        username = force_text(base64.urlsafe_b64encode(digest)).replace('=', '')
        # Add user data to dictionary
        kwargs = {
            'username': username,
            'password': None,
            'language': self.request.LANGUAGE_CODE,
            'timezone': self.request.session.get('django_timezone', settings.TIME_ZONE),
        }
        # Check for facebook data
        if provider.name == 'facebook':
            # Add facebook data to dictionary
			kwargs.update({
	            'first_name': info.get('first_name', ''),
	            'last_name': info.get('last_name', ''),
                'gender': Genders.get_value(info.get('gender')),
	        })
        # Create user
        user = User.objects.create_user(**kwargs)
        # Email user to welcome
        auth_emails.welcome(user)
        # Check for facebook email data
        if provider.name == 'facebook' and info.get('email'):
            # Create new email
            new_email = NewEmail.objects.create_new_email(user, info['email'])
            # Email user to verify email
            account_emails.verify_email()
        return user

    def handle_existing_user(self, provider, user, access, info):
        "Login user and redirect."
        # Check if user is active
        if not user.is_active:
            return self.handle_login_failure(provider, "Not active.")
        # login user
        login(self.request, user)
        # activate user's language
        self.request.session['django_language'] = user.language
        # activate user's timezone
        self.request.session['django_timezone'] = user.timezone
        return redirect(self.get_login_redirect(provider, user, access))