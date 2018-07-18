<?php
	session_start();
	if(empty($_SESSION['user'])) {
	header("Location: ../index.php",TRUE,301);
	die();
}
?>
<!-- saved from url=(0078)file:///C:/Users/GEEK-TN/Desktop/PFE/INTERFACES%20WEB/ADMIN/5-10-2018/PFA.html -->
<html><head><meta http-equiv="Content-Type" content="text/javascript; charset=UTF-8">



<title>ADMIN INTERFACE</title>

<!-- For-Mobile-Apps -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<script type="application/x-javascript"> addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>
<!-- //For-Mobile-Apps -->
<!-- Style --> <link rel="stylesheet" href="./admin_interface_files/style.css" type="text/css" media="all">



<script src="https://code.jquery.com/jquery-2.1.1.min.js" type="text/javascript"></script>


<link rel='shortcut icon' type='image/x-icon' href='../images/Pi.ico' />




</head>

<body>

<h1 style="display: block;position: relative;max-width: 63%;max-height: 100%;font-size: 22px;">Welcome, <?php echo $_SESSION['user'];?></h1>
<form action = "out.php" method = "POST">
<input class="button" type="submit" value = "Logout">
</form>


<div class="container" style="
">

     <div class="camera-form" style="margin-top: 17px;float: left;margin-left: 28px;margin-right: 25px;display: inline-block;max-width: 81%; width:570px ">
	       

        <h2> ETAT DE SYSTEME </h2>

           <br>

        <span 
         id="dot_AJAX">
        </span>
   

<!-- SCRIPT DE REFRAICHEMENT -->

<script language="javascript" type="text/javascript">

function loadlink2(){
    $('#dot_AJAX').load("test.php");
}

loadlink2(); // This will run on page load
setInterval(function(){
    loadlink2() // this will run after every 1 seconds
}, 1000); 




</script>

<!-- ----FIN SCRIPT------>
      
   
        <br>


        <button class="button2">START</button>

        <br>

     
<div class="onoffswitch">
    <input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" id="myonoffswitch" checked="">
    <label class="onoffswitch-label" for="myonoffswitch">
        <span class="onoffswitch-inner"></span>
        <span class="onoffswitch-switch"></span>
    </label>
</div>




	 </div>	 
	 



	 
<div id="links" class="dock1" style="margin-top: 18px;margin-right: 25px;margin-left: 20px;display: inline-block;overflow: overlay;max-width: 90%;">






	</div></div>




<!-- SCRIPT DE REFRAICHEMENT -->

<script language="javascript" type="text/javascript">

function loadlink(){
    $('#links').load('users.php',function () {
         $(this).unwrap();
    });
}

loadlink(); // This will run on page load
setInterval(function(){
    loadlink() // this will run after every 1 seconds
}, 1000); 




</script>

<!-- ----FIN SCRIPT------>






<div class="footer">
     
</div>

</body></html>