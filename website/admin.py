from django.contrib import admin
from .models import Profile
from .models import SharedObjects
from .models import Network
from .models import Conversation
from .models import Request
# Register your models here.
 
admin.site.register(Profile)
admin.site.register(SharedObjects)
admin.site.register(Network)
admin.site.register(Conversation)
admin.site.register(Request)