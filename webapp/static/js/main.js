async function onClick(event) {
    event.preventDefault()
    let url = event.target.dataset.adUrl
    const settings = {
        method: 'POST',
        headers: {"X-CSRFToken": getCookie("csrftoken")},
    }
    let response = await fetch(url, settings)
    let answer = await response.json()
    console.log(answer)
}

function onLoad() {
    const buttons = document.querySelectorAll('.request')
    buttons.forEach(function (currentBtn) {
        currentBtn.addEventListener('click', onClick)
    })
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

window.onload = onLoad