# -*- coding: utf-8 -*-
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from precisionFramework.apps.precisionCalculator.forms.signup import SignupForm
from precisionFramework.apps.precisionCalculator.models import Tool

def landing_page(request):
    return render(request, "precisionFramework/homeauth.html", {})


def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")


def home(request):
    is_registered_tool = False
    if request.user.is_authenticated:
        tools = Tool.objects.filter(user=request.user.profile)
        if tools:
            is_registered_tool = True

    return render(request, "precisionFramework/homeauth.html", {"is_registered_tool": is_registered_tool})


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homeauth')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('homeauth')

    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


