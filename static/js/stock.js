function get_stock() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("실시간 주식 데이터 저장 성공")
        }
    };
    xhttp.open("GET", "getstock");
    xhttp.send();
}

function stockchart() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var img_name = this.responseText
            document.getElementById("chart_view").innerHTML = '<img src="./' + img_name + '" width=570 height=310>'
        }
    };
    xhttp.open("POST", "stockchart");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "stock_name=" + document.getElementById("stock_name").value;
    console.log(query)
    xhttp.send(query);
    // alert(document.getElementById('stock_name').value)
}

function wordcloud() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var img_name = this.responseText
            document.getElementById("cloud_view").innerHTML = '<img src="./' + img_name + '" width=550 height=300>'
        }
    };
    xhttp.open("POST", "wordcloud");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "stock_name=" + document.getElementById("stock_name").value;
    console.log(query)
    xhttp.send(query);
}

function upbit() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            coin = this.responseText
            img_name = document.getElementById("coin_name").value
            document.getElementById("upbit2").style.display = 'block';
            document.getElementById("upbit").innerHTML = coin
            document.getElementById("upbit2").innerHTML = '<img src="./static/img/' + img_name + '.png" width=550 height=300>'
        }
    };
    xhttp.open("POST", "upbit");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "coin_name=" + document.getElementById("coin_name").value;
    console.log(query)
    xhttp.send(query);
};


function upbit_graph() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
   
           }
    };
    xhttp.open("POST", "upbit_graph");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "coin_name=" + document.getElementById("coin_name").value;
    console.log(query)
    xhttp.send(query);
};
