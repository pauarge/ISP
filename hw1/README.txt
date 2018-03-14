Ex 1:
The JS code checks if the password entered by the user is equal to the output of the function superencryption with the params email and mySecureOneTimePad. Therefore, to bypass the system, the password must the the output of that function. Calling it with the required parameters in the browser console is trivial.

Ex 2:
First, login with the email and whatever password. That login form stores a cookie in the browser called LoginCookie, which is used to verify access for the protected areas. Once logged in, clicking to each character doesn't matter. It only matters if the cookie is correct. The cookie is encoded in base64. Change the "user" string by "administrator", reencode the cookie and do the request with the new cookie.

Ex3: 
Run dockers and interceptor.py. When it finds the result, it makes the request and prints the token.

Ex4:
Run dockers and interceptor2.py. It keeps printing the matching tokens, and when 5 are available, simply paste them in a request to the server (for instance in Postman).