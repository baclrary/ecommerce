from django.urls import path
from .views import ReviewCreateView, LikeReviewView, DislikeReviewView, ReplyCreateView

urlpatterns = [
    path('create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:object_id>/like/', LikeReviewView.as_view(), name='like-review'),
    path('<int:object_id>/dislike/', DislikeReviewView.as_view(), name='dislike-review'),
    path('create-reply/<int:review_id>/', ReplyCreateView.as_view(), name='reply-create'),
    path('create-reply/<int:review_id>/<int:parent_reply_id>/', ReplyCreateView.as_view(),
         name='reply-to-reply-create'),

]
