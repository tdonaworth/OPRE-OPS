from django.shortcuts import render
from django.http import HttpResponse
import datetime

from django.views.generic import ListView
from django.views.generic import DetailView
from ops_site.models import CommonAccountingNumber

def home(request):
    html = "<html><body><h1>OPRE OPS</h1><a href='cans'>List CANs</a></body></html>"
    return HttpResponse(html)


class CANInfoListView(ListView):
    model = CommonAccountingNumber

class CANInfoDetailView(DetailView):

    queryset = CommonAccountingNumber.objects.all()

    def get_object(self):
        obj = super().get_object()
        return obj
