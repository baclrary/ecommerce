"""
    Permissions for CustomUser model
"""
# є суть в плурал, навіть якщо у вью або темлейті потрібна перевірка на власника:
# Приклад: хочу удалити свій комент: потрібно мати пермішн на видалення і перевірка на власника щоб видалити
# Хочу видалити чужі коменти: потрібно мати пермішен на видалення коментів (загальне).
# if request.user.has_perm.delete_review & review.owner == request.user OR request.user.has_perm.delete_reviews


user_account_management_permissions = [
    ("ban_users", "Can ban users accounts"),
    ("unban_users", "Can unban users accounts"),

    ("edit_own_group", "Can edit its own account role"),
    ("edit_user_group", "Can edit user accounts roles"),
]

user_data_access_and_modification_permissions = [
    ("view_own_activity", "Can view its own account activity"),
    ("view_users_activities", "Can view users accounts activities"),

    ("view_moderators_activities", "Can view moderators accounts activities"),
    ("view_admins_activities", "Can view admins accounts activities"),

    ("change_own_status", "Can change its own account status"),
    ("change_users_statuses", "Can change users accounts statuses"),

    ("manage_own_profile", "Can manage its own account profile"),
    ("manage_users_profiles", "Can manage users accounts profiles"),

    ("verify_own_profiles", "Can verify its own account profile"),
    ("verify_users_profiles", "Can verify users accounts profiles"),

    ("view_own_sensitive_info", "Can view its own sensitive account information"),
    ("view_sensitive_users_info", "Can view sensitive users accounts information"),

    ("view_own_statistics", "Can view its own account statistics"),
    ("view_users_statistics", "Can view users accounts statistics"),
    ("view_hidden_statistics", "Can view hidden users accounts statistics"),

    ("export_own_data", "Can export own account data"),
    ("export_users_data", "Can export users accounts data"),
]

user_permissions_granting_and_revocation_permissions = [
    ("grant_own_permissions", "Can grant permissions to itself account"),
    ("grant_users_permissions", "Can grant permissions to users accounts"),

    ("revoke_own_permissions", "Can revoke permissions from itself account"),
    ("revoke_users_permissions", "Can revoke permissions from users accounts"),
]

user_notification_and_distribution_permissions = [
    ("manage_own_distributions", "Can manage its own account email distributions"),
    ("manage_users_distributions", "Can manage users accounts email distributions"),

    # ("send_own_notifications", "Can send notifications to itself account"),
    # ("send_users_notifications", "Can send notifications to users accounts"),
]

user_session_control_permissions = [
    ("manage_own_session_status", "Can manage its own account session status (Terminate)"),
    ("manage_users_session_statuses", "Can manage user accounts sessions statuses (Terminate)"),
]

user_feedback_and_reporting_permissions = [
    ("flag_itself", "Can report itself account"),
    ("flag_users", "Can report users account"),
]


user_premium_permissions = [
    ("premium_permission_1", "Premium permission")
]

user_permissions = (
        user_account_management_permissions
        + user_data_access_and_modification_permissions
        + user_permissions_granting_and_revocation_permissions
        + user_notification_and_distribution_permissions
        + user_session_control_permissions
        + user_feedback_and_reporting_permissions
        # + user_premium_management_permissions
)
