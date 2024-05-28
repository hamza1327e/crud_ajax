from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.forms import Record
from app.models import RecordTable

def SignupPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            return HttpResponse("Your password and confirm password do not match!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect("home")

    return render(request, 'signup.html')


def LoginPage(request):
    error_message = None

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('home')
        else:
            error_message = "Username or password incorrect!"

    return render(request, 'login.html', {'error_message': error_message})


def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    if request.method == 'POST':
        form = Record(request.POST)
        if form.is_valid():
            record = form.save()
            data = RecordTable.objects.values()
            data_list = list(data)
            return JsonResponse({'success': 'Save', 'record': {'id': record.id, 'first_name': record.first_name, 'last_name': record.last_name, 'email': record.email, 'phone': record.phone, 'city': record.city}})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': 0, 'errors': errors})

    form = Record()
    search_id = request.GET.get('id', None)

    if search_id:
        records = RecordTable.objects.filter(pk=search_id)
    else:
        records = RecordTable.objects.all()

    return render(request, 'index.html', context={'form': form, 'row': records})


@login_required
def edit(request, id):
    record = get_object_or_404(RecordTable, pk=id)
    if request.method == 'POST':
        form = Record(request.POST, instance=record)
        if form.is_valid():
            form.save()
            data = RecordTable.objects.values()
            data_list = list(data)
            return JsonResponse({'success': 'Update', 'record': {'id': record.id, 'first_name': record.first_name, 'last_name': record.last_name, 'email': record.email, 'phone': record.phone, 'city': record.city}})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': 0, 'errors': errors})
    else:
        form = Record(instance=record)
        record_data = {
            'first_name': record.first_name,
            'last_name': record.last_name,
            'email': record.email,
            'phone': record.phone,
            'city': record.city,
        }
        return JsonResponse({'record': record_data})


@login_required
def delete(request, id):
    try:
        record = RecordTable.objects.get(pk=id)
        record.delete()
        return JsonResponse({'status': 1}, status=200)
    except RecordTable.DoesNotExist:
        return JsonResponse({'status': 0}, status=404)
