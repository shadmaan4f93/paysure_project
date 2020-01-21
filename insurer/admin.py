from django.contrib import admin
from insurer.models import Policy,PolicyAuthorization
# Register your models here.
admin.site.register(Policy)


class AuthorizationAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp']
admin.site.register(PolicyAuthorization,AuthorizationAdmin)