<?php
include('session.php');
?>

<html>
<head>
    <title>TEST</title>
<?php
    $content = file_get_contents('php://input');
    $data = json_decode($content);
//    echo $content;
//    var_dump($content);
//    echo $data;
//    var_dump($data);
?>
</head>

<body>
    Hi, <?php echo $data->name; ?>
    <br />You are <?php echo $data->age; ?> years old.

</body>
</html>
