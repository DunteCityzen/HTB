$username = 'tstark'
$password = 'playboy69'

$secpasswd = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ($username, $secpasswd)

Start-Process -FilePath "powershell.exe" -Credential $credential -NoNewWindow
