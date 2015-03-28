<?php
$target_dir = "/tmp/";
$target_file = $target_dir . basename($_FILES['upload_file']['name']);

// check file exist
  if (file_exists($target_file) ) {
    echo "The file had been existed";
  }
// move tmpfile to destination
  else if (move_uploaded_file($_FILES['upload_file']['tmp_name'], $target_file) ) {
    echo "The file " . basename( $_FILES['upload_file']['name']) . " has been uploaded";
  }
  else{
    echo "There was an error uploading the file, please try again!";
  }
?>