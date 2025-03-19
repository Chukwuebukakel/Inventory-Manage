from django.contrib import admin
from user.models import Profile


# Register your models here.
admin.site.register(Profile)



class Profile(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['username', 'phone', 'branch']




