from .models import Monitoring


def get_full_monitoring(request):
    return {'monitoring_full_list': Monitoring.objects.all()}
