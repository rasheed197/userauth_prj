# models.py
import bcrypt
from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class User(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True, validators=[
        RegexValidator(
            regex=r'((^\+234\d{10})|(^234\d{10})|(^0[789][01]\d{8}))',
            message="Phone number must be entered in the format: '+234XXXXXXXXXX', or '234XXXXXXXXXX', or '0XXXXXXXXXX' ."
        )
    ])
    organisations = models.ManyToManyField('Organisation', related_name='users', through='UserOrganisation')

    def save(self, *args, **kwargs):
        # if self._state.adding:
        #     self.password = self.hash_password(self.password)
        self.full_clean()
        super(User, self).save(*args, **kwargs)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        passwordByte = password.encode('utf-8')
        hashed = bcrypt.hashpw(passwordByte, salt)
        return hashed.decode('utf-8')
        # return hashed

    def check_password(self, password):
        passwordBytes = password.encode('utf-8') 
        storedPassword = self.password.encode('utf-8')
        return bcrypt.checkpw(passwordBytes, storedPassword)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Organisation(models.Model):
    org_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserOrganisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
