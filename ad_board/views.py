from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Advertisement, Comment
from .forms import AdvertisementForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout


def advertisement_list(request):
    # Получение всех объявлений с пагинацией
    advertisements = Advertisement.objects.all().order_by('-created_at')
    paginator = Paginator(advertisements, 4)  # По 10 объявлений на странице
    page = request.GET.get('page')
    ads = paginator.get_page(page)

    return render(request, 'ad_board/advertisement_list.html', {'ads': ads})

def advertisement_detail(request, pk):
    # Получение детальной информации об объявлении
    ad = get_object_or_404(Advertisement, pk=pk)
    comments = Comment.objects.filter(advertisement=ad).order_by('-created_at')

    return render(request, 'ad_board/advertisement_detail.html', {'ad': ad, 'comments': comments})

@login_required
def create_advertisement(request):
    # Создание нового объявления
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('advertisement_list')
    else:
        form = AdvertisementForm()

    return render(request, 'ad_board/create_advertisement.html', {'form': form})

@login_required
def edit_advertisement(request, pk):
    # Редактирование существующего объявления
    ad = get_object_or_404(Advertisement, pk=pk)

    if request.user != ad.author:
        raise Http404("У вас нет прав на редактирование этого объявления")

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=ad)
        if form.is_valid():
            ad = form.save()
            return redirect('advertisement_detail', pk=ad.pk)
    else:
        form = AdvertisementForm(instance=ad)

    return render(request, 'ad_board/edit_advertisement.html', {'form': form, 'ad': ad})

@login_required
def delete_advertisement(request, pk):
    # Удаление объявления
    ad = get_object_or_404(Advertisement, pk=pk)

    if request.user != ad.author:
        raise Http404("У вас нет прав на удаление этого объявления")

    if request.method == 'POST':
        ad.delete()
        return redirect('advertisement_list')

    return render(request, 'ad_board/delete_advertisement.html', {'ad': ad})

@login_required
def create_comment(request, pk):
    # Создание нового комментария к объявлению
    ad = get_object_or_404(Advertisement, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.advertisement = ad
            comment.author = request.user
            comment.save()
            return redirect('advertisement_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'ad_board/create_comment.html', {'form': form, 'ad': ad})

@login_required
def delete_comment(request, pk):
    # Удаление комментария
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        raise Http404("У вас нет прав на удаление этого комментария")

    ad_pk = comment.advertisement.pk
    comment.delete()

    return redirect('advertisement_detail', pk=ad_pk)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('advertisement_list')
    else:
        form = UserCreationForm()

    return render(request, 'ad_board/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('advertisement_list')
    else:
        form = AuthenticationForm()

    return render(request, 'ad_board/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('advertisement_list')
