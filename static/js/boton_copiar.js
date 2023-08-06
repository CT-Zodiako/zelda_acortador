// mi_script.js
function redirigirALanding() {
    window.location.href = "/";
}

function copiarUrl() {
    let url = document.getElementById("shorulr");
    let button = document.getElementById("bottoncopiar");

    navigator.clipboard.writeText(url.value).then(function() {    
        button.innerHTML = "Copiado";
    }, function() {
        button.innerHTML = "Error";
    });
}
