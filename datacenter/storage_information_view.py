from datacenter.models import Visit
from django.shortcuts import render

from django.utils.timezone import localtime
from .models import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    non_closed_visits = []
    active_visits = Visit.objects.filter(leaved_at=None)
    for visit in active_visits:
        visit_name = visit.passcard.owner_name
        visit_entered_time = localtime(visit.entered_at)
        duration_inside = format_duration(get_duration(visit))
        is_strange = is_visit_long(visit)

        non_closed_visitor = {
            "who_entered": visit_name,
            "entered_at": visit_entered_time,
            "duration": duration_inside,
            "is_strange": is_strange
        }

        non_closed_visits.append(non_closed_visitor)

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
