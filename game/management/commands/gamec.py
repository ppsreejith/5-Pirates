from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from core.models import GlobalValues, GlobalSettings
from game.models import Profile, RoundAllotment
import time
import create_alloc_r
import after_a_session

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        order = ("start","stop","evaluate","fill","remove","init","startReg","stopReg","check","run","clear")
        self.glo = GlobalValues.objects.get()
        
        val = next( (x for x in args if x in order) ,False)
        if not val:
            self.stdout.write( "Default arguments are %s"%", ".join(order) )
            return
        self.call(val)
        return
    
    def call(self, val):
        getattr(self, val)()
        self.end()
    
    def run(self):
        self.stdout.write("Registration started\n")
        self.call("startReg")
        while raw_input("Enter 'begin' to start the game:\t") != "begin" or raw_input("Are you sure? (y)") not in ("y","Y"):
            pass
        self.call("init")
        session = 1
        self.stdout.write("Session 1 started.")
        time.sleep(self.glo.session_time*60 + 1)
        while True:
            self.call("stop")
            self.stdout.write("Session stopped, evaluating..")
            self.call("evaluate")
            self.glo = GlobalValues.objects.get()
            if session >= self.glo.no_of_sessions:
                break
            session += 1
            self.stdout.write("Session evaluated, break time..")
            self.sleep(self.glo.break_time*60 + 1)
            self.call("start")
            self.stdout.write("Starting session no: %d."%session)
            self.sleep(self.glo.session_time*60 + 1)
            #Type the evaluate, start, stopreg
        self.stdout.write("Game over..")
    
    def sleep(self,waitTime):
        self.glo.endtime = time.time() + waitTime
        self.glo.save()
        time.sleep(waitTime)
    
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
    
    def check(self):
        message = ''
        if self.glo.running:
            message = 'session ends'
        else:
            message = 'next session'
        waitTime = float(self.glo.endtime) - time.time()
        gls = GlobalSettings.objects.get()
        self.stdout.write("""
Session running:\t%s
Registrations Allowed:\t%s
Current session no:\t%d
Bonus Points:\t%d
Penalty Points:\t%d
Time till %s:\t%0.2fs
        """%(self.glo.running, self.glo.allowReg, gls.current_session,
             gls.bonus_points, gls.penalty_points, message, waitTime))
    
    def evaluate(self):
        after_a_session.go() 
        self.stdout.write("..Baby don't hurt me don't hurt me no more..")
    
    def startReg(self):
        self.glo.allowReg = True
    
    def stopReg(self):
        self.glo.allowReg = False
    
    def clear(self):
        RoundAllotment.objects.all().delete()
    
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
        
