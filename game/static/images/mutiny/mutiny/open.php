<?php
include ("y.php"); 
include("new/config.php");
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<link rel="stylesheet" type="text/css" href="co.css" />
<link rel="stylesheet" type="text/css" href="wow.css" />
<link rel="stylesheet" type="text/css" href="cs.css" />

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
</head>
 <font size="+2"><?php  echo "Recent Queries"; ?></font>
<div align="center">
     <div class="button_example">IIT-JEE / BITSAT</div><br /><BR />
 <?php
    $wer="select * from discuss where arbit='IIT-JEE' ORDER BY isnull(id),id DESC ";
  $a=mysql_query($wer) or die("Hello");
  ?>
  <table border="4" width="900" cellpadding="10px">
    <?php
	$c=0;
  while($qw=mysql_fetch_array($a))
  {
	  if($c==2)
	  {
		  break;
		  }
	 else
	 {?>
  <tr><td class="buttonsample">
  <font size="+1" class="buttonample" >
  <?php
   echo $qw[1];
   echo " asks";
   ?></font>
   <br/><br />
   <?php echo $qw[2] ?>
   <br/>
   <div align="right">
   <a class="button_example" target="B" href="post.php?valu=<?php echo $qw[0];?>">View / Reply</a></div>
   </td></tr>
  <?php
  $c++;
  }
  }
  ?>
  </table>
  <br />
   <div class="button_example">JEE MAIN/ STATE EXAM</div><br /><BR />
 <?php
    $wer="select * from discuss where arbit='WBJEE' ORDER BY isnull(id),id DESC ";
  $a=mysql_query($wer) or die("BHAK");
  ?>
  <table border="4" width="900" cellpadding="10px">
    <?php
	$c=0;
  while($qw=mysql_fetch_array($a))
  {
	  if($c==2)
	  {
		  break;
		  }
	 else
	 {?>
  <tr><td class="buttonsample">
  <font size="+1" class="buttonample" >
  <?php
   echo $qw[1];
   echo " asks";
   ?></font>
   <br/><br />
   <?php echo $qw[2] ?>
   <br/>
   <div align="right">
   <a class="button_example" target="B" href="post.php?valu=<?php echo $qw[0];?>">View / Reply</a></div>
   </td></tr>
  <?php
  
  }
  $c++;
  }
  ?>
  </table>
  <br />
     <div class="button_example">MISCELLANEOUS</div><br /><BR />
 <?php
    $wer="select * from discuss where arbit='arbit' ORDER BY isnull(id),id DESC ";
  $a=mysql_query($wer) or die("BHAK");
  ?>
  <table border="4" width="900" cellpadding="10px">
    <?php
	$c=0;
  while($qw=mysql_fetch_array($a))
  {
	  if($c==2)
	  {
		  break;
		  }
	 else
	 {?>
  <tr><td class="buttonsample">
  <font size="+1" class="buttonample" >
  <?php
   echo $qw[1];
   echo " asks";
   ?></font>
   <br/><br />
   <?php echo $qw[2] ?>
   <br/>
   <div align="right">
   <a class="button_example" target="B" href="post.php?valu=<?php echo $qw[0];?>">View / Reply</a></div>
   </td></tr>
  <?php
  $c++;
  }
  }
  ?>
  </table>
  
</body>
</html>