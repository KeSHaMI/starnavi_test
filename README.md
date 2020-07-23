# starnavi_test

Technologies: DjangoRestFramework, djangorestframework_simplejwt(Token authetication)

# Tests

I've tried TDD and that's pretty nice, testing all functionality required in test_cycle.py and additionaly testing all crud in test_crud.py

# CRUD requests guide

in general data manipulation looks like
domain/api/action/model/id(if operation requires(get, update, delete))/

Actions:
  - get_all(returns all instances of model) GET
  - get(returns single instance) GET
  - create(creates instance) POST
  - update(returns udpated instance) POST!
  - delete(deletes instance) DELETE
  
 Models:
  - User(default django user fields + last_action_time): 
    Important fields: last_login, last_action_time, email(unique), username
    To create: email, username, password
  - Post:
    Fields: user, title, body, date_created(auto)
    To create: user(id), title, body
  - Like:
    Fields: user, post, date_created(auto)
    To create: user(id), post(id)
    
# Tokens
Usng JWT token authentication system

POST api/token/:
  request: password, email 
  response: access-token(1 hour), refresh-token(1 day)
POST api/token/refresh:
  request: refresh-token
  response: access-token
  
Using tokens:
  Add Authentication header(Bearer ACCESS-TOKEN) for each request(creating user doesn't require)
  
# Analytics
GET api/analytic/?date_from=(ISO format datetime)&date_to=(ISO format datetime)
response: likes amount aggregated by date(not Like objects, just numbers)
