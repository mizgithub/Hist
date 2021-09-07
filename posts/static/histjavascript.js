function login(){
	var form=new FormData(document.getElementById('loginForm'));
	var http = new XMLHttpRequest();
        http.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
              
                $("#auditsearchres").html(this.responseText);
            }
        };
        http.open("POST", "login", true);
        http.send(form);
}
function signup(){
	var form = new FormData(document.getElementById('signupForm'));
	var http= new XMLHttpRequest();
	http.onreadystatechange=function() {

		if(this.readyState == 4 && this.status == 200) {

			document.getElementById("errorMessage").innerHTML=this.responseText;
		}
	}
	http.open("POST","{% url 'signup' %}", true);
	http.send(form);
}