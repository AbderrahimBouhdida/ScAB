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
$sql = "SELECT last_beat FROM heartbeat WHERE id = 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
		$time = $row["last_beat"];
    }
} else {
    echo "0 results";
}
$diff = abs(strtotime($time)-time());

$conn->close();
$colo = "#962323";
$state = "offline";
if($diff >15){
	$etat = "Offline";
	$colo = "#962323";

}
else {
	$etat = "Online";
	$colo = "#00FF00";
	$t = "";
}

 ?>
<span style="
    background-color: <?php echo $colo;?>;
    border: inset;" class = "dot">



    <h3><?php echo $state;?></h3>
		


</span>
