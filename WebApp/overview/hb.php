<?php
$servername = "localhost";
$username = "id6047718_tester";
$password = "123456789";
$dbname = "id6047718_test";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
if ($_POST["id"] == 1){
$sql = "UPDATE heartbeat set last_beat = now()";
if ($conn->query($sql) === TRUE) {
    echo "record updated successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}
}
$conn->close();
 ?>