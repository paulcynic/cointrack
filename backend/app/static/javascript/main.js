// Очистка списка
function clearList(){
	var divResult = document.getElementById("divResult");
	while (divResult.hasChildNodes())
		divResult.removeChild(divResult.lastChild);
}
// Добавление нового элемента списка
function addResultForm(text){
	if (text.length == 0) return;
	var divResult = document.getElementById("divResult");
    var p = document.createElement("p")
	divResult.appendChild(p);
	var pText = document.createTextNode(text);
	p.appendChild(pText);
}


function addResultString(text, p){
	if (text.length == 0) return;
	var pText = document.createTextNode(text);
	var br = document.createElement("br");
    p.appendChild(pText);
    p.appendChild(br);
}


function showPrice(){
	// Параметры поиска
    var form = document.forms.form
	var coin = form.querySelector("select[name=coin]").value;
	var currency = form.querySelector("select[name=currency]").value;
	// Формирование строки поиска
	var searchString = "coin=" + coin + "&" + "currency=" + currency;
	//alert("searchString: " + searchString);
	
	// Запрос к серверу
	var req = new XMLHttpRequest();
	req.onreadystatechange = function(){
			if (req.readyState != 4) return;
            var respText = req.responseText;
            var resObj = JSON.parse(respText);
            var responseText = String(coin) + ": " + String(resObj[coin][currency]) + " " + String(currency);
			clearList();
			addResultForm(responseText);
		};
		
	// Метод POST
	req.open("POST", "/api/v1/coins/show/price", true);

	// Установка заголовков
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	//req.setRequestHeader("Content-Length", searchString.length);
	
	// Отправка данных BODY методом POST 
	req.send(searchString);			
}


function followCoin(){
    var form = document.forms.form
	var coin = form.querySelector("select[name=coin]").value;
	var currency = form.querySelector("select[name=currency]").value;
	var lower = form.querySelector("input[name=lower]").value;
	var upper = form.querySelector("input[name=upper]").value;
	// Формирование строки поиска
	var searchString = "coin=" + coin + "&" + "currency=" + currency + "&" + "lower=" + String(lower) + "&" + "upper=" + String(upper);
	//alert("searchString: " + searchString);
	
	// Запрос к серверу
	var req = new XMLHttpRequest();
	req.onreadystatechange = function(){
			if (req.readyState != 4) return;
            var respText = req.responseText;
            var resObj = JSON.parse(respText);
            var responseText = "";

            if (String(resObj["detail"]).startsWith("[")) {
                responseText = "Enter correct Lower and Upper limits";
            }else{
                responseText = resObj["detail"];
            }
			clearList();
			addResultForm(responseText);
		};
		
	// Метод POST
	req.open("POST", "/api/v1/coins/follow/coin", true);

	// Установка заголовков
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	//req.setRequestHeader("Content-Length", searchString.length);
	
	// Отправка данных BODY методом POST 
	req.send(searchString);			
}


function showAll(){
	// Запрос к серверу
	var req = new XMLHttpRequest();
	req.onreadystatechange = function(){
		if (req.readyState != 4) return;
        var respText = req.responseText;
        var resObj = JSON.parse(respText);
		clearList();
	    var divResult = document.getElementById("divResult");
	    var bracket = document.createElement("fieldset");
        var p = document.createElement("p")
	    divResult.appendChild(bracket).appendChild(p);
        for (var i = 0; i < resObj.length; i++){
            var text = String(resObj[i].coin_name) + ": " + String(resObj[i].price) + " " + String(resObj[i].currency_label);
			addResultString(text, p);
        };
	};
		
	// Метод POST
	req.open("GET", "/api/v1/coins/follow/all", true);

	req.send();			
}

