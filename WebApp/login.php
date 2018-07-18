<?php
session_start();
$servername = "localhost";
$username = "id6047718_tester";
$password = "123456789";
$dbname = "id6047718_test";
$conn = new mysqli($servername, $username, $password, $dbname);

$myusername = mysqli_real_escape_string($conn,$_POST['user']);
$mypassword = mysqli_real_escape_string($conn,$_POST['pass']);

// Create connection

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$sql = "SELECT id FROM admin WHERE user = '$myusername' and pass = '$mypassword'";
$result = mysqli_query($conn,$sql);
$count = mysqli_num_rows($result);
if($count == 1) {
$_SESSION['user'] = $myusername;
          //echo "<script>location.href='/overview/view.php';</script>";
		  header("Location: overview/view.php",TRUE,301);
      }else {
			//echo "Your Login Name or Password is invalid";
			header("Location: index.php?message=error");
      }
$conn->close();
?>			

