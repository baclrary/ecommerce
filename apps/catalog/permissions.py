category_permissions = [
    ("create_category", "Can create a new category"),
    ("edit_own_category", "Can edit own categories"),
    ("edit_others_categories", "Can edit others categories"),
    ("delete_own_category", "Can delete own categories"),
    ("delete_others_categories", "Can delete others categories"),
    ("view_hidden_categories", "Can view hidden categories")
]

subcategory_permissions = [
    ("create_subcategory", "Can create a new subcategory"),
    ("edit_own_subcategory", "Can edit own subcategories"),
    ("edit_others_subcategories", "Can edit others subcategories"),
    ("delete_own_subcategory", "Can delete own subcategories"),
    ("delete_others_subcategories", "Can delete others subcategories"),
    ("view_hidden_subcategories", "Can view hidden subcategories")

]

categoryattribute_permissions = [
    ("create_categoryattribute", "Can create a new category attribute"),
    ("edit_own_categoryattribute", "Can edit own category attributes"),
    ("edit_others_categoryattribute", "Can edit others category attributes"),
    ("delete_own_categoryattribute", "Can delete own category attributes"),
    ("delete_others_categoryattribute", "Can delete others category attributes"),
    ("view_hidden_categoryattributes", "Can view hidden category attributes")
]

product_permissions = [
    ("create_product", "Can create a new product"),
    ("edit_own_product", "Can edit own products"),
    ("edit_others_products", "Can edit others products"),
    ("delete_own_product", "Can delete own products"),
    ("delete_others_products", "Can delete others products"),
    ("change_product_status", "Can change product status (Active/Inactive)"),
    ("view_hidden_products", "Can view hidden products")
]

productattribute_permissions = [
    ("create_productattributes", "Can create a new product attributes"),
    ("edit_own_productattributes", "Can edit product attributes"),
    ("edit_others_productattributes", "Can edit others product attributes"),
    ("delete_own_productattributes", "Can delete product attributes"),
    ("delete_others_productattributes", "Can delete others product attributes"),
    ("view_hidden_productattributes", "Can view hidden product attributes")
]

banner_permissions = [
    ("create_banners", "Can create a new banners"),
    ("edit_own_banners", "Can edit own banners"),
    ("edit_others_banners", "Can edit others banners"),
    ("delete_own_banners", "Can delete own banners"),
    ("delete_others_banners", "Can delete others banners"),
    ("view_hidden_banners", "Can view hidden banners")
]

catalog_permissions = (
        category_permissions
        + subcategory_permissions
        + categoryattribute_permissions
        + product_permissions
        + productattribute_permissions
        + banner_permissions
)
