# Get Code (Blog/Website)

## Project Overview

The Get Code Blog/Website project aims to create a web platform combining both backend functionalities and a frontend UI. This platform allows users to download specific code files and view posts. If the requested code file is not available, users can contact the admin to request it.


#### Frontend

The frontend of the Get Code Blog/Website project is designed using HTML and CSS to provide a clean and user-friendly interface. Jinja templates are employed to dynamically render content and integrate with the backend seamlessly. HTML structures the content, CSS styles it to enhance visual appeal, and Jinja templates facilitate the presentation of dynamic data. This combination ensures that users have an interactive and engaging experience while navigating the website and accessing code files and posts.

#### Backend

The backend of the Get Code Blog/Website project is developed using Python with the Flask framework. Flask is used to handle web requests and manage the application’s routing. For database interaction, SQLAlchemy is employed as the Object-Relational Mapping (ORM) tool, facilitating smooth communication between the Flask application and the MySQL database. SQLAlchemy simplifies database operations by allowing developers to use Python classes to represent database tables and execute queries. This setup ensures efficient and scalable data management for the application.

### User and Admin Features

#### User Features

* **Download Code Files:** Users can search for and download specific code files available on the platform.

* **View Posts:** Users can browse and read posts related to various code snippets and topics.


#### Admin Features

* **Manage Code Files:** Admins have the ability to add, delete, and edit code files available on the platform.

* **Manage Posts:** Admins can create, modify, and remove posts to keep content up to date.

* **Admin Login:** Access to the admin panel is secured with a username and password. These credentials are configurable via a .json file. Once logged in, admins have full control over managing and editing all content on the website.


## Installation

#### Prerequisites

* Python 3.8 or later
* pip (Python package installer)
* MySQL Database


#### Steps

1. Clone the repository:

    `git clone https://github.com/username/repository.git` 

    `cd repository`

2. Create Virtual Environment:
    
    `python -m venv venv`

3. Activate the Virtual Environment:

    * On Windows:
    
        `venv\Scripts\activate`
    
    * On Mac or Linux:

        `source venv/bin/activate`

4. Install the required packages:

    `pip install -r requirements.txt`


## Configuraton

Create config.json file and add configuration params:

```json
{
    "params":
    {
        "local_server":"True/False",
        "MYSQL_HOST":"",
        "MYSQL_USER":"",
        "MYSQL_PASSWORD":"",
        "MYSQL_DB":"",
        "local_uri":"mysql+pymysql://<root>:<password>@localhost:3306/<db_name>",
        "prod_uri":"mysql+pymysql://<root>:<password>@localhost:3306/<db_name>",
        "SQLALCHEMY_TRACK_MODIFICATIONS":"False",
        "fb_uri":"<fb_uri>",
        "tw_uri":"<twitter_uri>",
        "gt_uri":"<github_uri>",
        "no_of_posts":int(<no of post per page>),
        "admin-uname":"<Admin username>",
        "admin-pass":"<Admin password>",
        "admin-name":"<admin name>",
        "admin-email":"<admin email>",
        "codefile-uploadpath":"<path to codefiel upload>"
    }
}
```


## Running the Appliacation

To run the Flask application in development mode, use:

`python Website.py`

For production deployment, use a WSGI server like Gunicorn:

`gunicorn --bind 0.0.0.0:8000 wsgi:app`


## Acknowledgements

* **Flask:** A lightweight WSGI web application framework in Python that provides the necessary tools and libraries for building web applications.
* **SQLAlchemy:** An ORM library for Python that simplifies database interactions and management.
* **HTML/CSS:** The foundational technologies for creating and styling the frontend of the website.
* **Jinja:** A templating engine for Python that enables dynamic content rendering within HTML templates.
* **Open Source Community:** For providing valuable resources, libraries, and tools that aid in the development of web applications.