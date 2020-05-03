# Messaging
A messaging server using [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [Sqlite](https://www.sqlitetutorial.net/sqlite-python/)
## How to run the server?
##### to run this server you have first to excute in the command line ```py main.py```
##### you will see the URL that server is runing on. it's usually runing on  http://localhost:5000/
## How to use the server?
the best way to use this server is with [postman](https://www.postman.com/)
## The Api's:
##### The server includes the following Api's:
### Add Message:
##### To add a new message
##### method-POST , url-'/addMessage'
##### data required :
##### json object:
##### ```{"application_id": number,"session_id": text,"message_id":unique text, "participants":list of participants,"content": text}```
### Get Message:
##### To get a message by a requested attribute 
##### method - POST , url-'/getMessage'
**query params one of the following:**
##### ```application_id : number ``` 
##### ```session_id :text ``` 
##### ```message_id :text ```
### Delete Message:
##### To delete a message by a requested attribute 
##### method - POST , url-'/deleteMessage'
**query params one of the following:**
##### ```application_id : number ``` 
##### ```session_id :text ``` 
##### ```message_id :text ```
