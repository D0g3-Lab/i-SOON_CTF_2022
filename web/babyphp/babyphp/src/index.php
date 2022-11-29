<?php
//something in flag.php

class A
{
    public $a;
    public $b;

    public function __wakeup()
    {
        $this->a = "babyhacker";
    }

    public function __invoke()
    {
        if (isset($this->a) && $this->a == md5($this->a)) {
            $this->b->uwant();
        }
    }
}

class B
{
    public $a;
    public $b;
    public $k;

    function __destruct()
    {
        $this->b = $this->k;
        die($this->a);
    }
}

class C
{
    public $a;
    public $c;

    public function __toString()
    {
        $cc = $this->c;
        return $cc();
    }
    public function uwant()
    {
        if ($this->a == "phpinfo") {
            phpinfo();
        } else {
            call_user_func(array(reset($_SESSION), $this->a));
        }
    }
}


if (isset($_GET['d0g3'])) {
    ini_set($_GET['baby'], $_GET['d0g3']);
    session_start();
    $_SESSION['sess'] = $_POST['sess'];
}
else{
    session_start();
    if (isset($_POST["pop"])) {
        unserialize($_POST["pop"]);
    }
}
var_dump($_SESSION);
highlight_file(__FILE__);