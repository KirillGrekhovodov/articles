async function makeRequest(url, method = 'GET') {
    let headers = {};
    if (method !== "GET"){
        const csrftoken = getCookie('csrftoken');
        headers = {'X-CSRFToken': csrftoken}
    }
    let response = await fetch(url, {
        "method": method,
        "headers": headers
    });
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.statusText);
        error.response = response
        console.log(error)
        throw error;
    }
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


async function onClick(event) {
    event.preventDefault();
    let target = event.target;
    let url = target.href;
    let articleId = target.dataset.articleId

    let method = "POST"
    if(target.innerText === "ДизЛайк") {
        method = "DELETE"
    }

    let response = await makeRequest(url, method);

    if(target.innerText === "Лайк"){
        target.innerText = "ДизЛайк";
    }
    else{
        target.innerText = "Лайк";
    }

    let spanCount = document.getElementById(`article_likes_count_${articleId}`)
    spanCount.innerText = response.count;
}


function onLoad() {
    let likes = document.getElementsByClassName("likes")
    for (let like of likes) {
        like.addEventListener("click", onClick)
    }
}

window.addEventListener('load', onLoad)