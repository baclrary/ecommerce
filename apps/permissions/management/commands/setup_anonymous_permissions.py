from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm, get_anonymous_user, remove_perm


class Command(BaseCommand):
    help = 'Set permissions for anonymous users'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting permissions for anonymous users...')

        anonymous_user = get_anonymous_user()

        # Allow anonymous users some permissions
        assign_perm('review.view_hidden_reviews', anonymous_user)
        #
        # Remove permissions
        # remove_perm('review.view_hidden_reviews', anonymous_user)

        self.stdout.write(self.style.SUCCESS('Done setting permissions for anonymous users'))
