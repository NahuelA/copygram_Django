""" Logout from users app. """

# Django
from .__modules__ import *


class LogoutView(APIView):
    """Delete access, sessionid and csrf cookies"""

    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "head", "options"]

    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)

        if request.COOKIES.get("access_token") != None:
            response.delete_cookie("access_token", "/")
            response.delete_cookie("csrftoken", "/")
            response.delete_cookie("sessionid", "/")

        return response
