from datetime import datetime
from django.http import (
    Http404,
    HttpResponse,
    JsonResponse,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import EventIndexPage

def today_message_get_calendar_events(request):
    """
    JSON list of events compatible with fullcalendar.js
    """
    # Parse input.
    try:
        page_id = request.GET["pid"]
    except KeyError:
        return HttpResponse("pid required", status=400)

    start = None
    end = None
    start_str = request.GET.get("start", None)
    end_str = request.GET.get("end", None)
    try:
        if start_str:
            start = timezone.make_aware(
                datetime.strptime(start_str[:10], "%Y-%m-%d"),
            )
        if end_str:
            end = timezone.make_aware(
                datetime.strptime(end_str[:10], "%Y-%m-%d"),
            )
    except ValueError:
        return HttpResponse(
            "start and end must be valid datetimes.", status=400
        )

    # Get the page.
    try:
        page = EventIndexPage.objects.get(pk=page_id).specific
    except (EventIndexPage.DoesNotExist, ValueError):
        raise Http404("Page does not exist")

    return JsonResponse(
        page.get_calendar_events(start=start, end=end), safe=False
    )

