# Plexus2.0

### Linux based Setup for Plexus development:
1) Run the following git clone:
 
    `git clone https://github.com/Rohit599/Plexus2.0 Plexus`
    
2) cd into the directory into which you cloned the git repository:
 
    `cd Plexus`
 
3) Run virtualenv on the git cloned directory to setup the Python virtual environment:
 
    `virtualenv env`
 
4) Activate the virtual environment:
 
    `source bin/activate`
    
    (`env\scripts\activate` for Windows based users)
 
5) After activating the virtual environment, install the dependencies:
 
    `pip install -r requirements.txt`
 
6) Generate initial data by running the command:

    `python manage.py startdata`

7) Now, create the database migrations so as to use the Database:
 
    `python manage.py makemigrations`
    
    `python manage.py migrate`
    
8) Create a supersuperuser:

    `python manage.py createsuperuser`
  
9) You are all set. Run the final command:

    `python manage.py runserver`
    
10) Its time to rock. Visit http://localhost:8000 in your browser and you should be all set.
    
### API Endpoints:

- `admin/` : Opens admin panel
- `api/register/player_register/`: Register a player
- `api/register/society_register/`: Register a society
- `api/register/login/`: Login for player/society
- `api/token/`: Returns an access and refresh JSON web token pair
- `api/token/refresh/`: Returns an access type JSON web token if the refresh token is valid
- `api/dashboard/society_dashboard/`: Lists all the events under the society
- `api/dashboard/events/`: Viewset for the event model : <b>Creates event</b>
- `api/dashboard/events/{pk}/questions`: Viewset for the questions model : <b>Creates question for a specific event pk</b>
- `api/dashboard/events/{pk}/questions/{pk}`: PUT/PATCH/DELETE for question of specific pk
- `api/dashboard/events/{pk}/rules/`: Viewset for the rules model : <b>Creates rules for a specific event pk</b>
- `api/dashboard/events/{pk}/rules/{pk}`: PUT/PATCH/DELETE for rules of specific pk
- `api/dashboard/past_events/`: Get all past events
- `api/dashboard/present_events/`: Get all present events
- `api/dashboard/future_events/`: Get all future events
- `api/dashboard/player_dashboard/`: Gets a list for all the events
- `api/dashboard/player_dashboard/{pk}`: Gets all the details for a specific event pk
- `api/dashboard/player_dashboard/{pk}/play`: Gets the question of a specific event pk
- `api/dashboard/leaderboard/<int:pk>`: Leaderboard of a specific event
- `/swagger/`: API Documentation using Swagger
- `/redoc/`: API Documentation using Redoc
