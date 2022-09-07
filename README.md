# Test, Flask and AWS

## This repository is a simple test to explore Flask and AWS compatibility

## Test steps
- [x] Push code to github
- [] Set-up environment on AWS
- [] Set-up code pipeline on AWS
- [] See if application is live
- [] Make changes to code
- [] Push updates to github
- [] Check if application is still live and updates are there

## help
https://aws.amazon.com/getting-started/hands-on/serve-a-flask-app/
https://www.youtube.com/watch?v=4tDjVFbi31o


## Attempt 1
- Failed...
- didn't have a `requirement.txt` file...likely an issue as AWS didn't know about flask
- what the heck is AWS lightsail?

## Attempt 2
- it worked!
- not completely sure but filename `application.py`, `application` instead of `app` in the code seemed to work

## Notes and Thoughts:
- first deployment attempt, main py file is named `application.py`, note Flask docs typically start with app
-
- In the context of my personal website, is it as simple as renaming the main folder to 'application'?
- I didn't create a `requirements.txt` file
