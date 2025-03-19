#Web app with five vulnerabilities
Project I for the Cyber Security Base 2025 course

##Assignment
A django web app that must inlcude five vulnerabilities from the OWASP top ten list https://owasp.org/www-project-top-ten/

##Description
The app can be used to post messages on a message wall with the poster's name visible under the message. The app has a login/register function. The user can open an account page where they can see the messages they have posted and delete messages.

##Installation:
1. Navigate to the directory you wish to save the program in the command line.
1. run "git clone https://github.com/mko3000/cyber_security_base_course_project1.git"
1. run "python3 manage.py migrate"
1. run "python3 manage.py runserver"


##Planned vulnerabilities

### Flaw 1: Insecure design (A04:2021)
There are multiple insecure design choices:
1. When logging in, if the user enters an non existing username they are informed that that user doesn't exist.
1. If the user enters a wrong password for an existing user, they are informed that the password was wrong.
1. The app does not use django's in-built User model and the authentication tools. The user id of the current user is stored in cookies in a plain text format using a a super simple formula: id_username (for example "321_alice").
1. csft tokens are not used. In fact, all the views that handle post request have a @csrf_exempt decorator added.
1. Logging in is not required for sending.
1. Django's admin functionality is not used.

### Flaw 2: Identification and Authentication Failures (A07:2021)

The app has at least these identification and authentication failures:
1. Permits brute force or other automated attacks.
1. Password length or complexity are not enforced.
1. Exposes session identifier in the URL. The user account pages can be accessed by using the username in the URL like this: /account/?user=alice.

### Flaw 3: Cryptographic failures (A02:2021)
The user data, including passwords, is stored in the database in plain text. Also the session token is not used but a plain test user identfier cookie is used instead.

### Flaw 4: Broken access control (A01:2021)
An attacker can access any user's messages by entering the user's username in the account page's url as a parameter. In the account page, the correct user access is not confirmed and the attacker can delete the user's messages which should be possible only for the user themself.

### Flaw 5: Insufficient logging and monitoring (A09:2021)
No logging feature has been implemented. An attacker could use brute force attacks to try passwords and it would remaing unnoticed. Also, a user could post inpropriate messagas on the message board and it would be difficult to block for example their ip address, because that data is not collected. In addition, there is no moderation.

- Insecure design
    - tells if password is wrong but username correct
    - user id saved in cookies in plain text using a super simple formula: id_username (for example "321_alice")
    - csfr token not used
- Identification and Authentication Failures
    - permits brute force or other automated attacks.
    - password length or complexity not enforced
    - exposes session identifier in the URL.
- Crytographic failures
    - password as plain text
- Broken access control
    - can get to other user's account page trough url and delete their messages.
- Insufficient logging
    - not logging anything


