function Get-WebCredentials
{
[CmdletBinding()] Param ()


$ClassHolder = [Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime]
$VoltObj = new-object Windows.Security.Credentials.PasswordVault
$VoltObj.RetrieveAll() | foreach { $_.RetrievePassword(); $_ }
}