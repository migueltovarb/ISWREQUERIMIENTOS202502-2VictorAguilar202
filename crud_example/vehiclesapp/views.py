from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Vehicle
from .forms import VehicleForm

def vehicle_list(request):
    return render(request, 'vehicle_list.html')

def list_view(request):
    context = {}
    context["dataset"] = Vehicle.objects.all()
    return render(request, "list_view.html", context)

def create_view(request):
    context = {}
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    context['form'] = form
    return render(request, "create_view.html", context)

def update_view(request, id):
    context = {}
    obj = get_object_or_404(Vehicle, id=id)
    form = VehicleForm(request.POST or None, instance=obj)
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    
    context["form"] = form
    return render(request, "create_view.html", context)

def delete_view(request, id):
    context = {}
    obj = get_object_or_404(Vehicle, id=id)
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect('/')
    context["object"] = obj
    return render(request, "delete_view.html", context)