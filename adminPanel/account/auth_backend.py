'''Defines which authentication backend for registration app.'''
from django.contrib.auth.backends import ModelBackend
from .models import RabbitUser


class RabbitUserModelBackend(ModelBackend):

    '''Authenticate AppUser'''

    def authenticate(self,  login_id=None, password=None):
        '''
        Method for authentication
        '''
        try:
            user = RabbitUser.objects.get(login_id=login_id)
            if user.check_password(password):
                return user
        except RabbitUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        '''
        Method for getting user data by passing user_id
        '''
        try:
            return RabbitUser.objects.get(pk=user_id)
        except RabbitUser.DoesNotExist:
            return None
