from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from content.models import Ccomment, Menu, Content, ContentForm, ContentImageForm, CImages
from home.models import UserProfile
from product.models import Category, Comment
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               }
    return render(request, 'user_profile.html', context)


def user_info(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {'category': category,
               'profile': profile,
               }
    return render(request, 'user_info.html', context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user/info')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

        context = {'category': category,
                   'user_form': user_form,
                   'profile_form': profile_form,
                   }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user/info')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form, 'category': category, })


@login_required(login_url='/login')  # Check Login
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    comment = Ccomment.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'comments': comments,
               'comment': comment,
               }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    Ccomment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted ...')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')  # Check Login
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'menu': menu,
               'contents': contents,
               }
    return render(request, 'user_contents.html', context)

@login_required(login_url='/login')  # Check Login
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()   # veritabanına kaydet
            messages.success(request, 'Your content insterted successfully!')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.error(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm()
        return render(request, 'user_addcontent.html', {'form': form, 'category': category, 'menu': menu, })

@login_required(login_url='/login')  # Check Login
def contentedit(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your content updated successfully!')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.error(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit./'+str(id))
    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm(instance=content)
        return render(request, 'user_addcontent.html', {'form': form, 'category': category, 'menu': menu, })

@login_required(login_url='/login')
def contentdelete(request, id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Content deleted ...')
    return HttpResponseRedirect('/user/contents')

def contenaddimage(request,id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.content_id = id
            data.image = form.cleaned_data['image']
            data.save()   # veritabanına kaydet
            messages.success(request, 'Your image has been successfully uploaded!')
            return HttpResponseRedirect(lasturl)
        else:
            messages.error(request, 'Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        content = Content.objects.get(id=id)
        images = []
        try:
            images = CImages.objects.filter(content_id=id)
        except:
            pass
        form = ContentImageForm()
        return render(request, 'content_gallery.html', {'form': form, 'content': content, 'images': images, })