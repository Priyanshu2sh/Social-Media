from django.db import models
from django.contrib.auth.models import AbstractUser
from django import utils
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def get_password_reset_url(self):
        base64_encoded_id = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(self.id))
        token = PasswordResetTokenGenerator().make_token(self)
        reset_url_args = {'uidb64': base64_encoded_id, 'token': token}
        reset_path = reverse('reset_password', kwargs=reset_url_args)
        reset_url = f'http://127.0.0.1:8000/{reset_path}'
        return reset_url
