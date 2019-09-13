from django.contrib import admin

from django.contrib.auth.models import AbstractUser
from api.models import User, Client, Project, IssueTicket
# Register your models here.

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(IssueTicket)