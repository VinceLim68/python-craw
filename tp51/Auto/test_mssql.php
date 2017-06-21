<?php
//phpinfo();
$serverName = "(192.168.1.3)"; 
$connectionInfo = array( "UID"=>"sa", 
"PWD"=>"sa", 
"Database"=>"Evalue"); 
 
$conn = sqlsrv_connect( $serverName, $connectionInfo); 
if( $conn ) 
{ 
echo "Connection established.n"; 
} 
else 
{ 
echo "Connection could not be established.n"; 
die( print_r( sqlsrv_errors(), true)); 
} 


?>