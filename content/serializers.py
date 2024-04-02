from rest_framework import serializers
from .models import Video, VideoLike, VideoComment


class VideoSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    video_like_count = serializers.SerializerMethodField("get_video_like_count")
    video_comment_count = serializers.SerializerMethodField("get_video_comment_count")
    video_me_like = serializers.SerializerMethodField("get_video_me_like")

    class Meta:
        model = Video
        fields = (
            'uuid',
            'create_at',
            'title',
            'author',
            'file',
            'video_like_count',
            'views_count',
            'video_comment_count',
            'video_me_like'
        )
        fields = '__all__'

    @staticmethod
    def get_video_like_count(obj):
        return obj.video_likes.count()

    @staticmethod
    def get_video_comment_count(obj):
        return obj.video_comments

    def get_video_me_like(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            try:

                like = VideoLike.objects.get(video=obj, user=request.user)
                if like.dislike:
                    return -1
                else:
                    return 1
            except VideoLike.DoesNotExist:
                return 0
        else:
            return 0


class LikeSerializer(serializers.ModelSerializer):
    video_id = serializers.UUIDField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = VideoLike
        fields = ('video_id', 'user_id', 'dislike')

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        video_id = validated_data.pop('video_id')

        video = Video.objects.get(uuid=video_id)

        video_like = VideoLike.objects.create(user_id=user_id, video=video, **validated_data)
        return video_like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = '__all__'
