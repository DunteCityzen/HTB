# OFFICE MY WALKTHROUGH
## Service enumeration
* nmap found a bunch of services, and directories in robots.txt.
* Joomla website.

## Looking for CVEs
* Found some interesting endpoints to interact with for extra information eg:
	version - http://10.10.11.3/administrator/manifests/files/joomla.xml
	sensitive dbinfo - http://10.10.11.3/api/index.php/v1/config/application?public=true
		rootuser:<password>
	sensitive userinfo - http://10.9.49.205/api/index.php/v1/users?public=true
		Superuser to allow login as admin into the webapp.
		
## Considering other options
### Port 88 - kerberos.
* Kerberos is a an network authenication protocol that works by checking credentials and gives tickets that grants user access to services in the network.
* It uses a trusted 3rd party, key distribution center, to authenticate users to services using a secure ticketing system thereby ensuring that passwords never touch the wire.

* Kerbrute - is a tool used to guess a list of usernames that are recognized by the key distribution center without needing a password.

* So after using this tool with a wordlist from seclist/usernames/xato......... (not the duplicate one) I found valid usernames and created a script to get the usernames part only (frank@domain.local -> frank) and store in a file.

* We have usernames, now what? How do we gain access with these? We can't we don't have any passwords yet. Or do we? Remember the password we got from using the cve-2023-23752.py exploit script to get credentials from Joomla unauthenticated. The one from the db config details -> root:<password>. Yeah!

### Using kerbrute to perform passwordspraying
* This was to figure out if any of those valid usernames we got from kerbrute earlier reused the db's root user password.
* Indeed, one of the user's matched.

### Initial access with psexec(! Failed)
* This failed since the user's credentials we found doesn't have write permissions in any of the available shares.

### Other options
* We are not able to write, but can we read the shares though? Using smbclient -U <user> -L \\host.
* Then after listing the shares, spotted a non-default share, Soc analysis and in there found a pcap file which we exfiltrated.
* An analysis of the file revealed SMB communication and kerberos communication as well. Perfect. Using `tshark -r <pcapfile> -Y kerberos -V | grep cipher` yielded a comprehensive response containing all the information in the packets. Found the Ciphertext and the encryption algorithm in the packets' data and together with the username and protocol version a hash was curated and cracked by hashcat + rockyou.txt wordlist. The decrypted password was => <redacted>. This password had been reused as the Administrator user in the content management system, Joomla.

### Initial access via php webshell
* On the content management system, we were able to edit the templates and edited the error.php template with php code that downloaded a reverse_tcp msfvenom payload from our machine and executed it to get a meterpreter session that we had setup with the payload accordingly.

### Switching users
* Ran a metersploit post exploitation module `post/windows/manage/run_as_psh` and got access to cmd as tstark. From here we found the flag in his Desktop location.


## Escalating privileges
### Enumeration
* Downloaded winpeas from our machine and executed to get paths to root user(Administrator).
* Listed all directories recursively from `C:\` and Libre Office caught my eye.
* Listed the listeninng ports and discovered an interesting port that did not appear in the nmap scan.
* Setup a remote tunnel using chisel to a port on my localhost and accessed the service behind the port from my browser, it was a web service.
