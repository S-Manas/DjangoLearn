from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if request.path.startswith('/admin/') and not request.user.is_staff_member:
            return redirect(reverse('home'))  # Redirect to home if not staff

        return self.get_response(request)
