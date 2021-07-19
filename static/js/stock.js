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

function get_news() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert("실시간 뉴스 데이터 저장 성공")
        }
    };
    xhttp.open("GET", "getnews");
    xhttp.send();
}

function stockchart() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var img_name = this.responseText
            document.getElementById("chart_view").innerHTML = '<img src="./' + img_name + '" width=550 height=300>'
        }
    };
    xhttp.open("POST", "stockchart");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "stock_name=" + document.getElementById("stock_name").value;
    console.log(query)
    xhttp.send(query);
    alert(document.getElementById('stock_name').value)
}

function wordcloud() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var img_name = this.responseText
            document.getElementById("cloud_view").innerHTML = '<img src="./' + img_name + '" width=400 height=500>'
        }
    };
    xhttp.open("POST", "wordcloud");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    query = "stock_name=" + document.getElementById("stock_name").value;
    console.log(query)
    xhttp.send(query);
}
