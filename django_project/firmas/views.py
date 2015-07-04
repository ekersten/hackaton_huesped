import urllib, cStringIO
from random import randint


from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout

from django.conf import settings

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from core.models import Signature
from core.models import Client

# Create your views here.
def home(request):
	context = {}
	return render(request, 'firmas/index.html', context)

def firma(request):
	context = {}
	context['staticroot'] = settings.STATIC_ROOT
	if request.user.is_authenticated:
		context['fb_uid'] = request.user.social_auth.get(provider='facebook').uid
	return render(request, 'firmas/subeFirma.html', context)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    context = {}
    return render(request, 'firmas/index.html', context)

def signature(request, signature_id):
	signature_obj = Signature.objects.get(pk=signature_id)

	firma = Image.new('RGB', (290, 130), 'white')
	response = HttpResponse(content_type='image/png')

	draw = ImageDraw.Draw(firma)
	font_line1 = ImageFont.truetype("/home/django/django_project/firmas/static/firmas/lato-bold.ttf", 14)
	font_extra_lines = ImageFont.truetype("/home/django/django_project/firmas/static/firmas/lato-regular.ttf", 12)
	
	draw.text((91, 10),signature_obj.user.get_full_name(),(0,0,0),font=font_line1)
	draw.text((91, 25),signature_obj.line1,(0,0,0),font=font_extra_lines)
	draw.text((91, 40),signature_obj.line2,(0,0,0),font=font_extra_lines)
	draw.text((91, 55),signature_obj.line3,(0,0,0),font=font_extra_lines)

	# open image from url
	avatar_url = 'http://graph.facebook.com/' + signature_obj.user.social_auth.get(provider='facebook').uid + '/picture?type=large'

	# http://graph.facebook.com/10206742313654411/picture?type=large

	avatar = cStringIO.StringIO(urllib.urlopen(avatar_url).read())
	avatar_img = Image.open(avatar)
	avatar_img = avatar_img.resize((71,71))

	firma.paste(avatar_img, (10,10))

	# insertar marca
	marca = Client.objects.all()[randint(0, Client.objects.all().count() - 1)]
	marca_img = Image.open(marca.logo)
	marca_img = marca_img.resize((200, 40))
	firma.paste(marca_img, (10, 87))

	# insertar logo fundacion
	logo_img = Image.open('/home/django/django_project/firmas/static/firmas/logo_firma.png')
	firma.paste(logo_img, (220, 60))

	firma.save(response, "PNG")
	return response

def save_signature(request):
	Signature.objects.filter(user=request.user).delete()
	sig = Signature()
	sig.line1 = request.POST.get('line1', '')
	sig.line2 = request.POST.get('line2', '')
	sig.line3 = request.POST.get('line3', '')
	sig.line4 = request.POST.get('line4', '')
	sig.user = request.user

	sig.save()

	response = 'http://104.131.8.22/firma/' + str(sig.id) + '/'
	return HttpResponse(response)