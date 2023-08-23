async function makeRequest(url, data = {}, method = 'GET') {
    let headers = {};
    let response;

    console.log(getCookie("token"))
    if (method !== "GET") {
        headers = {
            'Authorization': `Token ${getCookie("token")}`,
            "Content-Type": "application/json",
        }
    }

    if (["POST", "PATCH", "PUT"].includes(method)) {
        response = await fetch(url, {
            "method": method,
            "headers": headers,
            "body": JSON.stringify(data)
        });
    } else {
        response = await fetch(url, {
            "method": method,
            "headers": headers,
        });
    }

    if (response.ok) {
        return await response.json();
    } else {
        console.log(response.statusText)
        let error = new Error(response.statusText);
        throw error;
    }
}

async function onClick(event) {
    let response = await makeRequest(
        "http://localhost:8000/api/v3/articles/80/",
        {"title": "111133", "content": "2222"},
        "PUT"
    );
    console.log(response)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function onLoad() {
    let button = document.getElementById("button")
    button.addEventListener("click", onClick)
}

window.addEventListener('load', onLoad)