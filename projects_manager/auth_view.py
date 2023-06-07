from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
        })

    @staticmethod
    def get(request, *args, **kwargs):

        try:
            token_value = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            token = Token.objects.get(key=token_value)
            user = token.user

            return Response({
                'user_id': user.id,
            })
        except IndexError:
            return Response({'detail': 'Authorization error'}, status=401)

    @staticmethod
    def delete(request, *args, **kwargs):

        try:
            token_value = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            token = Token.objects.get(key=token_value)
            token.delete()
            return Response({'message': 'Logout successful'}, status=200)

        except IndexError:
            return Response({'detail': 'Authorization error'}, status=401)
