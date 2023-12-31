import json
import os
import tempfile

from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
# Import necessary Django modules
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Import local models and forms
from catalog.models import Product
from guardian.shortcuts import assign_perm
from .forms import ReviewForm, ReplyForm
from .models import Review, Media, Reaction, Reply

# Import moviepy for video conversion
from moviepy.editor import VideoFileClip


class ReviewCreateView(generic.View):
    form_class = ReviewForm  # Assign the ReviewForm as the form to be used

    @staticmethod
    def convert_to_mp4(file_path, output_path):
        """
        Converts any given video file to mp4 format while preserving audio

        :param file_path: Path to the video file to be converted
        :param output_path: Path where the converted file will be saved
        """
        clip = VideoFileClip(file_path)
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    def handle_uploaded_file(self, f, review):
        """
        Handle file uploads for a given review. Files are saved to Media model.

        :param f: File object
        :param review: Review object associated with the file
        """
        file_extension = os.path.splitext(f.name)[-1].lower()
        # If the uploaded file is a video
        if file_extension in ['.mp4', '.mkv', '.avi', '.webm']:
            media_type = 'video'
            # Create a temporary mp4 file
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
                for chunk in f.chunks():
                    temp_file.write(chunk)
                # If the original file isn't already mp4, convert it
                if file_extension != '.mp4':
                    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_output_file:
                        self.convert_to_mp4(temp_file.name, temp_output_file.name)
                        with open(temp_output_file.name, 'rb') as mp4_file:
                            content_file = ContentFile(mp4_file.read(), name=f"{os.path.splitext(f.name)[0]}.mp4")
                            Media.objects.create(review=review, file=content_file, media_type=media_type)
                else:
                    # If the original file is mp4, directly create a Media object
                    Media.objects.create(review=review, file=f, media_type=media_type)
        else:
            # Determine the media_type and create a Media object
            media_type = 'video' if f.content_type.startswith('video') else 'image'
            Media.objects.create(review=review, file=f, media_type=media_type)

    def post(self, request, *args, **kwargs):
        """
        Handle the POST method for review creation. This includes saving the review, handling file uploads,
        and setting permissions.

        :param request: HTTP request object
        :param args: Arguments passed to the view
        :param kwargs: Keyword arguments passed to the view
        :return: HTTP response object
        """
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.product = get_object_or_404(Product, id=request.POST.get('product'))
            new_review.save()

            for f in request.FILES.getlist('media_files'):
                self.handle_uploaded_file(f, new_review)

            assign_perm('change_review', request.user, new_review)
            assign_perm('delete_review', request.user, new_review)
            product_id = form.cleaned_data['product'].id
            category_slug = form.cleaned_data['product'].category.category.slug
            sub_category_slug = form.cleaned_data['product'].category.slug
            return HttpResponseRedirect(reverse('product-detail-view',
                                                kwargs={'product_id': product_id, 'category_slug': category_slug,
                                                        'sub_category_slug': sub_category_slug}))
        else:
            # Handle case when form data is invalid
            product_id = request.POST.get('product_id', None)
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                return HttpResponseRedirect(reverse('product-detail-view', kwargs={'product_id': product.id,
                                                                                   'category_slug': product.category.category.slug,
                                                                                   'sub_category_slug': product.category.slug}))
            else:
                return HttpResponse("Invalid form data", status=400)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ReactionView(generic.View):
    """
    Base class for LikeReviewView and DislikeReviewView. Provides common method for
    getting or creating a Reaction object.
    """
    http_method_names = ['post']

    def get_reaction(self, object_id, reaction_type):
        """
        Retrieve or create a Reaction object based on the object_id and reaction_type.
        :param object_id: id of the object to which the reaction is tied.
        :param reaction_type: string representing the type of reaction ('like' or 'dislike').
        :return: JsonResponse indicating the status of the operation.
        """
        model_name = self.request.POST.get('model_name')
        ModelClass = Review if model_name == 'review' else Reply

        obj = get_object_or_404(ModelClass, id=object_id)
        reaction, created = Reaction.objects.get_or_create(
            user=self.request.user,
            review=obj if model_name == 'review' else None,
            reply=obj if model_name == 'reply' else None,
            defaults={'reaction': reaction_type}
        )

        if not created and reaction.reaction == reaction_type:
            reaction.delete()  # Remove the reaction if it was already set
            # obj.remove_user_reaction(self.request.user)  # Remove the reaction if it was already set
            return JsonResponse({"status": f"{reaction_type}_removed"})

        if not created:
            reaction.reaction = reaction_type  # Switch the reaction to reaction_type
            reaction.save()
            return JsonResponse({"status": f"switched_to_{reaction_type}"})

        return JsonResponse({"status": "added"})


