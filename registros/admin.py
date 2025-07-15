from django.contrib import admin
from .models import Alumnos
from .models import Comentario
from .models import ComentarioContacto

# Register your models here.

class AdministrarModelo(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('matricula', 'nombre', 'carrera', 'turno', 'created')
    search_fields = ('matricula', 'nombre', 'carrera', 'turno')
    date_hierarchy = 'created'
    list_filter = ('carrera', 'turno')

admin.site.register(Alumnos, AdministrarModelo)

class AdministrarComentarios(admin.ModelAdmin):
    list_display = ('id', 'coment')
    search_fields = ('id', 'created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')  

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name="comentaristas").exists():
            return ('alumno', 'created', 'id')
        else:
            return ('alumno', 'coment', 'created', 'id')


admin.site.register(Comentario, AdministrarComentarios)

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'created')
    search_fields = ('id', 'created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')

    def get_readonly_fields(self, request, obj = None):
        if request.user.groups.filter(name="Usuarios").exists():
            return ('created', 'updated', 'matricula', 'carrera', 'turno')
        else:
            return ('created', 'updated')

admin.site.register(ComentarioContacto, AdministrarComentariosContacto)

