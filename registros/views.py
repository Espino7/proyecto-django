from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComentarioContactoForm, FormArchivos
from .models import ComentarioContacto, Archivos, Alumnos
import datetime
from django.contrib import messages
# Accedemos al modelo Alumnos que contiene la estructura de la tabla.

# Create your views here.

def registros(request):
    alumnos=Alumnos.objects.all()
    #All recupera todos los objetos del modelo (registros de la tabla alumnos)
    return render(request, "registros/principal.html", {'alumnos':alumnos})

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): # Si los datos recibidos son correctos
            form.save() #inserta
            comentarios=ComentarioContacto.objects.all()
            return render(request, "registros/consultas.html", {'comentarios': comentarios})  # Redirecciona después de guardar
    form = ComentarioContactoForm()
    #Si algo ale mal se reenvian al formulario los datos ingresados
    return render(request, 'registros/contacto.html', {'form': form})

def contacto(request):
    return render(request, "registros/contacto.html")
    #Indicamos el lugar donde se renderiza el resultado de esta vista

def comentarios(request):
    comentarios=ComentarioContacto.objects.all()
    return render(request, "registros/comentarios.html", {'comentarios': comentarios})

def consultarComentarioIndividual(request, id):
    comentario=ComentarioContacto.objects.get(id=id)
    return render(request, "registros/formEditarComentario.html", {'comentario': comentario})

def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    if(form.is_valid):
        form.save()
        comentarios=ComentarioContacto.objects.all()
        return render(request, "registros/comentarios.html", {'comentarios':comentarios})
    return render(request, "registros/formEditarComentario", {'comentario':comentario})

def eliminarComentarioContacto(request, id, confirmacion='registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method=='POST':
        comentario.delete()
        comentarios=ComentarioContacto.objects.all()
        return render(request, "registros/comentarios.html", {'comentarios':comentarios})
    return render(request, confirmacion, {'object':comentario})

# Consultas de alumnos
def consultar1(request):
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultar2(request):
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
    alumnos=Alumnos.objects.all().only('matricula',"nombre","carrera","turno","imagen")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultar6(request):
    fechaInicio = datetime.date(2025, 6, 23)
    fechaFin = datetime.date(2025, 7, 10)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio, fechaFin))
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

def consultar7(request):
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request, "registros/consultas.html", {'alumnos':alumnos})

# Consultas de comentarios contacto
def consulta1(request):
    fechaInicio = datetime.date(2025, 7, 8)
    fechaFin = datetime.date(2025, 7, 9)
    comentarios = ComentarioContacto.objects.filter(created__range=(fechaInicio, fechaFin))
    return render(request, "registros/consultasComentario.html", {'comentarios': comentarios})

def consulta2(request):
    comentarios = ComentarioContacto.objects.filter(mensaje__contains='ARRARRIWRA RROOOOW')
    return render(request, "registros/consultasComentario.html", {'comentarios': comentarios})

def consulta3(request):
    comentarios = ComentarioContacto.objects.filter(usuario__in=["Tester 1"])
    return render(request, "registros/consultasComentario.html", {'comentarios': comentarios})

def consulta4(request):
    comentarios = ComentarioContacto.objects.only('mensaje')
    return render(request, "registros/consultaOnly.html", {'comentarios': comentarios})

def consulta5(request):
    comentarios = ComentarioContacto.objects.exclude(mensaje__contains='prueba')
    return render(request, "registros/consultasComentario.html", {'comentarios': comentarios})

#Consulta SQL

def consultarSQL(request):
    alumnos = Alumnos.objects.raw(
        "SELECT id, matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera = 'TI' ORDER BY turno DESC"
    )
    return render(request, "registros/consultas.html", {'alumnos': alumnos})


def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            archivo = form.cleaned_data['archivo']

            insert = Archivos(titulo=titulo, descripcion=descripcion, archivo=archivo)
            insert.save()

            messages.success(request, "Archivo subido correctamente")
            return render(request, "registros/archivos.html", {'form': FormArchivos()})  # formulario limpio
        else: 
            messages.error(request, "Error al procesar el formulario")
            return render(request, "registros/archivos.html", {'form': form})
    else: 
        form = FormArchivos()
        return render(request, "registros/archivos.html", {'form': form})
def subirArchivos(request):
    return render(request, "registros/archivos.html")

def seguridad(request, nombre=None):
    nombre = request.GET.get('nombre')
    return render(request, "registros/seguridad.html", {'nombre': nombre})