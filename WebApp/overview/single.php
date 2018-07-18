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
$my_date = date("Y-m-d H:i:s");
$sql = "INSERT INTO log (nom, prenom, departement, date) VALUES ('" . $_POST["name"] . "','" . $_POST["prenom"] . "','". $_POST["departement"] ."','".$my_date."')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
 ?>
