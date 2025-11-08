from django.contrib import admin
from .models import User,OAuthAccount

# Register your models here.

admin.site.register(User)
admin.site.register(OAuthAccount)
