## Guidelines
- Date Format - yyyy/mm/dd


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




