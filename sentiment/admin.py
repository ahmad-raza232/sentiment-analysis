from django.contrib import admin
# No models to register


class MyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    

# Register your models here.
