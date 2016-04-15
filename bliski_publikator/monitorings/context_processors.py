from .models import Monitoring


def get_full_monitoring(request):
    object_list = Monitoring.objects.all()
    active = []
    nonactive = []
    for obj in object_list:
        if obj.active and len(active) < 3:
            active.append(obj)
        else:
            nonactive.append(obj)
    return {'monitoring_full_list': {'active': active, 'nonactive': nonactive}}
