async function makeRequest(url, method = 'GET') {
        let response = await fetch(url, {"method": method});
        if (response.ok) {
            return await response.json();
        } else {
            let error = new Error(response.statusText);
            error.response = response
            console.log(error)
            throw error;
        }
    }

    async function onClick(event){
        event.preventDefault()
        let button = event.target
        let url = button.dataset.articlesUrl
        console.log(url);
        let test = await makeRequest(url);
        console.log(test)
        console.log(test.test)
        console.log(test.test2)
    }


    function onLoad() {
        let button = document.getElementById("button")
        button.addEventListener('click', onClick)
    }

    window.addEventListener('load', onLoad)