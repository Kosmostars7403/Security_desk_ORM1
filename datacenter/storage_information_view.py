from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import format_duration


def storage_information_view(request):
    non_closed_visits = []

    visits_at_storage = Visit.objects.filter(leaved_at=None)

    for visit in visits_at_storage:
        duration = visit.get_duration()
        visit = {"who_entered": visit.passcard.owner_name,
                 "entered_at": visit.entered_at,
                 "duration": format_duration(duration),
                 "is_strange": visit.is_visit_long}
        non_closed_visits.append(visit)

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
