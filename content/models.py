from django.db import models
from accounts.models import User
from base.models import BaseModelContent
from django.core.validators import FileExtensionValidator


class Channel(BaseModelContent):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    banner = models.ImageField(null=True, blank=True, upload_to='banner/')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatar/')
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='user_chanel')
    follower = models.ManyToManyField(User, related_name='user_follower', blank=True)

    def __str__(self):
        return self.name


class HashTags(BaseModelContent):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Video(BaseModelContent):
    author = models.ForeignKey(Channel, related_name='video_author', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='title')
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='videos/', validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv', 'mpeg4'])
    ])
    tag = models.ManyToManyField(HashTags, related_name='video_tag', blank=True)
    views_counts = models.BigIntegerField(default=0)
    video_comments = models.TextField()
    #
    # def __str__(self):
    #     return self.title


class VideoLike(BaseModelContent):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_likes')
    dislike = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return self.user.username


class HistoryView(BaseModelContent):
    user = models.ForeignKey(User, related_name='history_user', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='history_video', on_delete=models.CASCADE, verbose_name='VideoLike')
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class VideoComment(BaseModelContent):
    user = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE, blank=True)
    video = models.ForeignKey(Video, related_name='user_video', on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.comment


class CommentLike(BaseModelContent):
    user = models.ForeignKey(User, related_name='user_comment_like', on_delete=models.CASCADE)
    comment = models.ForeignKey(VideoComment, related_name='like_comment', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
