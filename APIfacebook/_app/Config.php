<?php

session_start();
require_once 'Facebook/autoload.php';

$fb = new Facebook\Facebook([
    'app_id' => '414700660515073',
    'app_secret' => 'd146af89ae0e67e4c1ee3c2027b87285',
    'default_graph_version' => 'v2.7',
        ]);

