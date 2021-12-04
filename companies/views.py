from django.shortcuts import render

# Create your views here.
from .models import Worker, Company
from .forms import NewUserForm

def workers(request):
    workers_list = Worker.objects.order_by('first_name')
    workers_dict = {'workers_info': workers_list}
    return render(request, 'companies/index.html', workers_dict)
    

def users(request):

    form = NewUserForm()

    if request.method == 'POST':
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return workers(request)
        else:
            print('ERROR FORM INVALID')
    
    return render(request, 'companies/users.html', {'form': form})