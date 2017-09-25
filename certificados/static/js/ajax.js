function AjaxRequest(){
	if (window.XMLHttpRequest){
		try{
	        this.request = new XMLHttpRequest(); // Outros Navegadores
	    }catch(e){
	    	this.request = null;
	    }
    }
}

AjaxRequest.prototype.openGET = function(url, funcao){
	this.request.open('GET',url,true);
	this.request.send(null);
	this.request.onreadystatechange = funcao;
}

AjaxRequest.prototype.getReadyState = function() {
  return this.request.readyState;
}

AjaxRequest.prototype.getStatus = function() {
  return this.request.status;
}

AjaxRequest.prototype.getResponseText = function() {
  return this.request.responseText;
}

AjaxRequest.prototype.getResponseXML = function() {
  return this.request.responseXML;
}



function buscaCertificados(){
    $.ajax({
        url : "/certificados/bsc/", // the endpoint
        type : "POST", // http method
        data : { nome : $('#nome').val(),
                 csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val()
               }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            //var data_resp = JSON.parse(json);
            var encontrado = false;
            $('#resultado').html('');

            $.each(json, function(i, itemData){
                encontrado=true;
                console.log(itemData);
                $('#resultado').append('<p> <a target="_blank" href="/certificados/'+ itemData['id_c']+'">Download</a> <b>'+ itemData['nome'] +'</b>: '+ itemData['tipo'] +'</p>');

            });
            if(!encontrado){
                $('#resultado').append('<p Nome não encontrado!</p>');
            }


        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText + " - " + errmsg); // provide a bit more info about the error to the console
        }
    });
}
