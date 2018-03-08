<?php
include('login.php');

if (isset($_SESSION['login_user']) ) {
    header("location: action.php");
}

?>

<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>

    <form action="" method="post">
    <label>Username:</label>
    <input name="username" placeholder="username" type="text" />
    <br />
 
    <label>Password:</label>
    <input name="password" placeholder="********" type="password" />
    <br />

    <input name="submit" type="submit" value=" Login " />
    <br />

    <span><?php echo $error; ?></span>
    </form>

</body>
</html>
