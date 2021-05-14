from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from blog.models import Article
from mysite.forms import UserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail
import os

from django.contrib.sitemaps import ping_google

@login_required
def ping(request):
	try:
		if request.user.is_admin:
			ping_google()
	except:
		pass
	return redirect('/')

def index(request):
	ranks = Article.objects.order_by('-count')[:2]
	objs = Article.objects.all()[:3]
	context = {
		'title': 'Really Site',
		'articles': objs,
		'ranks': ranks,
	}
	return render(request, 'mysite/index.html', context)

class Login(LoginView):
	template_name = 'mysite/auth.html'

	def form_valid(self, form):
		messages.success(self.request, 'やったね！ログイン成功だよ！')
		return super().form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'エラー発生してもうてるけども！！！')
		return super().form_invalid(form)

def signup(request):
	context = {}
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			login(request, user)
			messages.success(request, '登録完了してもうたけど!!')
			return redirect('/')
	return render(request, 'mysite/auth.html', context)

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class MypageView(LoginRequiredMixin, View):
	context = {}

	def get(self, request):
		return render(request, 'mysite/mypage.html', self.context)

	def post(self, request):
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			profile.save()
			messages.success(request, '更新完了してもうたけど!!')
		return render(request, 'mysite/mypage.html', self.context)
"""
@login_required
def mypage(request):
	context = {}
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			profile.save()
			messages.success(request, '更新完了してもうたけど!!')
	return render(request, 'mysite/mypage.html', context)
"""

class ContactView(View):
	context = {
		'grecaptcha_sitekey': os.environ['GRECAPTCHA_SITEKEY'],
	}

	def get(self, request):
		return render(request, 'mysite/contact.html', self.context)

	def post(self, request):
		recaptcha_token = request.POST.get("g-recaptcha-response")
		res = grecaptcha_request(recaptcha_token)
		if not res:
			messages.error(request, 'reCAPTCHAに失敗したようです。')
			return render(request, 'mysite/contact.html', context)
		messages.success(request, 'お問い合わせ受理しました！！')
		return render(request, 'mysite/contact.html', self.context)

'''
def contact(request):
	context = {
		'grecaptcha_sitekey': os.environ['GRECAPTCHA_SITEKEY'],
	}
	if request.method == "POST":
		recaptcha_token = request.POST.get("g-recaptcha-response")
		res = grecaptcha_request(recaptcha_token)
		if not res:
			messages.error(request, 'reCAPTCHAに失敗したようです。')
			return render(request, 'mysite/contact.html', context)
		messages.success(request, 'お問い合わせ受理しました！！')

	return render(request, 'mysite/contact.html', context)
'''
def grecaptcha_request(token):
    from urllib import request, parse
    import json, ssl
 
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
 
    url = "https://www.google.com/recaptcha/api/siteverify"
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    data = {
        'secret': os.environ['GRECAPTCHA_SECRETKEY'],
        'response': token,
    }
    data = parse.urlencode(data).encode()
    req = request.Request(
        url,
        method="POST",
        headers=headers,
        data=data,
    )
    f = request.urlopen(req, context=context)
    response = json.loads(f.read())
    f.close()
    return response['success']

import payjp

class PayView(View):
	payjp.api_key = os.environ['PAYJP_SECRET_KEY']
	public_key = os.environ['PAYJP_PUBLIC_KEY']
	amount = 1000

	def get(self, request):
		context = {
			'amount': self.amount,
			'public_key': self.public_key,
		}
		return render(request, 'mysite/pay.html', context)
	
	def post(self, request):
		customer = payjp.Customer.create(
			email='example@pay.jp',
			card=request.POST.get('payjp-token')
		)
		charge = payjp.Charge.create(
			amount=self.amount,
			currency='jpy',
			customer=customer.id,
			description='支払いテスト'
		)
		context = {
			'amount': self.amount,
			'public_key': self.public_key,
			'charge': charge,
		}
		return render(request, 'mysite/pay.html', context)