from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render

from django.utils.timezone import localtime
from .models import get_duration, format_duration

def storage_information_view(request):
    non_closed_visits = []
    active_visits = Visit.objects.filter(leaved_at=None)
    for visitor in active_visits:
        visitor_name = visitor.passcard.owner_name
        visitor_entered_time = localtime(visitor.entered_at)
        duration_inside = format_duration(get_duration(visitor_entered_time))

        non_closed_visitor = {
            "who_entered": visitor_name,
            "entered_at": visitor_entered_time,
            "duration": duration_inside,
        }

        non_closed_visits.append(non_closed_visitor)


    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