class LikeReviewView(ReactionView):
    """
    View for handling 'like' reactions. Inherits from ReactionView.
    """

    def post(self, request, object_id):
        """
        Handle POST request for 'like' reactions.
        :param request: HttpRequest object.
        :param object_id: id of the object to which the reaction is tied.
        :return: JsonResponse indicating the status of the operation.
        """
        return self.get_reaction(object_id, 'like')


class DislikeReviewView(ReactionView):
    """
    View for handling 'dislike' reactions. Inherits from ReactionView.
    """

    def post(self, request, object_id):
        """
        Handle POST request for 'dislike' reactions.
        :param request: HttpRequest object.
        :param object_id: id of the object to which the reaction is tied.
        :return: JsonResponse indicating the status of the operation.
        """
        return self.get_reaction(object_id, 'dislike')


@method_decorator(csrf_exempt, name='dispatch')
class ReplyCreateView(generic.View):
    def get_post_data(self, request):
        body_unicode = request.body.decode('utf-8')
        return json.loads(body_unicode)

    def get_object_or_404(self, model_class, id):
        try:
            return model_class.objects.get(id=id)
        except model_class.DoesNotExist:
            raise Http404(f"{model_class.__name__} does not exist")

    def create_reply(self, user_id, reply_text, review=None, parent_reply=None):
        return Reply.objects.create(
            review=review,
            user_id=user_id,
            reply_text=reply_text,
            parent_reply=parent_reply
        )

    def post(self, request, *args, **kwargs):
        post_data = self.get_post_data(request)
        user_id = post_data.get('user_id')
        review_id = post_data.get('review_id')
        parent_id = post_data.get('parent_id')
        reply_text = post_data.get('reply_text')

        review, parent_reply = None, None
        if parent_id not in [None, 'null']:
            parent_reply = self.get_object_or_404(Reply, parent_id)
        else:
            review = self.get_object_or_404(Review, review_id)

        reply = self.create_reply(
            user_id=user_id,
            reply_text=reply_text,
            review=review,
            parent_reply=parent_reply
        )

        return JsonResponse({'status': 'success', 'reply': model_to_dict(reply)}, status=201)







# @method_decorator(csrf_exempt, name='dispatch')
# class ReplyCreateView(generic.View):
#     def post(self, request, *args, **kwargs):
#         body_unicode = request.body.decode('utf-8')
#         body_data = json.loads(body_unicode)
#         user_id = body_data.get('user_id')
#         review_id = body_data.get('review_id')
#         parent_id = body_data.get('parent_id')
#         reply_text = body_data.get('reply_text')
#
#         try:
#             review = Review.objects.get(id=review_id)
#         except Review.DoesNotExist:
#             return JsonResponse({"error": "Review does not exist"}, status=404)
#
#         reply = None
#         parent_reply = None
#         if parent_id not in [None, 'null']:  # Check for both None and 'null' string
#             try:
#                 parent_reply = Reply.objects.get(id=parent_id)
#                 reply =  Reply.objects.create(
#                     user_id=user_id,
#                     parent_reply=parent_reply,
#                     reply_text=reply_text,
#                 )
#             except Reply.DoesNotExist:
#                 return JsonResponse({"error": "Parent reply does not exist"}, status=404)
#         else:
#             reply = Reply.objects.create(
#                 review=review,
#                 user_id=user_id,
#                 reply_text=reply_text,
#             )
#
#         return JsonResponse({'status': 'success', 'reply': model_to_dict(reply)}, status=201)
