<?php
include('session.php');
?>

<html>
  <body>

    <p>GET:</p>
    <form action="get.php" method="get">
    name: <input type="text" name="name_php" />
    age: <input type="text" name="age_php" />
    <input type="submit" />
    </form>
    <br/ >

    <p>POST:</p>
    <form action="post.php" method="post">
    name: <input type="text" name="NAME_PHP" />
    age: <input type="text" name="AGE_PHP" />
    <input type="submit"/>
    </form>
    <br />

<!--
    <p>JSON:</p>
    <form action="json.php" method="post" enctype='application/json'>
    name: <input type="text" name="name"/>
    age: <input type="text" name="age"/>
    <input type="submit"/>
    </form>
    <br>
-->

    <p>UPLOAD:</p>
    <form action="upload.php" method="post" enctype="multipart/form-data">
    select file to upload: <input type="file" name="upload_file" id="upload_file" />
    <input type="submit" name="submit" />
    </form>
    <br />

    <input type="button" value="logout" onclick="javascript:location.href='logout.php'" />

  </body>
</html>
