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
	var bracket = document.createElement("fieldset");
    var p = document.createElement("p")
	divResult.appendChild(bracket).appendChild(p);
	var pText = document.createTextNode(text);
	p.appendChild(pText);
}

// Поиск книг
function fetchPrice(){
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
	req.open("POST", "/request/coin/", true);

	// Установка заголовков
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	//req.setRequestHeader("Content-Length", searchString.length);
	
	// Отправка данных BODY методом POST 
	req.send(searchString);			
}
