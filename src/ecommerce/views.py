from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import ProductModel

from django.contrib.auth.decorators import login_required

from .forms import ProductModelForm # <------ Archivo creado
from .models import ProductModel
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def home(request):
    html = """
    <DOCTYPE html>
    <html>
        <head>
            <style>
                h1{color: blue}
            </style>
        </head>

        <body>
            <h1>Hola Mundo<h1>
        </body>
    </html>
    """
    return HttpResponse(html)

# def home(request):
#     response = HttpResponse()
    
#     response.content = "Algun contenido de prueba"
#     response.write("<p>Página no encontrada</p>")
#     response.status_code = 404

#     return response

def redirect_to_test(request):
    return HttpResponseRedirect("/ecommerce/")

# @login_required
def product_model_list_view(request):
    query = request.GET.get("q", None)
    queryset = ProductModel.objects.all()
    if query is not None:
        queryset = queryset.filter(
            Q(title__icontains=query)
        )
    template = "ecommerce/list-view.html"
    context = {
            "products" : queryset
    }

    if request.user.is_authenticated:
        template = "ecommerce/list-view.html"
    else:
        template = "ecommerce/list-view-public.html"

    return render (request, template, context)



def product_model_delete_view(request, product_id):
    instance = get_object_or_404(ProductModel, id=product_id)# Que traiga el objeto o mande un 404
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Producto eliminado")
        return HttpResponseRedirect("/ecommerce/")
    context = {
        "product": instance
    }
    template = "ecommerce/delete-view.html"
    return render(request, template, context)

def product_model_update_view(request, product_id=None):
    instance = get_object_or_404(ProductModel, id=product_id)
    form = ProductModelForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Producto actualizado con éxito")
        return HttpResponseRedirect("/ecommerce/{product_id}".format(product_id=instance.id))
    context = {
        "form": form
    }
    template = "ecommerce/update-view.html"
    return render (request,template,context)    

def product_model_create_view(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Producto creado con éxito")
        return HttpResponseRedirect("/ecommerce/{product_id}".format(product_id=instance.id))
    context = {
        "form": form
    }
    template = "ecommerce/create-view.html"
    return render (request,template,context)


def product_model_detail_view(request, product_id):
    instance = get_object_or_404(ProductModel, id=product_id)# Que traiga el objeto o mande un 404
    context = {
        "product": instance
    }
    template = "ecommerce/detail-view.html"
    return render(request, template, context)

# def product_model_list_view(request):
    print(request.user) # < --------- Esto imprime que usuario esta logeado en la página 
    queryset = ProductModel.objects.all() # Quesryset lo que agrupa la respuesta de un modelo 
   # return HttpResponse("Un ecommerce personalizado")
    template = "ecommerce/list-view.html"
    context = {
        "products" : queryset # <-----------------------------------------------
    }

    if request.user.is_authenticated:
        template = "ecommerce/list-view.html"
    else:
        template = "ecommerce/list-view-public.html"

    return render(request, template, context)

@login_required # <---- con esto nuestra lista queda más protegida
def login_required_view(request):
    print(request.user) # < --------- Esto imprime que usuario esta logeado en la página 
    queryset = ProductModel.objects.all() # Quesryset lo que agrupa la respuesta de un modelo 
   # return HttpResponse("Un ecommerce personalizado")
    template = "ecommerce/list-view.html"
    context = {
        "products" : queryset # <-----------------------------------------------
    }

    if request.user.is_authenticated:
        template = "ecommerce/list-view.html"
    else:
        template = "ecommerce/list-view-public.html"

    return render(request, template, context)

    