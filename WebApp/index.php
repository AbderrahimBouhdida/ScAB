<?php 
	session_start();
	if(!empty($_SESSION['user'])) {
	header("Location: overview/view.php",TRUE,301);
	}?>
<!-- saved from url=(0047)file:///C:/Users/GEEK-TN/Desktop/web/index.html -->
<html><head><meta http-equiv="Content-Type" content="application/html; charset=UTF-8">
<title>FACE RECOGNIZER V1.0 - LOGIN</title>
<!-- For-Mobile-Apps -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<meta name="keywords" content="Dark Login Form Widget Responsive, Login Form Web Template, Flat Pricing Tables, Flat Drop-Downs, Sign-Up Web Templates, Flat Web Templates, Login Sign-up Responsive Web Template, Smartphone Compatible Web Template, Free Web Designs for Nokia, Samsung, LG, SonyErricsson, Motorola Web Design">
<script type="application/x-javascript"> addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>
<!-- //For-Mobile-Apps -->
<!-- Style --> <link rel="stylesheet" href="css/style_login.css" type="text/css" media="all">

<link rel='shortcut icon' type='image/x-icon' href='../images/Pi.ico' />


</head>
<body>
<div class="container"> 
<h1>FACE RECOGNIZER v1.0</h1>
<h2>BY : JIHED CHAIBI & ABDERRAHIM BOUHDIDA</h2>
<h2>LFEEA3 - FSM - 2018</h2>
     <div class="contact-form">
	 <div class="signin">
     <form action="login.php" method="POST">
	      <p>Username</p>
	      <input type="text" name="user" class="user" value="Enter Here" onfocus="this.value = &#39;&#39;;" onblur="if (this.value == &#39;&#39;) {this.value = &#39;Enter Here&#39;;}">
		  <p>Password </p>
		  <input type="password" name="pass" class="pass" value="Password" onfocus="this.value = &#39;&#39;;" onblur="if (this.value == &#39;&#39;) {this.value = &#39;Password&#39;;}">
			<p><?php if(!empty($_GET['message'])) 
				echo "Login Failed !";
				?><p>
          <input type="submit" value="Submit">
	 </form>
	 </div>
	 </div>
</div>
<div class="footer">

</div>

</body></html>
