# Starnavi_test

Technologies: DjangoRestFramework, djangorestframework_simplejwt(Token authetication)

# Tests

I've tried TDD and that's pretty nice, testing all functionality required in test_cycle.py and additionaly testing all crud in test_crud.py

# CRUD requests guide

in general data manipulation looks like
domain/api/action/model/id(if operation requires(get, update, delete))/

Actions:
<table>
  <tr>
    <td><b>Action</b></td><td><b>Comment</b></td><td><b>Method</b></td>
  </tr>
  <tr>
    <td>get_all</td><td>returns all instances of model</td><td>GET</td>
  </tr>
  <tr>
    <td>get</td><td>returns single instance</td><td>GET</td>
  </tr>
  <tr>
    <td>create</td><td>creates instance</td><td>POST</td>
  </tr>
  <tr>
    <td>update</td><td>returns updated instance</td><td>POST!</td>
  </tr>
  <tr>
    <td>delete</td><td>deletes instance</td><td>DELETE</td>
  </tr>
</table>

  
 Models:
 <table>
  <tr>
    <td><b>Model</b></td><td><b>Fields</b></td><td><b>To create</b></td>
  </tr>
  <tr>
    <td>User(default django user fields + last_action_time)</td><td>last_login, last_action_time, email(unique), username</td><td> email, username, password</td>
  </tr>
  <tr>
    <td>Post</td><td>user, title, body, date_created(auto)</td><td>user(id), title, body</td>
  </tr>
  <tr>
    <td>Like</td><td>user, post, date_created(auto)</td><td>user(id), post(id)</td>
  </tr>
  </table>

    
# Tokens
Usng JWT token authentication system
<table>
  <tr>
    <td><b>Method</b></td><td><b>Link</b></td><td><b>Request</b></td><td><b>Response</b></td>
  </tr>
  <tr>
    <td>POST</td><td>api/token/</td><td>password, email</td><td>access-token(1 hour), refresh-token(1 day)</td>
  </tr>
  <tr>
    <td>POST</td><td>api/token/refresh</td><td>refresh-token</td><td>access-token</td>
  </tr>
</table>
  
Using tokens:
  Add Authentication header(Bearer ACCESS-TOKEN) for each request(creating user doesn't require)
  
# Analytics
Link example
GET api/analytic/?date_from=(ISO format datetime)&date_to=(ISO format datetime)

response: likes amount aggregated by date(not Like objects, just numbers)
