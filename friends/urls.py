from django.urls import path
from friends.views import (
    UserListCreateView,
    FriendshipCreateView,
    update_friendship_status,
    FriendshipRequestsSentListAPIView,
    FriendshipRequestsReceivedListAPIView,
    FriendListAPIView,
    friendship_status,
    remove_friend
)

urlpatterns = [
    path('register/', UserListCreateView.as_view(), name='register'),
    path('friendship/create/', FriendshipCreateView.as_view(), name='send_friend_request'),
    path('friendship-request/', update_friendship_status),
    path('friendship_requests_sent/<int:user_id>/', FriendshipRequestsSentListAPIView.as_view()),
    path('friendship_requests_received/<int:user_id>/', FriendshipRequestsReceivedListAPIView.as_view()),
    path('friend_list/<int:user_id>/', FriendListAPIView.as_view(), name='friend_list'),
    path('friendship_status/', friendship_status, name='friendship_status'),
    path('remove-friend/', remove_friend, name='remove_friend'),
]