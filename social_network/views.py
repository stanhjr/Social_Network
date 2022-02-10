from rest_framework import permissions, viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .tools import add_like, remove_like, get_fans, get_total_likes_or_data_range
from .models import MyUser, Post
from .serializers import SignUpSerializer, PostSerializer, FanSerializer, DateSerializer


class LikedMixin:
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        creates a like for a post from a user
        """
        obj = self.get_object()
        add_like(obj, request.user)

        return Response({'post_id': obj.id, 'action': 'like'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """
        delete a like for a post from a user
        """
        obj = self.get_object()
        remove_like(obj, request.user)

        return Response({'post_id': obj.id, 'action': 'unlike'}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def get_fans(self, request, pk=None):
        """
        get all users who liked this post
        """
        obj = self.get_object()
        fans = get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)


class SignUp(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Sign up access',
                         'username': response.data.get('username')},
                        status=status.HTTP_201_CREATED)


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        """
        only the author of the post or the admin can delete a post
        """
        serializer = self.get_serializer(self.get_object())
        author_id = serializer.data.get('author').get('id')
        user = self.request.user
        if user.id == author_id or user.is_superuser:
            super().destroy(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        raise serializers.ValidationError(
            {"detail": "You do not have permission to perform this action or you did not create this post"})

    def update(self, request, *args, **kwargs):
        """
        only the author of the post can update a post
        """
        serializer = self.get_serializer(self.get_object())
        author_id = serializer.data.get('author').get('id')
        user = self.request.user
        if user.id == author_id:
            super().update(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK)

        raise serializers.ValidationError(
            {"detail": "you did not create this post"})

    def partial_update(self, request, *args, **kwargs):
        """
        only the author of the post can partial update a post
        """
        serializer = self.get_serializer(self.get_object())
        author_id = serializer.data.get('author').get('id')
        user = self.request.user
        if user.id == author_id:
            super().partial_update(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK)

        raise serializers.ValidationError(
            {"detail": "you did not create this post"})


class UserActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        user activity an endpoint which will show when user
        was login last time and when he made a last request to the service
        """
        last_login = request.user.last_login.strftime('%Y-%m-%d %H:%M:%S')
        last_action = request.user.last_action.strftime('%Y-%m-%d %H:%M:%S')
        username = request.user.username

        return Response({'username': username,
                         'last_login': last_login,
                         'last_action': last_action})


class AnaliticsView(APIView):

    def get(self, request):
        """
        analytics about how many likes were made.
        example url /api/analytics/?date_from=2020-02-02&date_to=2020-02-15
        return analytics aggregated by day.
        """
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        serializer = DateSerializer(data={'date_from': date_from, 'date_to': date_to})
        if serializer.is_valid():
            date_from = serializer.data.get('date_from')
            date_to = serializer.data.get('date_to')

            return Response({"total_likes": get_total_likes_or_data_range(date_from, date_to)})

        return Response(serializer.errors)
