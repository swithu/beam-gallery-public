from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic import DetailView, DeleteView, FormView
from django.urls import reverse_lazy
from .forms import PhotoPostForm, ContactForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import PhotoPost
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Q
from dotenv import load_dotenv
import os

load_dotenv()

class CoverView(TemplateView):
    template_name = 'cover.html'


class IndexView(ListView):
    template_name = 'index.html'
    queryset = PhotoPost.objects.order_by('-posted_at')
    paginate_by = 9


@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    form_class = PhotoPostForm
    template_name = "post_photo.html"
    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)


class PostSuccessView(TemplateView):
    template_name = 'post_success.html'


class CategoryView(ListView):
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = PhotoPost.objects.filter(
            category=category_id
        ).order_by('-posted_at')
        return categories


class TagView(ListView):
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        tag_id = self.kwargs['tag']
        tags = PhotoPost.objects.filter(
            Q(tag1=tag_id) | Q(tag2=tag_id) | Q(tag3=tag_id)
            | Q(tag4=tag_id)| Q(tag5=tag_id)
        ).order_by('-posted_at')
        return tags
    

class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = PhotoPost.objects.filter(
            user=user_id
        ).order_by('-posted_at')
        return user_list


class DetailView(DetailView):
    template_name = 'detail.html'
    model = PhotoPost


class MypageView(ListView):
    template_name = 'mypage.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = PhotoPost.objects.filter(
            user=self.request.user
        ).order_by('-posted_at')
        return queryset


class PhotoDeleteView(DeleteView):
    model = PhotoPost
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('photo:mypage')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('photo:contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        subject = 'お問い合わせ：{}'.format(title)
        message = \
            '送信者名：{0}\n メールアドレス：{1}\n タイトル：{2}\n メッセージ：\n{3}' \
            .format(name, email, title, message)
        
        from_email = os.environ.get('EMAIL_USER')
        to_list = os.environ.get('EMAIL_USER')
        
        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=[to_list],
                               )
        message.send()
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。'
        )
        return super().form_valid(form)