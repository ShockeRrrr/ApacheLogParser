from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum, Count
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from LogParser.models import LogEntry

@csrf_exempt
def main_dashboard(request):
    query = request.GET.get('search')
    data = LogEntry.objects.all().order_by('id') if not query \
        else LogEntry.objects.filter(Q(ip__icontains=query) | Q(date__icontains=query) |
                                     Q(method__icontains=query) | Q(status_code__icontains=query) |
                                     Q(user_agent__icontains=query) | Q(referrer__icontains=query) |
                                     Q(request_path__icontains=query)).order_by('id')

    page = request.GET.get('page', 1)
    context = main_page_data(page, data)
    return render(request, 'index.html', context)


def main_page_data(page, data):
        paginator = Paginator(data, 10)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return {
            'data': posts,
            'ip_count': data.values('ip').annotate(name_count=Count('ip')).order_by('-name_count')[:10],
            'method_count': data.values('method').annotate(name_count=Count('method')).order_by('-name_count'),
            'response_size': data.aggregate(Sum('response_size'))['response_size__sum'] or 0
        }
