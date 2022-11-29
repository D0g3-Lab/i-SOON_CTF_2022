<html>
<body>
<form method="POST" enctype="multipart/form-data">
这前端不美si你！！！
<input type="file" name="upload_file" />
<input type="submit" name="submit" value="submit" />
</form>
</body>
</html>
<?php
function waf($var): bool{
    $blacklist = ["\$_", "eval","copy" ,"assert","usort","include", "require", "$", "^", "~", "-", "%", "*","file","fopen","fwriter","fput","copy","curl","fread","fget","function_exists","dl","putenv","system","exec","shell_exec","passthru","proc_open","proc_close", "proc_get_status","checkdnsrr","getmxrr","getservbyname","getservbyport", "syslog","popen","show_source","highlight_file","`","chmod"];

    foreach($blacklist as $blackword){
        if(stristr($var, $blackword)) return True;
    }

    return False;
}
error_reporting(0);
//设置上传目录
define("UPLOAD_PATH", "./uploads");
$msg = "Upload Success!";
if (isset($_POST['submit'])) {
$temp_file = $_FILES['upload_file']['tmp_name'];
$file_name = $_FILES['upload_file']['name'];
$ext = pathinfo($file_name,PATHINFO_EXTENSION);
if(!preg_match("/php/i", strtolower($ext))){
die("俺不要图片,熊大");
}

$content = file_get_contents($temp_file);
if(waf($content)){
    die("哎呦你干嘛，小黑子...");
}
$new_file_name = md5($file_name).".".$ext;
        $img_path = UPLOAD_PATH . '/' . $new_file_name;


        if (move_uploaded_file($temp_file, $img_path)){
            $is_upload = true;
        } else {
            $msg = 'Upload Failed!';
            die();
        }
        echo $msg."  ".$img_path;
}