## Guidelines
- Date Format - yyyy/mm/dd



## [DEV] - 2023-06-07

REFACTOOOOR
### CHANGED
- Improve templates 




## [DEV] - 2023-06-06

REFACTOOOOR
### ADDED
- Admin.py to users

### CHANGED
- Move authentication from core to users app
- Refactor Cart.views.get_cart_from_session func





## [DEV] - 2023-06-05

Another refactor day

### Added
- Category's image field
- Categories list
- Catalog
  - Admin.py 
    - Search fields
    - List filters
    - Inlines for related models
    - Docstrings
  - Model.py
    - add allow_unicode=True to slug fields
- viewsets.py


### Changed
- Catalog 
  - Views.py
    - Refactoring
      - Removed unnecessary imports:
      - Added individual functions for getting attributes, reviews, and filtered products
      - Added prefetch_related and select_related: To improve the efficiency of database queries
      - Created a function for getting all categories
      - Move viewsets to viewsets.py
      - Docstrings
  - Model.py
    - Fixing
      - added a check to func get_product_rating to ensure there are ratings before attempting to calculate the mean
      
    - Refactoring
      - removing unnecessary filtering from @price property

## [DEV] - 2023-06-04

Converted fork into repository because commits history

### Added
- tailwind js packages
- Top product component
- Most reviewed component
- Implemented banner slider

### Fixed
- Display product based on is_active field value



## [DEV] - 2023-06-03

#### Refactor day

### Added
- DocStrings for different views and models
- Project's media assets

- Django Models
  - Core
    - Add "upload_to" field to profile
  - Catalog
    - default images paths
    - upload images paths

### Changed
- Reinstall tailwindcss for production


- HTML Pages
  - Templates
    - SubCategory Detail page 
    - Product Detail page


- Django Models
  - Core
    - Update age method to return the age in years as an integer. The previous version was returning a datetime.timedelta object.


- Django Urls
  - SubCategory Detail View
  - Product Detail View
  - All Cart Urls
  - Config Urls file
  

- Pipenv file


### Removed
- HTML Pages
  - Templates
    - Non-used templates
- Content of the static folder




## [DEV] - 2023-06-02

### Added
- Implemented product filtering
- Implemented product attributes 

### Changed

- HTML Pages
  - Templates
    - SubCategory Detail page 
    - Product Detail page

    
- Django Views
  - SubCategory Detail View
  - Product Detail View
  

## [DEV] - 2023-06-01

### Added
- Implemented reviews


- HTML Pages
  - Templates
    - Product Detail page
    

- Django Views
  - Product Detail View
  - Review Create View
  

- Django Urls
  - Product detail
  - Review create


- Django Forms
  - ReviewForm


- templatetags folder
  - Math filters for reviews
    - floor
    - full_stars
    - half_star
    - round_half

## [DEV] - 2023-05-31

### Added

- HTML Pages
  - Templates
    - Category Detail page
    - Sub Category Detail page
    

- Django Views
  - Category Detail View
  - Sub Category Detail View
  

- Django Models
    - Category 
      - slug field
      - icon field
      - description field


- Django Urls
  - Category detail
  - SubCategory detail

## [DEV] - 2023-05-30

### Added

- HTML Pages
  - Templates
    - Home page
  - Components
    - Header
      - Logo
      - Categories list
    - Slider
    - New products
    - Trending products


- Django Models
  - Sub Category


- Django Views
  - Home page view


### Fixed

- Product model - @price property

### Changed
- Django models
  - Category
  - Product
    - category field relationship (Category -> SubCategory)
  - ProductAttribute
    - related_name on category



## [DEV] - 2023-05-29

[//]: # ([view diff]&#40;https://github.com/standard/standard/compare/v5.2.0...v5.2.1&#41;)

#### A fork of the repository was made and I started writing the frontend

### Added

- Template folder

### Changed

- Project structure

### Removed

- The unimplemented frontend folder




