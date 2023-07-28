from django.contrib import admin

from user.models import User, Expertise, Advisor, Availability

# Register your models here.
admin.site.register(User)
admin.site.register(Expertise)
admin.site.register(Advisor)
admin.site.register(Availability)
