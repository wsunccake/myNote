<?php
session_start();

$error='';

if (isset($_POST['submit'])) {
    if (empty($_POST['username']) || empty($_POST['password'])) {
        $error = "Username or Password is invalid";
    }
    else {
        $username=$_POST['username'];
        $password=$_POST['password'];

        if ( ($username == 'testuser') and ($password == 'test1234') ){
            $_SESSION['login_user']=$username;
            header("location: action.php");
        }
        else {
            $error = "Username or Password is invalid";
        }
    }
}
?>

