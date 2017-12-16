# APP2 MODELS
from __future__ import unicode_literals
from django.db import models
from ..login_app.models import User
import datetime

# # Create your models here.

class TripManager(models.Manager):

    def validate_trip(self, post_data, user_id):
        errors = []
        # check destination field
        if len(post_data['destination']) < 1:
            errors.append("Destination field is required")
        # check descripton field
        if len(post_data['desc']) < 1:
            errors.append("Description field is required")

        # check start_date is in future
        if post_data['start_date'] == "":
            errors.append("Travel Date From is required")
        else:
            start_date = datetime.datetime.strptime(post_data['start_date'],"%Y-%m-%d")
            if start_date < datetime.datetime.today():
                errors.append("Travel Date From must be in the future")
        
        # check end_date is not in future
        if post_data['end_date'] == "":
            errors.append("Travel Date To is required")
        else:
            end_date = datetime.datetime.strptime(post_data['end_date'],"%Y-%m-%d")
            if end_date < start_date:
                errors.append("Travel Date To must be greater than Travel Date From")

        if not errors:
            # make our new quote

            new_trip = self.create(
                destination = post_data['destination'],
                start_date = post_data['start_date'],
                end_date = post_data['end_date'],
                desc = post_data['desc'],
                user_id = user_id,
            )
            return new_trip
        return errors

    def update_trip(self, trip_id, user_id):
        favorites_update = Trip.objects.get(id=trip_id)
        favorites_update.favorites.add(User.objects.get(id=user_id))       
        favorites_update.save()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField(auto_now = False)
    end_date = models.DateField(auto_now = False)
    desc = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = 'posted_by')
    favorites = models.ManyToManyField(User, related_name ='favorite_trips')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
