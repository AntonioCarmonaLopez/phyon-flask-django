
 

function validarLoginChat() {
    txtUsuario = document.getElementById("txtUsuario");
    slcSala = document.getElementById("slcSala").value;
if (txtUsuario.value == ''){
    txtUsuario.style.border = "solid 1px red";
    alert("Usuario vacio");
    return false;
} else {
    localStorage.setItem('usuario', txtUsuario.value);
    localStorage.setItem('sala', slcSala);
    return true;
    }
}

function recuperarInfo() {
    let info = localStorage.getItem('usuario')+' en '+localStorage.getItem('sala');
    const h1 = document.createElement('h1');
    h1.innerHTML = info;
    document.querySelector('#titulo').append(h1);
}
