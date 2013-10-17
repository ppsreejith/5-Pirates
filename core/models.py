from django.db import models

class GlobalSettings():
    current_session = models.PositiveIntegerField()
    penalty_points = models.PositiveIntegerField() # Indicates how much points will be the penalty for editing each time.
    bonus_points = models.PositiveIntegerField() # Maximum bonus points for exact guess. Reduced by a factor as the difference increases.
    
    def clean(self):
        if (GlobalSettings.objects.count() > 0 and self.id != GlobalSettings.objects.get().id):
            raise ValidationError("Can only create 1 %s instance" % model.__name__)

