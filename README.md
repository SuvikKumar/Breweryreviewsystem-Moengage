# Brewery Reviews Application

This is a Flask web application that allows users to search for breweries, view brewery details and reviews, and add their own reviews. The application features user authentication with login and signup functionality.

## Features

- User Authentication: Sign up and log in to access the application.
- Search for Breweries: Search by name, city, or type.
- View Brewery Details: See the name, address, phone number, website URL, city, state, and current rating of a brewery.
- View and Add Reviews: View existing reviews and add new reviews for a brewery.

## Pages

1. **Login/Signup Page**
2. **Search Page**
3. **Brewery Page**: Displays existing reviews and allows adding new reviews.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/SuvikKumar/Breweryreviewsystem-Moengage/tree/main.git
    cd brewery-reviews
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```sh
    python -c "from app import init_db; init_db()"
    ```

5. Run the application:
    ```sh
    python app.py
    ```

6. Open a web browser and go to `http://127.0.0.1:5000/`.

## Usage

### 1. Sign Up
- Go to the sign-up page (`/signup`) and create a new account.

### 2. Log In
- Go to the login page (`/login`) and log in with your credentials.

### 3. Search for Breweries
- Use the search form on the home page to search for breweries by name, city, or type.

### 4. View Brewery Details
- Click on a brewery from the search results to view its details and reviews.

### 5. Add a Review
- On the brewery details page, use the form to add a new review with a rating and description.

## Database Schema

### Users Table
- `id`: Integer, Primary Key
- `username`: Text, Unique, Not Null
- `password`: Text, Not Null

### Breweries Table
- `id`: Integer, Primary Key
- `name`: Text, Not Null
- `location`: Text, Not Null
- `address`: Text, Not Null
- `phone`: Text
- `website`: Text
- `city`: Text
- `state`: Text
- `type`: Text
- `current_rating`: Real

### Reviews Table
- `id`: Integer, Primary Key
- `brewery_id`: Integer, Foreign Key to Breweries Table
- `rating`: Integer, Not Null
- `description`: Text, Not Null


## Repository

The code for this application is available on GitHub: https://github.com/SuvikKumar/Breweryreviewsystem-Moengage/tree/main

