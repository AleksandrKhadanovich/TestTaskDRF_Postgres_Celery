# support backend service

## Usage

### After docker is ran admin user is created:
username: Admin
password : 123
email : admin@gmail.com

### To create user:
url: http://127.0.0.1:8000/api/v1/support/usernew/
Necessary data:

"username": "",
"email": "",
"password": ""

### To obtain JWT token for existing user:
url: http://127.0.0.1:8000/api/v1/support/usernew/
Necessary data:
"username": "",
"password": ""

### To view user's own tickets and support answers:
url: http://127.0.0.1:8000/api/v1/support/new/
Necessary data:
"comment":""
JWT token authorization

### To view user's own tickets and support answers:
url: http://127.0.0.1:8000/api/v1/support/list/
JWT token authorization

### To view user's tickets:
url: http://127.0.0.1:8000/api/v1/support/lstadm/
JWT token authorization

### To view one of tickets, send answers, change ticket's status:
url: http://127.0.0.1:8000/api/v1/support/lstadm/pk
where pk is comment's id
JWT token authorization


## License
Freeware license
