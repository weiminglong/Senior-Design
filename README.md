# QA Classifier

## Setting Up the Project
- Backend
  - Create a conda environment for the backend dependencies and activate 
  - Install dependencies using the environment.yml file found within the repository
  - Create a MongoDB account and AWS account
  - Configure the AWS S3 bucket access and Google Cloud access in the console and replace authentication strings (*note: must use the same database and collection names)
    - app.py for MongoDB
    - auto.py for Google Cloud
  - Configure `export FLASK_APP=app.py`
- Frontend
  - Install node.js and npm
  - Install Angular CLI and Angular Material 
- Run `flask run` for the backend and `ng serve` in the frontend to test if the application has installed correctly.
