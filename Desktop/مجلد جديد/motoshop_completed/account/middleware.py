from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve, Resolver404


class RedirectAuthenticatedUsersMiddleware:
    """Keep authenticated users away from guest-only auth pages.

    This protects both normal clicks and manual URL entry for login/register.
    """

    guest_only_url_names = {'login', 'register'}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                match = resolve(request.path_info)
            except Resolver404:
                match = None

            if match and match.url_name in self.guest_only_url_names:
                messages.info(request, 'أنت مسجل الدخول بالفعل.')
                return redirect('home')

        return self.get_response(request)
