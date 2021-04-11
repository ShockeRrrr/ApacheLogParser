from django.shortcuts import render
from .forms import LogEntry
import re

def index(request):
    if request.method == 'POST':
        f = request.FILES['file'].read()
        txt = str(f.decode('utf-8'))
        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        ips = re.findall(pattern, txt)
        ips = {'ips':ips}

        return render(request, 'index.html', ips)
    else:
        return render(request, 'index.html')

