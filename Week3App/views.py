from django.shortcuts import render_to_response
from django.template import RequestContext
from url_parser import parse

def home(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def result(request):
    url = request.POST['url_input']
    result = parse(url)
    return render_to_response('result.html', {'result':result}, context_instance=RequestContext(request))
    
