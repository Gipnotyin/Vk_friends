from rest_framework import serializers, generics
from rest_framework.response import Response

from .models import User, Friendship


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class FriendshipSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'created_at', 'status']
        read_only_fields = ['id', 'created_at']


class FriendshipUpdateView(generics.UpdateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
