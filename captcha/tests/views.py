from django import forms
from captcha.fields import CaptchaField
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.models import User


TEST_TEMPLATE = r'''
{% load url from future %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8">
        <title>captcha test</title>
    </head>
    <body>
        {% if passed %}
        <p style="color:green">Form validated</p>
        {% endif %}
        <form action="{% url 'captcha-test' %}" method="post">
            {{form.as_p}}
            <p><input type="submit" value="Continue &rarr;"></p>
        </form>
    </body>
</html>
'''


def test(request):

    class CaptchaTestForm(forms.Form):
        subject = forms.CharField(max_length=100)
        sender = forms.EmailField()
        captcha = CaptchaField(help_text='asdasd')

    passed = False
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            passed = True
    else:
        form = CaptchaTestForm()

    t = loader.get_template_from_string(TEST_TEMPLATE)
    return HttpResponse(t.render(RequestContext(request, dict(passed=passed, form=form))))


def test_model_form(request):
    class CaptchaTestModelForm(forms.ModelForm):
        subject = forms.CharField(max_length=100)
        sender = forms.EmailField()
        captcha = CaptchaField(help_text='asdasd')

        class Meta:
            model = User
            fields = ('subject', 'sender', 'captcha', )

    passed = False
    if request.POST:
        form = CaptchaTestModelForm(request.POST)
        if form.is_valid():
            passed = True
    else:
        form = CaptchaTestModelForm()

    t = loader.get_template_from_string(TEST_TEMPLATE)
    return HttpResponse(t.render(RequestContext(request, dict(passed=passed, form=form))))


def test_custom_error_message(request):

    class CaptchaTestForm(forms.Form):
        captcha = CaptchaField(help_text='asdasd', error_messages=dict(invalid='TEST CUSTOM ERROR MESSAGE'))

    passed = False
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            passed = True
    else:
        form = CaptchaTestForm()

    t = loader.get_template_from_string(TEST_TEMPLATE)
    return HttpResponse(t.render(RequestContext(request, dict(passed=passed, form=form))))


def test_per_form_format(request):

    class CaptchaTestForm(forms.Form):
        captcha = CaptchaField(help_text='asdasd', error_messages=dict(invalid='TEST CUSTOM ERROR MESSAGE'),
                               output_format=u'%(image)s testPerFieldCustomFormatString %(hidden_field)s %(text_field)s')
    passed = False
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            passed = True
    else:
        form = CaptchaTestForm()

    t = loader.get_template_from_string(TEST_TEMPLATE)
    return HttpResponse(t.render(RequestContext(request, dict(passed=passed, form=form))))
