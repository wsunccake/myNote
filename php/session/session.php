<?php
session_start();

// var_dump($_SESSION);

if (!isset($_SESSION['login_user']) ) {
    header("location: index.php");
    exit("Please login\n");
}
?>
