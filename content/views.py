# from .models import Video, VideoLike, VideoComment
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from content.serializers import VideoSerializer, LikeSerializer, CommentSerializer
from base.custom_pagination import CustomPaginator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from content.models import Video, VideoLike, VideoComment


class VideoListView(ListAPIView):
    queryset = Video.objects.all()
    pagination_class = CustomPaginator
    serializer_class = VideoSerializer
    permission_classes = (AllowAny,)


class VideoCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.user_chanel)


class VideoRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_object(self):
        return Video.objects.get(pk=self.kwargs['pk'], author=self.request.user.user_chanel)


class VideoUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_object(self):
        return Video.objects.get(pk=self.kwargs['pk'], author=self.request.user.user_chanel)


class VideoDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_object(self):
        return Video.objects.get(pk=self.kwargs['pk'], author=self.request.user.user_chanel)


class LikeView(ModelViewSet):
    queryset = VideoLike.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return VideoLike.objects.filter(user=self.request.user)


class CommentViewSet(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]
    model = VideoComment

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

            data = {
                "status": True,
                'message': 'Comment is created'
            }
            return Response(data)

    def get(self, request):
        obj=VideoComment.objects.filter(video__uuid=request.data['video'])
        serializer= self.serializer_class(instance=obj, many=True)

        data={
            "status": True,
            "data" : serializer.data
        }

        return Response(data)
