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
from users.choices import Genders
from users.models import User, Email, NewEmail


class CustomOAuthRedirect(OAuthRedirect):

    def get_additional_parameters(self, provider):
        return {'scope': ['email', 'user_birthday']}


class CustomOAuthCallback(OAuthCallback):

    def get_or_create_user(self, provider, access, info):
        "Create a shell users.User."
        digest = hashlib.sha1(smart_bytes(access)).digest()
        # Base 64 encode to get below 30 characters
        # Removed padding characters
        username = force_text(base64.urlsafe_b64encode(digest)).replace('=', '')
        # Add basic user data to dictionary
        kwargs = {
            'username': username,
            'password': None,
            'language': self.request.LANGUAGE_CODE,
            'timezone': self.request.session.get('django_timezone', settings.TIME_ZONE),
        }
        # Add facebook data to dictionary
        kwargs.update({
            'first_name': info.get('first_name', ''),
            'last_name': info.get('last_name', ''),
            'birthday': User.prepare_birthday(info.get('birthday')),
            'gender': Genders.get_value(info.get('gender')),
        })
        # Create user
        user = User.objects.create_user(**kwargs)
        # Create new email
        new_email = NewEmail.objects.create_new_email(user, info['email'])
        # Send welcome email to user to verify email
        auth_emails.welcome(user)
        # Return user
        return user

    def handle_existing_user(self, provider, user, access, info):
        "Login user and redirect."
        # Check if user is active
        if not user.is_active:
            return self.handle_login_failure(provider, "User account not active. Contact admin.")
        # Login user
        login(self.request, user)
        # Activate user's language
        self.request.session['django_language'] = user.language
        # Activate user's timezone
        self.request.session['django_timezone'] = user.timezone
        # Go to login redirect page
        return redirect(self.get_login_redirect(provider, user, access))