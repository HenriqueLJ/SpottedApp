from django.http import HttpResponse
from django.shortcuts import render
from core.models import Spotteds
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseForbidden

# Create your views here.

def criarSpotted(request):
    if (request.method == 'GET'):
        return render(request, "enviar.html")
    else:
        Spotteds.objects.create(titulo=request.POST.get('titulo'),
        texto=request.POST.get('mensagem'),
        categoria = request.POST.get('categoria'))
        return HttpResponse("Ideia enviada com sucesso")

def listarSpotteds(request):
    if (request.method == 'GET'):
        page = request.GET.get('page', 1)
        spotteds_list = Spotteds.objects.filter(aceito=1).order_by('-id')
        paginator = Paginator(spotteds_list, 9)
        spotteds_list = paginator.page(page)
        return render(request, 'listaspoteds.html', {'spotteds_list':spotteds_list})

def avaliarSpotteds(request):
    if request.user.is_superuser!=True:
        return HttpResponseForbidden
    if (request.method == 'GET'):
        page = request.GET.get('page', 1)
        spotteds_list = Spotteds.objects.filter(avaliado=0).order_by('id')
        paginator = Paginator(spotteds_list, 9)
        spotteds_list = paginator.page(page)
        return render(request, 'avaliaspotteds.html', {'spotteds_list':spotteds_list})
    if (request.method == 'POST'):
        if(request.POST.get('veredito') == '1'):
           spotted = Spotteds.objects.get(id=request.POST.get('id_spotted'))
           spotted.aceito=1
           spotted.avaliado=1
           spotted.save()
        else:
           spotted = Spotteds.objects.get(id=request.POST.get('id_spotted'))
           spotted.aceito=0
           spotted.avaliado=1
           spotted.save()  
        return HttpResponse(str(request.POST.get('id_spotted')))
        
def criarUsuario(request):
    if(request.method == 'GET'):
        return render(request,'criarusuario.html')
    if(request.method == 'POST'):
        user = User.objects.create_user(username=request.POST.get('usuario'),email = request.POST.get('email'),first_name = request.POST.get('nome'),last_name = request.POST.get('sobrenome'),password = request.POST.get('password'))
        user.save()
        return render(request, 'enviar.html')    

def logarUsuario(request):
    if(request.method == 'GET'):
        return render(request,'login.html')
    if(request.method == 'POST'):
        user = auth.authenticate(username=request.POST.get('usuario'),password = request.POST.get('password'))
        if user is not None:
            auth.login(request,user)
            return render(request, 'enviar.html')
        else:
            return render(request,'login.html')    

def deslogarUsuario(request):
    if(request.method == 'GET'):
        if (request.user.is_authenticated):
            auth.logout(request)    
            return render(request,'login.html')
        else:  
            return render(request,'login.html')

def contatos(request):
    return render(request,'Contatos.html')
    
def privacidade(request):
    return render(request,'Privacidade.html')