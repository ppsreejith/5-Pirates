from django.contrib.auth.models import User
from game.models import Profile

#for i in range(ord('a'), ord('z') + 1):
for j in range(ord('a'), ord('z') + 1):
    st = chr(j)
    email = st + '@' + st + '.' + st
    usr = User.objects.create_user(st, email, st)
    prof = Profile(user=usr, facebook_id=1)
    prof.save()

    
        
        
