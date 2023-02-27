import socket
import signal
import sys
import random

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "password" value = "new" />
   <input type = "submit" value = "Click here to Change Password" />
   </form>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % (port, port)

new_password_page = """
   <form action="http://localhost:%d" method = "post">
   New Password: <input type = "text" name = "NewPassword" /> <br/>
   <input type = "submit" value = "Submit" />
</form>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print("Here is the {}".format(tag))
    print("\"\"\"")
    print(value)
    print("\"\"\"")
    print()

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
login_details = {}
with open('passwords.txt', 'r') as f:
    for line in f:
        user, password = line.split()
        login_details[user] = password

# Read secret data of all the users
secret_data = {}
with open('secrets.txt', 'r') as f:
    for line in f:
        user, secret = line.split()
        secret_data[user] = secret

cookie_store = {}

### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    # TODO: Put your application logic here!
    # Parse headers and body and perform various actions
    # You need to set the variables:
    # (1) `html_content_to_send` => add the HTML content you'd like to send to the client.
    # Right now, we just send the default login page.
    html_content_to_send = login_page
    # But other possibilities exist, including
    # html_content_to_send = success_page + <secret>
    # html_content_to_send = bad_creds_page
    # html_content_to_send = logout_page

    # (2) `headers_to_send` => add any additional headers you'd like to send the client?
    # Right now, we don't send any extra headers.
    headers_to_send = ''

    # Check if cookie is present
    # print("HEADERS SPLIT\n====================")
    # print(headers.split('\r\n'))
    cookie = ''
    if 'Cookie' in headers:
        cookie = headers.split('\r\n')
        for line in cookie:
            if 'Cookie' in line:
                cookie = line.split(' ')[1].split('=')[1]
                print("COOKIE: " + cookie)
                break
        # print("COOKIE: " + cookie)
        for user in cookie_store:
            if cookie_store[user] == int(cookie):
                html_content_to_send = success_page + secret_data[user]
            else:
                html_content_to_send = bad_creds_page
                

    if body:
        body = body.split('&')
        body = [x.split('=') for x in body]
        body = {x[0]: x[1] for x in body}

        # print_value('body', body)
        if 'action' in body and body['action'] == 'logout':
            html_content_to_send = logout_page
            # Remove cookie
            headers_to_send = 'Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n'
        elif 'password' in body and body['password'] == 'new' and len(body) == 1 and cookie:
            html_content_to_send = new_password_page
        elif 'NewPassword' in body and len(body) == 1:
            # login_details[body['username']] = body['NewPassword']
            # find username from current cookie
            for user in cookie_store:
                if cookie_store[user] == int(cookie):
                    login_details[user] = body['NewPassword']
                    html_content_to_send = success_page + secret_data[user]
                    break
        elif 'username' in body and 'password' in body:
            if body['username'] in login_details and login_details[body['username']] == body['password']:
                html_content_to_send = success_page + secret_data[body['username']]

                # Set cookie
                rand_val = random.getrandbits(64)
                headers_to_send = 'Set-Cookie: token=' + str(rand_val) + '\r\n'
                cookie_store[body['username']] = rand_val
            else:
                html_content_to_send = bad_creds_page
        else:
            html_content_to_send = bad_creds_page

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
    
    print("Served one request/connection!")
    print()

# We will never actually get here.
# Close the listening socket
sock.close()
