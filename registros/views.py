from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumnos
from .forms import ComentarioContactoForm
from .models import ComentarioContacto
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