from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from core.models import GlobalValues
from game.models import Profile
import after_a_session

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        order = ("start","stop","evaluate","fill","remove","init","startReg","stopReg")
        self.glo = GlobalValues.objects.get()
        
        val = next( (x for x in args if x in order) ,False)
        if not val:
            self.stdout.write( "Default arguments are %s"%", ".join(order) )
            return
        
        getattr(self, val)()
        self.end()
    
    def init(self):
        self.glo.allowReg = False
        self.glo.save()
        GlobalSettings.objects.update(current_session = 1)
        create_alloc_r.create_alloc(1)
        self.glo.running = True
    
    def start(self):
        self.glo.running = True
        self.glo.allowReg = False
        self.stdout.write("..let there be light..")
    
    def stop(self):
        self.glo.running = False
        Session.objects.all().delete()
        self.stdout.write("..and the darkness began..")
    
    def evaluate(self):
        after_a_session.go() 
        self.stdout.write("..Baby don't hurt me don't hurt me no more..")
    
    def startReg(self):
        self.glo.allowReg = True
    
    def stopReg(self):
        self.glo.allowReg = False
    
    def fill(self):
        users = []
        profiles = []
        for i in range(0,100):
            tempuser = User(username = "autouser%d"%i,email ="autoemail%d@mail.com"%i, password = "sreejithhere")
            users.append(tempuser)
        User.objects.bulk_create(users)
        users = User.objects.filter(username__startswith = "autouser")
        for user in users:
            profile = Profile(user = user, facebook_id = i)
            profiles.append(profile)
        Profile.objects.bulk_create(profiles)
            
        self.stdout.write("..moths! MOTHS EVERYWHEREEE!!!..")

    def remove(self):
        User.objects.filter(username__startswith = "autouser").delete()
        self.stdout.write("..The genocide is complete..")
    
    def end(self):
        self.glo.save()
        
