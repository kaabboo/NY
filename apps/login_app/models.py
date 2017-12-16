from __future__ import unicode_literals
import re
import bcrypt
from django.db import models


# # Create your models here.
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['user_name']
        if len(self.filter(user_name=post_data['user_name'])) > 0:
            # check this user's password
            user = self.filter(user_name=post_data['user_name'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        # if len(post_data['first_name']) < 2:
        if len(post_data['Name']) < 2:
            errors.append("name field must be at least 3 characters")
        # check length of name fields
        if len(post_data['user_name']) < 2:
            errors.append("username field must be at least 3 characters")
        # check length of password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check name fields for letter characters            
        if not re.match(NAME_REGEX, post_data['Name']):
            errors.append('name fields must be letter characters only')
        # check uniqueness of username
        if len(User.objects.filter(user_name=post_data['user_name'])) > 0:
            errors.append("username already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                # first_name=post_data['first_name'],
                Name=post_data['Name'],
                user_name=post_data['user_name'],
                password=hashed
            )
            return new_user
        return errors

class User(models.Model):
    Name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()