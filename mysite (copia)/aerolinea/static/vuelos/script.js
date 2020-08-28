function validacionLogin (){
    txtNombre = document.getElementById("txtNombre");
    txtPass = document.getElementById("txtPassword");
    if(txtNombre.value.length < 8) {
        txtNombre.style.border = "solid 1px red";
        alert("Nombre vacio");
        return false;
    } else if(pass.length < 8) {
        txtPass.style.border = "solid 1px red";
        alert("Contrasela vacia");
        return false;
    }
    return true;
}

function validacionLogup (){
    txtNombre = document.getElementById("txtNombre");
    txtEmail = document.getElementById("txtEmail");
    txtPass = document.getElementById("txtPassword");
    txtPass2 = document.getElementById("txtPassword2");
    if(txtNombre.value.length < 8) {
        txtNombre.style.border = "solid 1px red";
        alert("Nombre vacio");
        return false;
    } else if(txtPass.value.length < 8) {
            txtPass.style.border = "solid 1px red";
            alert("Contrasela vacia");
            return false;
    } else if(txtPass.value.length < 1) {
        txtEmail.style.border = "solid 1px red";
        alert("Email vacio");
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
