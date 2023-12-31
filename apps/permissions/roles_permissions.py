"""
    Files defines permissions for default groups
"""
from users.permissions import user_premium_permissions
from django.contrib.auth.models import Group


def get_base_permissions():
    """
        Returns the set of common permissions
    """

    # Base permissions for 'users' app
    users_app_permissions = {
        "view_own_activity",
        "change_own_status",
        "manage_own_profile",
        "view_own_sensitive_info",
        "flag_itself",
        "flag_users",
        "manage_own_distributions",
        "manage_own_session_status",
    }

    # Base permissions for 'reviews' app
    reviews_app_permissions = {
        "add_review",
        "view_review",
        "change_review",
        "delete_review",
        "respond_own_review",
        "respond_others_reviews",
        "rate_own_review",
        "rate_others_reviews",
        "flag_own_review",
        "flag_others_reviews",
    }

    return users_app_permissions | reviews_app_permissions


def get_sellers_permissions():
    """
        Returns the set of all permissions for Seller group
    """
    seller_permissions = get_base_permissions()
    seller_permissions.remove("rate_own_review")
    seller_permissions.remove("rate_others_reviews")

    return seller_permissions


def get_moderators_permissions():
    """
        Returns the set of all permissions for Moderator group
    """
    moderator_permissions = get_base_permissions()
    additional_permissions = {
        "manage_users_profiles",
        "verify_users_profiles",
        "view_hidden_statistics",
        "export_own_data",
        "export_users_data",
        "manage_users_distributions",
        "manage_users_session_statuses",
        "hide_reviews",
        "show_reviews",
        "view_hidden_reviews",
        "approve_reviews",
        "post_without_approval"
    }

    return moderator_permissions | additional_permissions


def get_admins_permissions():
    """
        Returns the set of all permissions for Admin group
    """
    admin_permissions = get_moderators_permissions()
    additional_permissions = {
        "protect_reviews_from_delete",
        "protect_reviews_from_edit",
        "protect_reviews_from_respond",
        "protect_reviews_from_hide",

        "ban_users",
        "unban_users",
        "edit_user_group",
    }

    return admin_permissions | additional_permissions


def get_group_permissions(group_name: str):
    """
        Returns a list of permission codenames for a given Django group (role).
        ['add_user', 'change_user', 'delete_user', 'view_user']

        Note:
        This function assumes that a group with the given name exists.
        If the group does not exist, the function raises a Group.DoesNotExist exception.
        If you're not sure whether the group exists, you should handle this exception in your code.
    """

    group = Group.objects.get(name=group_name)
    permissions = group.permissions.all()

    return [perm.codename for perm in permissions]


customers_permissions = get_base_permissions()
sellers_permissions = get_sellers_permissions()
moderators_permissions = get_moderators_permissions()
admins_permissions = get_admins_permissions()

premium_customer_permissions = (
        list(customers_permissions)
        + [permission[0] for permission in user_premium_permissions]
)
