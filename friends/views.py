from django.db import models
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import User, Friendship
from .serializers import UserSerializer, FriendshipSerializer


#Добавить нового пользователя
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#отправить заявку в друзья
class FriendshipCreateView(generics.CreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        friend_id = self.request.data.get('friend_id')
        if user_id and friend_id:
            if user_id == friend_id:
                raise ValidationError("You can't send the request yourself.")
            friendship_to = Friendship.objects.filter(from_user=friend_id, to_user=user_id, status='pending').first()
            friendship = Friendship.objects.filter(from_user=user_id, to_user=friend_id).first()
            if not friendship:
                friendship = serializer.save(from_user_id=user_id, to_user_id=friend_id, status='pending')
            print(friendship)
            if friendship and friendship_to and friendship.status == 'pending' and friendship_to.status == 'pending':
                friendship.status = 'accepted'
                friendship_to.status = 'accepted'
                friendship.save()
                friendship_to.save()
                return Response({'status': 'accepted'}, status=status.HTTP_400_BAD_REQUEST)
            if friendship and friendship.status == 'accepted':
                raise ValidationError('These users are already friends')
        else:
            raise ValidationError('Both user_id and friend_id are required')


#Принять/отклонить пользователя в друзья
@api_view(['POST'])
def update_friendship_status(request):
    from_user_id = request.data.get('from_user')
    to_user_id = request.data.get('to_user')
    if from_user_id == to_user_id:
        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
    action = request.data.get('action')
    print(from_user_id, to_user_id)
    friendship = Friendship.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id, status='pending').first()
    friendship_to = Friendship.objects.filter(from_user_id=to_user_id, to_user_id=from_user_id)
    print(friendship)
    if not friendship:
        return Response({'error': 'Friendship not found.'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'accept' and friendship.status != 'accepted':
        friendship.status = 'accepted'
        friendship.save()
        if friendship_to:
            friendship_to.status = 'accepted'
            friendship_to.save()
        else:
            obj = Friendship(from_user_id=to_user_id, to_user_id=from_user_id, status='accepted')
            obj.save()
        return Response({'friendship_status': 'accepted'})
    elif action == 'reject':
        friendship.status = 'rejected'
        friendship.save()
        return Response({'friendship_status': 'rejected'})
    else:
        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)


#исходящие заявки
class FriendshipRequestsSentListAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Friendship.objects.filter(from_user_id=user_id, status='pending')


#входящие заявки
class FriendshipRequestsReceivedListAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Friendship.objects.filter((models.Q(to_user_id=user_id) & models.Q(status='pending')) |
                                         (models.Q(status='rejected') & models.Q(to_user_id=user_id)))


#Просмотр друзей
class FriendListAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Friendship.objects.filter(from_user=user_id, status='accepted')


@api_view(['GET'])
def friendship_status(request):
    user_id = request.GET.get('user')
    friend_id = request.GET.get('friend')
    friendship_status = 'Нет ничего'
    if user_id == friend_id:
        return Response({'friendship_status': 'I love VK'})
    if user_id and friend_id:
        friendship = Friendship.objects.filter(
            (models.Q(from_user=user_id) & models.Q(to_user=friend_id)) |
            (models.Q(from_user=friend_id) & models.Q(to_user=user_id))
        ).first()
        if friendship:
            print(friendship.status, friendship.from_user_id, friendship.to_user_id)
            if friendship.status == 'accepted':
                friendship_status = 'Друзья'
            elif friendship.from_user_id == int(user_id):
                friendship_status = 'Исходящая заявка'
            elif friendship.from_user_id == int(friend_id):
                friendship_status = 'Входящая заявка'
    return Response({'friendship_status': friendship_status})


@api_view(['POST'])
def remove_friend(request):
    user_id = int(request.data.get('user'))
    friend_id = int(request.data.get('friend'))
    if user_id == friend_id:
        return Response({'success': False})
    if user_id and friend_id:
        friendship = Friendship.objects.filter(
            from_user=user_id,
            to_user=friend_id,
            status='accepted'
        ).first()
        friendship_to = Friendship.objects.filter(
            from_user=friend_id,
            to_user=user_id,
            status='accepted'
        ).first()
        if friendship and friendship_to:
            friendship.delete()
            friendship_to.status = 'pending'
            friendship_to.save()
            return Response({'success': True})
    return Response({'success': False})
