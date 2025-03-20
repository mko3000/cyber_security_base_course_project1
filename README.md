# Web app with vulnerabilities
Project I for the Cyber Security Base 2025 course

## Assignment
A Django web app that must include five vulnerabilities from the OWASP top ten list https://owasp.org/www-project-top-ten/.

## Description
The app can be used to post messages on a message wall with the poster's name visible under the message. The app has a login/register function. The user can open an account page where they can see the messages they have posted and delete messages.

## Installation
1. Navigate to the directory you wish to save the program in the command line.
1. run ```git clone https://github.com/mko3000/cyber_security_base_course_project1.git```
1. run ```python3 manage.py migrate```
1. run ```python3 manage.py runserver```


## Vulnerability report

### Flaw 1: Insecure design (A04:2021)
There are multiple insecure design choices:
1. When logging in, if the user enters a nonexisting username they are informed that that user doesn't exist. And if the user enters a wrong password for an existing user, they are informed that the password is wrong. This can help an attacker to identify valid usernames and try passwords for those users.
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/views.py#L32
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/views.py#L38

    ***Fix***\
Don't specify which part of the credentials is wrong. Instead, prompt something like: "Wrong credentials. Try other credentials or register a new user"
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/fixed/fixed_views.py#L27

1. The app does not use Django's in-built User model and the authentication tools. The user id of the current user is stored in cookies in a plain text format using a super simple formula: id_username (for example "321_alice").
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/views.py#L48

    ***Fix***\
Instead of creating your own solution for user authentication, use Django's default solutions which are more secure. These include the User model and the login, logout and authenticate methods.
https://github.com/mko3000/cyber_security_base_course_project1/blob/e18d66fc18fd698b3179c7122c03fb8fe9b6ff79/msgboard/fixed/fixed_views.py#L46-L48
https://github.com/mko3000/cyber_security_base_course_project1/blob/e18d66fc18fd698b3179c7122c03fb8fe9b6ff79/msgboard/fixed/fixed_views.py#L62
https://github.com/mko3000/cyber_security_base_course_project1/blob/e18d66fc18fd698b3179c7122c03fb8fe9b6ff79/msgboard/fixed/fixed_views.py#L69

1. csft tokens are not used. In fact, all the views that handle post requests have a @csrf_exempt decorator added.
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/views.py#L59

    ***Fix***\
Enable csrf tokens. Django enforces csrf tokens by default and removing the @csrf_exempt decorators turns on the enforcement. If csrf token is missing in the page template's post forms, Django will warn the developer.

1. Logging in is not required for sending messages. If unregistered users can post messages, it's much more difficult to enforce any policies about not posting harmful material and attackers have easier access for trying to use the message input field for injection attacks, for example.

    ***Fix***\
Add a @login_required constructor for message sending and account views.
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/fixed/fixed_views.py#L51
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/fixed/fixed_views.py#L56


### Flaw 2: Identification and Authentication Failures (A07:2021)

The app has at least these identification and authentication failures:
1. Exposes session identifier in the URL. The user account pages can be accessed by using the username in the URL like this ```/account/?user=alice``` and searching the BadUser table by filtering with the username to get the user object.
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/views.py#L78-L79

    ***Fix***\
Instead of getting the user from the URL we could get the user from the request. This is much easier to implement and safer.
https://github.com/mko3000/cyber_security_base_course_project1/blob/352fff04190c740ecee195ddff985a584e80f412/msgboard/fixed/fixed_views.py#L84

1. Password length or complexity are not enforced. It's easier for the attacker to test, for example, common passwords and passwords reminding the username. Even a random password is possible to crack by cycling through possible strings if it's short.

    ***Fix***\
We can use Django's default password validators UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator, and NumericPasswordValidator. They check if the password is too similar to the username, if the password is long enough (default minimum length = 8), if the password is found in a common passwords list, and if the password is completely numeric. A validate_passwords method implementing these checks was added to views. https://github.com/mko3000/cyber_security_base_course_project1/blob/352fff04190c740ecee195ddff985a584e80f412/msgboard/fixed/fixed_views.py#L16


### Flaw 3: Cryptographic failures (A02:2021)
The user data, including passwords, is stored in the database in plain text. If an attacker got access to the app's database, they could easily read the passwords in the user table.
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/views.py#L48
https://github.com/mko3000/cyber_security_base_course_project1/blob/352fff04190c740ecee195ddff985a584e80f412/msgboard/models.py#L13-L15

In addition, the app doesn't use an encrypted sessionid to keep track of the user's session. Instead, a plain text user identifier cookie is used.  The method of how the user_id cookie is generated is easy to guess and an attacker could set their own cookie following the simple logic and pose as the user.
https://github.com/mko3000/cyber_security_base_course_project1/blob/0dd72f4c38746e753ecf278141cfb9e6878e8c5f/msgboard/views.py#L50-L51

***Fix***\
Use Django's in-built User model, which has the passwords encrypted. Instead of using a plain text user_id as a session token, use the sessionid available in the request object.
https://github.com/mko3000/cyber_security_base_course_project1/blob/352fff04190c740ecee195ddff985a584e80f412/msgboard/fixed/fixed_models.py#L2

### Flaw 4: Broken access control (A01:2021)
An attacker can access any user's messages by entering the user's username in the account page's URL as a parameter. In the account page, the correct user access is not confirmed and the attacker can delete the user's messages, which should be possible only for the user themself.
https://github.com/mko3000/cyber_security_base_course_project1/blob/352fff04190c740ecee195ddff985a584e80f412/msgboard/views.py#L84-L87

***Fix***\
A more secure way is to attain the user from the request. This method uses the encrypted sessionid token and ensures that only the messages from the user are displayed on the account page. An additional check can be made when deleting a message.
https://github.com/mko3000/cyber_security_base_course_project1/blob/e18d66fc18fd698b3179c7122c03fb8fe9b6ff79/msgboard/fixed/fixed_views.py#L94-L95

### Flaw 5: Insufficient logging and monitoring (A09:2021)
No logging feature has been implemented. An attacker could use brute force to try passwords and it would remain unnoticed. Also, a user could post inappropriate messages on the message board and it would be difficult to block, for example, their ip address, because that data is not collected. In addition, there is no moderation.

***Fix***\
Logging could be added for example, when a user logs in and out and when a login fails. Django provides tools for this. I implemented a method for logging failed login attempts, which logs the IP address where the attempt came from.
https://github.com/mko3000/cyber_security_base_course_project1/blob/38b00609b0d79cb9e37f2b7fbc19b366f3a3d194/msgboard/fixed/fixed_views.py#L14-L27
https://github.com/mko3000/cyber_security_base_course_project1/blob/38b00609b0d79cb9e37f2b7fbc19b366f3a3d194/msgboard/fixed/fixed_views.py#L66-L67
https://github.com/mko3000/cyber_security_base_course_project1/blob/38b00609b0d79cb9e37f2b7fbc19b366f3a3d194/msgboard/fixed/fixed_views.py#L72-L73

In the case of a public message board app, someone should monitor the logs and moderate message content. I did not hire a moderation team :)


