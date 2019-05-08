from django.contrib.auth import (
    get_user_model,
    login,
    authenticate,
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView

from test_app.forms import LoginForm, EditUserProfileForm

User = get_user_model()


class Login(FormView):
    template_name = 'test_app/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_get = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_get or next_post or None
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['username_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('test_app:users')
        return super(Login, self).form_valid(form)


class Logout(LogoutView):
    next_page = 'users'


def user_profile(request):
    context = {'user': request.user}
    return render(request, 'test_app/user.html', context)


def users_profile(request):
    '''
    List of users object
    '''
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'test_app/users.html', context)


@login_required(login_url='login')
def edit_profile(request):
    """
    Editing authorized user
    """
    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('test_app:user')
    else:
        form = EditUserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'test_app/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    """
    Change authorized user password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('test_app:user')
        else:
            return redirect('test_app:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'test_app/change_password.html', context)
