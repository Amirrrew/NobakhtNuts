from django.utils import timezone

from adminpanel_module.models import ActiveUser


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.save()

        ActiveUser.objects.update_or_create(
            session_key=request.session.session_key,
            defaults={
                "user": request.user if request.user.is_authenticated else None,
                "last_seen": timezone.now()
            }
        )

        response = self.get_response(request)
        return response