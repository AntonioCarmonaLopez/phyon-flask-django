function validacionLogin (){
    txtNombre = document.getElementById("txtNombre").value;
    txtPass = document.getElementById("txtPassword").value;
    if( txtNombre == null || txtNombre.length == 0) {
        txtNombre.style.border = "solid 1px red";
        alert("Nombre vacio");
        return false;
    } else if(pass == null || pass.length == 0) {
        txtPass.style.border = "solid 1px red";
        alert("Contrasela vacia");
        return false;
    }
    return true;
}

function validacionLogup (){
    txtNombre = document.getElementById("txtNombre").value;
    txtPass = document.getElementById("txtPassword").value;
    txtPass2 = document.getElementById("txtPassword2").value;
    if( txtNombre == null || txtNombre.length == 0) {
        txtNombre.style.border = "solid 1px red";
        alert("Nombre vacio");
        return false;
    } else if(txtPass == null || txtPass.length == 0) {
        txtPass.style.border = "solid 1px red";
        alert("Contrasela vacia");
        return false;
    } else if(txtPass.length < 9) {
        txtPass.style.border = "solid 1px red";
        alert("Contrasela menor de 8 caracteres");
        return false;
    }else if(txtPass2 != txtPass) {
        txtPass.style.border = "solid 1px red";
        txtPass2.style.border = "solid 1px red";
        alert("Las contraseñoa no coiciden");
        return false;
    }
    return true;
}

function validacionActualizar (){
    txtOrigen = document.getElementById("txtOrigen").value;
    txtDestino = document.getElementById("txtDestino").value;
    txtDuracion = document.getElementById("txtDuracion").value;
    if( txtOrigen == null || txtOrigen.length == 0) {
        txtOrigen.style.border = "solid 1px red";
        alert("Origen vacio");
        return false;
    } else if(txtDestino == null || txtDestino.length == 0) {
        txtDestino.style.border = "solid 1px red";
        alert("Destino vacio");
        return false;
    } else if(txtDuracion == null || txtDuracion.value < 27000) {
        txtDuracion.style.border = "solid 1px red";
        alert("Duración incorrecta");
        return false;
    }
    return true;
}
function habilitarDeshabilitar() {
    let txtOrigen = document.getElementById("txtOrigen");
    let txtDestino = document.getElementById("txtDestino");
    let txtDuracion = document.getElementById("txtDuracion");
    let btnActualizar = document.getElementById("btnActualizar");
    let btnEditar = document.getElementById("btnEditar");
    let btnCancelar = document.getElementById("btnCancelar");
    if (txtOrigen.disabled == true){
        txtOrigen.disabled = false;
        txtDestino.disabled = false;
        txtDuracion.disabled = false;
        btnActualizar.disabled = false;
        btnCancelar.disabled = false;
        btnEditar.disabled = true;
    } else {
        txtOrigen.disabled = true;
        txtDestino.disabled = true;
        txtDuracion.disabled = true;
        btnActualizar.disabled = true;
        btnCancelar.disabled = true;
        btnEditar.disabled = false;
    }
}
function borrar(vuelo_id) {
    if (confirm('¿Realmente deseas borrar el vuelo?')) {
          $.ajax({
            method: "GET",
            url: "http://127.0.0.1:5000/borrar/"+vuelo_id
          })
          
    }
}
 