from .models import AccessLog
from django.utils.deprecation import MiddlewareMixin

class UserVisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            AccessLog.objects.create(
                user=request.user,
                ip_address=self.get_client_ip(request)
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
