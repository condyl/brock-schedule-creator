# NOTICE: OLD REPO, NEW REPO [HERE](https://github.com/iOlivers/BrockTimeTable)
We have decided to create this project in React.  This repo will no longer be updated.

# Brock University Timetable Generator

## Features

* **Automatic Overlap Detection:** Say goodbye to conflicting classes. The generator only produces valid schedules where no classes overlap.
* **User-Friendly Course Input:** Simply add the courses you want to take, and the tool does the rest.
* **Instant Timetable Generation:** Get a list of all possible valid schedules in seconds.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/condyl/brock-schedule-creator.git
   ```
2. **Set Up Virtual Environment:** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install Dependencies:**
   ```bash
   pip install django
   ```
4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Start the Server:**
   ```bash
   python manage.py runserver
   ```

## Usage

1. **Visit the Website:** Open your web browser and navigate to `http://127.0.0.1:8000/`.
2. **Add Your Courses:** Enter the course codes for the classes you want to take.
3. **Generate Timetables:** Click the "Generate" button.
4. **Review & Select:** Browse the generated schedules and choose the one that best fits your needs. 
