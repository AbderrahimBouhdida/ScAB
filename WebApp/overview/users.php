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
$result = mysqli_query($conn, "SELECT * FROM log")or die("Error: " . mysqli_error($connection));
$num_rows=mysqli_num_rows($result);
?>


<h4 style="
    font-family: sans-serif;
    font-size: x-small;
    color: #26974e;
    display: list-item;
    float: inherit;
    margin-bottom: 19px;
    text-align: -webkit-center;"> LISTE DES PERSONNES </h4>


 <table border="1" style="
    width: 500px;
    margin-left: 30px;
    margin-right: 23px;
    font-family: monospace;
    margin-bottom: 38px;
    text-align: left;
    font-size: unset;
    color:  white;
">
  <thead>
    <tr style="">

    <th>ID</th>
    <th>Nom</th>
    <th>Prenom</th>
    <th>Departement</th>
    <th>DATE
</th>
  </tr></thead>



  <tbody>

    <?php
      $counter = 1;
      // start 1st row

      while($row = mysqli_fetch_array($result)){
        echo "<tr>";
      // if the 4th cell, end last row, and start new row
          if ($counter%3==1){
              echo "</tr><tr>";
          }
          echo
          "<td >".$row['id']."</td>"
          ."<td>"
             ."<div>".$row['nom']."</div>"
          ."</td>"
		  ."<td>"
             ."<div>".$row['prenom']."</div>"
          ."</td>"
          ."<td>".$row['departement']."</td>"
          ."<td>".$row['date']."</td>"
          ."</tr>";
          // increase the counter
          $counter++;
      } ?>

  </tbody>




</table>
