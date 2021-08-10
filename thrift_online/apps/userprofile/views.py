from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, UserProfileForm, EditUserForm, EditUserprofileForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        userprofileform = UserProfileForm(request.POST)

        if form.is_valid() and userprofileform.is_valid():
            user = form.save()

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('cart')
    else:
        form = SignUpForm()
        userprofileform = UserProfileForm()

    return render(request, 'signup.html', {'form': form, 'userprofileform': userprofileform})

@login_required
def myaccount(request):
    if request.method == 'POST':
        u_form = EditUserForm(request.POST, instance=request.user)
        up_form = EditUserprofileForm(request.POST, instance=request.user.userprofile)

        if u_form.is_valid() and up_form.is_valid():
            u_form.save()
            up_form.save()

            return redirect('myaccount')

    else:
        u_form = EditUserForm(instance=request.user)
        up_form = EditUserprofileForm(instance=request.user.userprofile)

    context = {
        'u_form' : u_form,
        'up_form' : up_form,
    }
    
    return render(request, 'myaccount.html', context)

