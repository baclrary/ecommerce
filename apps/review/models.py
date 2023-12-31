from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from catalog.models import Product
from .permissions import review_permissions


__all__ = ['BaseUserInteractionModel', 'BaseReviewModel', 'Reactable', 'Review', 'Reply', 'Reaction', 'Media']


class BaseUserInteractionModel(models.Model):
    """
    Abstract base model for common user interaction attributes
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='%(class)s_created',
                             related_query_name='%(class)s')
    created_at = models.DateTimeField(auto_now_add=True)
    hidden_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                  related_name='hidden_%(class)ss',
                                  null=True, blank=True)
    approved_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                    related_name='approved_%(class)ss',
                                    null=True, blank=True)

    class Meta:
        abstract = True


class BaseReviewModel(models.Model):
    """
    Abstract base model for common review attributes
    """
    is_hidden = models.BooleanField(default=False, blank=True)
    hidden_at = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Reactable(models.Model):
    """
    Abstract model for entities that can be reacted to (like, dislike)
    """
    class Meta:
        abstract = True

    def get_reactions_counts(self):
        reactions_counts = {
            'likes': self.reactions.filter(reaction='like').count(),
            'dislikes': self.reactions.filter(reaction='dislike').count(),
        }
        return reactions_counts

    def get_user_reaction(self, user):
        """
        Returns the reaction ('like', 'dislike', or None) given by the user to this reply.
        """
        reaction = self.reactions.filter(user=user).first()
        return reaction.reaction if reaction else None


    #
    # def remove_user_reaction(self, user):
    #     """
    #     Removes the reaction given by the user to this review.
    #     """
    #     try:
    #         self.reactions.get(user=user).delete()
    #     except Reaction.DoesNotExist:
    #         pass


class Review(BaseReviewModel, BaseUserInteractionModel, Reactable):
    """
    Model representing a product review
    """
    RATING_CHOICES = [
        (1, '1 - Terrible'),
        (2, '2 - Bad'),
        (3, '3 - Okay'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    review_text = models.TextField()

    class Meta:
        permissions = review_permissions

    def __str__(self):
        return f'"{self.title}" for "{self.product.title}" by {self.user.email}'

    @classmethod
    def get_user_total_reviews_count(cls, user):
        """
        Method to get total review count for a given user
        """
        return cls.objects.filter(user=user).count()


class Reply(BaseReviewModel, BaseUserInteractionModel, Reactable):
    """
    Model representing a reply to a product review or another reply
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='replies_to_review', null=True, blank=True)
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE,
                                     related_name='replies_to_reply', null=True, blank=True)
    reply_text = models.TextField()

    def __str__(self):
        if self.review:
            return f"Review: {self.review.title} - Reply: {self.reply_text}"
        elif self.parent_reply:
            return f"Parent Reply ID: {self.parent_reply.id} - Reply: {self.reply_text}"
        else:
            return f"Reply ID: {self.id} - Reply: {self.reply_text}"

    def save(self, *args, **kwargs):
        if not any([self.review, self.parent_reply]):
            raise ValidationError('Either review or parent_reply must be set.')
        if all([self.review, self.parent_reply]):
            raise ValidationError('Either review or parent_reply must be set, not both.')
        super().save(*args, **kwargs)





class Reaction(models.Model):
    REACTION_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.ForeignKey(Review, related_name='reactions',
                               on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(Reply, related_name='reactions',
                              on_delete=models.CASCADE, null=True, blank=True)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('user', 'review', 'reply')
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(review__isnull=False, reply__isnull=True) |
                    models.Q(review__isnull=True, reply__isnull=False)
                ),
                name='reaction_must_have_either_review_or_reply',
            ),
        ]

    def clean(self):
        super().clean()

        if all([self.review, self.reply]):
            raise ValidationError('A reaction can only be associated with a review or a reply, not both.')
        if not any([self.review, self.reply]):
            raise ValidationError('A reaction must be associated with either a review or a reply.')


class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='reviews/files/')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return f'{self.media_type} for "{self.review.title}"'
