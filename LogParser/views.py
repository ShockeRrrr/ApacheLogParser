from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'POST':
        f = request.FILES['file'].read()
        txt = str(f.decode('utf-8'))
        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        ips = re.findall(pattern, txt)
        return render(request, 'index.html', ips)
    return render(request, 'index.html')
