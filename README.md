# Hotel Management Django App
This Django application provides a complete solution for managing hotel information. It includes features for creating and managing hotel information, locations, amenities, and images. The app also supports CRUD operations for these entities. Additionally, a CLI tool is provided for importing data from another database.

## Features

- **Superuser Administration**: Create a superuser admin account to manage hotel information, locations, amenities, and images.
- **CRUD Operations**: Perform Create, Read, Update, and Delete operations for hotel information, locations, amenities, and images.
- **Dynamic Amenities Management**: Add multiple amenities dynamically when creating or editing hotel information.
- **CLI Tool**: Import data from another database using a command-line interface with authentication and connection details.
## Database design
- `id`: Auto-generated unique identifier for each hotel (Primary Key).
- `title`: The title of the hotel.
- `description`: A description of the hotel.
- `images`: A one-to-many relationship with the `Image` model. Each hotel can have multiple images.
  - `name`: The name of the image file.
- `location`: A many-to-many relationship with the `Location` model. Each hotel can be associated with multiple locations.
  - `name`: The name of the location.
  - `type`: The type of location (city, state, country).
  - `latitude`: The latitude coordinate of the location.
  - `longitude`: The longitude coordinate of the location.
- `amenities`: A many-to-many relationship with the `Amenity` model. Each hotel can have multiple amenities.
  - `name`: The name of the amenity.
- `create_date`: The date and time when the hotel information was created.
- `update_date`: The date and time when the hotel information was last updated.        
## Installation
1. **Clone the Repository**
 ```bash
   git clone https://github.com/w3-software-intern-Riad/django-admin-pipeline.git
   
   ```
   2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
 3. **Install Dependencies**

 ```bash
 pip install -r requirements.txt
```
4. **Configure .env**
```bash
create a .env file and configure it as .env.sample
```
 5. **Apply Migrations**

 ```bash
 python manage.py migrate
 ```

 6. **Create a Superuser**

 ```bash
 python manage.py createsuperuser
 ```
 7. **Run the Development Server**
 ```bash 
 python manage.py runserver
 ```
 ## Admin Interface
 - Once the server is running, you can access the Django admin interface at:
 ```bash
 http://127.0.0.0:8000/admin
 ```
 - Log in with the superuser credentials you created to manage hotel information, locations, amenities, and images.
 ## Using the CLI Tool
The CLI tool is implemented using Django's management commands. It allows importing data from another database. That database should have 8 property like propertyTitle , latitude , longitude , rating, price , location ,roomType, images

### Command
```bash
python manage.py import_data
```
### Terminal Output Example:
```bash
Admin username:👤 [Please provide the admin username that was used during the creation of the superuser account.]
```
```bash
Admin password:🔑 [Please provide the admin password that was used during the creation of the superuser account.]
```
### If admin is authenticated then 

```bash
Database name (scrapy database) : (eg. hotel)
```
```bash
Database username: (eg. postgres)
```
```bash
Database password: (eg. p@stgress)
```
```bash 
Database host: (eg. localhost)
```
```bash 
Database port: (eg. 5432)
```
```bash 
Directory path of the images in Scrapy project: (eg. /home/w3e101/Desktop/hdd_data/Abdulla-al-riad(intern 8th batch)/Hotel-Scraper/hotelscraper/images)
```
## Important Note

- To locate the image path in your Scrapy project, navigate to the `images` folder within the project, open a terminal, and type `pwd`.


## Contributing
### Contributions are welcome! Please follow the guidelines for contributing and ensure your code adheres to the project's style guidelines.

 - Fork the repository.

- Create a new branch (git checkout -b feature-branch).
-  Make your changes.
- Commit your changes (git commit -am 'Add feature').
- Push to the branch (git push origin feature-branch).
- Create a new Pull Request.