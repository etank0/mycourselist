
# MyCourseList

## Project Overview

**MyCourseList** is a web-based course management system designed to simplify the process of managing course selections for students and administrators. The system allows students to add and remove courses from their personal lists while giving administrators the ability to perform Create, Read, Update, and Delete (CRUD) operations on the course database.

## Features

- **User Management**: Students can easily manage their course selections, adding or removing courses as needed.
- **Administrative Access**: Administrators can perform comprehensive CRUD operations on the courses database, ensuring that the course listings are current and accurate.
- **YouTube Integration**: Courses are linked with YouTube videos providing supplementary video content to enhance the learning experience.
- **Responsive Design**: The system uses React, HTML and CSS(Bootstrap) to provide a responsive and visually appealing interface.

## Technologies Used

- **Frontend**: React, HTML, CSS(Bootstrap)
- **Backend**: Python (Flask)
- **Database**: SQLite3

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/etank0/mycourselist
   ```

2. **Navigate to the project directory:**
   ```bash
   cd mycourselist
   ```

3. **Install dependencies for frontend:**
   ```bash
   cd client
   npm install
   ```

4. **Install dependencies for backend:**
   ```bash
   cd server
   pip install -r requirements.txt
   ```

5. **Run the server application:**
   ```bash
   python app.py
   ```

6. **Run the client application:**
   ```bash
   npm start
   ```

## Usage

- **For Students**: Log in to your account, browse available courses, and manage your course list through the user dashboard.
- **For Administrators**: Access the administrative panel to update course details, add new courses, or delete outdated entries.
