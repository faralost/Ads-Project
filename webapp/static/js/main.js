async function onClick(event) {
    event.preventDefault()
    let url = event.target.dataset.adUrl
    const settings = {
        method: 'POST',
        headers: {"X-CSRFToken": getCookie("csrftoken")},
    }
    let response = await fetch(url, settings)
    let answer = await response.json()
    let alertDiv = document.getElementById('alert')
    let status = document.getElementById('status')
    console.log(answer.answer)
    if (answer.answer === 'Опубликован'){
        alertDiv.style.display = 'block';
        alertDiv.className = 'alert alert-success mt-4'
        alertDiv.innerText = answer.answer;
        status.innerText = `Статус: Опубликовано`;
    } else if (answer.answer === 'Уже был опубликован') {
        alertDiv.style.display = 'block';
        alertDiv.className = 'alert alert-warning mt-4';
        alertDiv.innerText = answer.answer;
    } else if (answer.answer === 'Отклонен') {
        alertDiv.style.display = 'block';
        alertDiv.className = 'alert alert-success mt-4'
        alertDiv.innerText = answer.answer;
        status.innerText = `Статус: Отклонено`;
    } else {
        alertDiv.style.display = 'block';
        alertDiv.className = 'alert alert-warning mt-4'
        alertDiv.innerText = answer.answer;
    }
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