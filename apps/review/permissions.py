reviews_basic_interactions_permissions = [
    ("respond_own_review", "Can respond to its own review"),
    ("respond_others_reviews", "Can respond to others reviews"),

    ("rate_own_review", "Can rate its own review"),
    ("rate_others_reviews", "Can rate others reviews"),

    ("flag_own_review", "Can flag its own review"),
    ("flag_others_reviews", "Can flag others reviews"),

    ("attach_files", "Can attach files"),
    ("remove_others_attached_files", "Can remove others attached files to reviews"),
]

reviews_visibility_permissions = [
    ("hide_reviews", "Can hide users reviews"),
    ("show_reviews", "Can show users reviews"),

    ("view_hidden_reviews", "Can view hidden reviews"),
    ("approve_reviews", "Can approve reviews"),
    ("post_without_approval", "Can post reviews without approval")
]

reviews_protection_permissions = [
    ("protect_reviews_from_delete", "Reviews of this user cannot be deleted"),
    ("protect_reviews_from_edit", "Reviews of this user cannot be edited"),
    ("protect_reviews_from_respond", "Reviews of this user cannot be respond"),
    ("protect_reviews_from_hide", "Reviews of this user cannot be hidden"),

    ("delete_protected_reviews", "This user can delete protected reviews"),
    ("edit_protected_reviews", "This user can edit protected reviews"),
    ("respond_protected_reviews", "This user can respond to protected reviews"),
    ("hide_protected_reviews", "This user can hide protected reviews"),
]

review_permissions = (
        reviews_basic_interactions_permissions
        + reviews_visibility_permissions
        + reviews_protection_permissions
)
