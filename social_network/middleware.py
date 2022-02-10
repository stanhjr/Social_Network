import datetime
from django.utils import timezone
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken


class LastActionMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if not request.path.startswith('/activity/'):
                request.user = authentication.JWTAuthentication().authenticate(request)[0]
                request.user.last_action = datetime.datetime.now(tz=timezone.utc)
                request.user.save()
        except TypeError as e:
            print(e)
        except InvalidToken:
            return None
