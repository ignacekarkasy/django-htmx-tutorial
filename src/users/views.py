from django.shortcuts import render, redirect

from .forms import ProfileEditForm


def profile_view(request):
    profile = request.user.profile
    return render(request, 'users/profile.html', {'profile': profile})


def profile_edit_view(request):
    form = ProfileEditForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'users/profile_edit.html', {'form': form})
