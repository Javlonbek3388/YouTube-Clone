from django.contrib import admin
from content.models import Video, VideoLike, VideoComment, Channel, HistoryView, CommentLike
# Register your models here.


class VideoId(admin.ModelAdmin):
    list_display = ['uuid', 'title']


class CommentId(admin.ModelAdmin):
    list_display = ['uuid', 'comment']


admin.site.register(Video, VideoId)
admin.site.register(VideoLike)
admin.site.register(VideoComment, CommentId)
admin.site.register(Channel)
admin.site.register(HistoryView)
admin.site.register(CommentLike)
