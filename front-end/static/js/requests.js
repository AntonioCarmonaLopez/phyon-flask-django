      // renderiza el contenido de la nueva pagina
      function load_page(name) {
        const request = new XMLHttpRequest();
        let url = `/articulo/${name}`
        request.open('GET', url);
        request.onload = () => {
            alert(name)
            const response = request.responseText;
            document.querySelector('#body').innerHTML = response;
    
            //empujar a la barra de direcciones y titulo de la pagina
            // la url soble la que se ha echo click
            document.title = url;
           history.pushState({'title': url, 'text': response}, url, url);
        };
        request.send();
    }


