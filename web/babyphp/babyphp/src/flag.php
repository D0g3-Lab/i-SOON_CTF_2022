<?php
session_start();
highlight_file(__FILE__);
//flag在根目录下
if($_SERVER["REMOTE_ADDR"]==="127.0.0.1"){
    $f1ag=implode(array(new $_GET['a']($_GET['b'])));
    $_SESSION["F1AG"]= $f1ag;
}else{
   echo "only localhost!!";
}
