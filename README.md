# twitter-clone
this is a social media app like tweeter that users can post text/video/images

features like reTweet, bookmark, like, comment, like comments, reply comments are implemented

### How to use 
- first create a .env file
- after creating the .env file add required info
```
Project_KEY = ""
Debug = True 
DB_NAME = ""
DB_USER = ""
DB_PASS = ""
```
- then run the docker compose

      docker compose -f "docker-compose.yml" up -d --build
- project will be running at port 8000
- to see logs in debugMode

      docker logs --tail 1000 -f <docker container>

## features
1) User have home page a only sees posts from following users
2) users can follow / unfollow eachother
3) if users like a post they can bookmark it
4) users can like posts
5) every users can comment or reoly to a comment
6) rePosting is avalible and also users can Quote posts like twitter

### auth
i wrote authentication and veryfing users my self

users can login/logout/singnup 

every time a user is created a post_save singnal will trigger a verification email

verification is done by sending a uuid and username in url

### User profile 
if request.user is equal to profile owner users can edit the profile

in profile part users can see the users tweets / retweets and some regular info about user (joined / birthday / follwer count / following count)

users can follow or un follow eachother 

message sending is unavalible because it contains js and websockets (i dont like js + i didnt care enough to do it )

