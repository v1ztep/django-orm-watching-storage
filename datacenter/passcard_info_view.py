from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from .models import get_duration, format_duration, is_visit_long
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = Passcard.objects.get(passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)
    for visit in passcard_visits:
        visit_entered_time = localtime(visit.entered_at)
        duration_inside = format_duration(get_duration(visit))
        is_strange = is_visit_long(visit)

        visit = {
            "entered_at": visit_entered_time,
            "duration": duration_inside,
            "is_strange": is_strange
        }

        this_passcard_visits.append(visit)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
