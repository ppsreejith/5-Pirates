from django.db import models

class GlobalSettings(models.Model):
    current_session = models.PositiveIntegerField()
    penalty_points = models.PositiveIntegerField() # Indicates how much points will be the penalty for editing each time.
    bonus_points = models.PositiveIntegerField() # Maximum bonus points for exact guess. Reduced by a factor as the difference increases.
    
    def clean(self):
        if (GlobalSettings.objects.count() > 0 and self.id != GlobalSettings.objects.get().id):
            raise ValidationError("Can only create 1 %s instance" % model.__name__)

class GlobalValues(models.Model):
    dashboard = models.TextField()
    loginScroll = models.TextField()
    ship1 = models.TextField()
    ship2 = models.TextField()
    ship3 = models.TextField()
    ship4 = models.TextField()
    ship5 = models.TextField()
