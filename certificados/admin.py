from django.contrib import admin
from .models import Certificado

# Register your models here.
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('participante', 'tipo',)
    pass

admin.site.register(Certificado, CertificadoAdmin)
