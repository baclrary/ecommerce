from django.contrib import admin
from .models import Review, Reply, Reaction, Media


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'product', 'user', 'rating', 'created_at', 'is_hidden', 'is_approved']
    search_fields = ['title', 'product__title', 'user__email', 'review_text']
    list_filter = ['rating', 'is_hidden', 'is_approved', 'created_at']
    raw_id_fields = ['product', 'user', 'hidden_by', 'approved_by']
    date_hierarchy = 'created_at'


admin.site.register(Review, ReviewAdmin)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'reply_text', 'review', 'user', 'created_at', 'is_hidden', 'is_approved']
    search_fields = ['reply_text', 'review__title', 'user__email']
    list_filter = ['is_hidden', 'is_approved', 'created_at']
    raw_id_fields = ['review', 'user', 'hidden_by', 'approved_by']
    date_hierarchy = 'created_at'


admin.site.register(Reply, ReplyAdmin)


class ReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'reply', 'reaction']
    search_fields = ['user__email', 'review__title', 'reply__reply_text']
    list_filter = ['reaction']
    raw_id_fields = ['user', 'review', 'reply']


admin.site.register(Reaction, ReactionAdmin)


class MediaAdmin(admin.ModelAdmin):
    list_display = ['review', 'media_type']
    search_fields = ['review__title']
    list_filter = ['media_type']
    raw_id_fields = ['review']


admin.site.register(Media, MediaAdmin)
