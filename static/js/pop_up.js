class ajax
{
    constructor()
    {
        var xhr
        if (window.XMLHttpRequest || window.activeXObject)
        {
            if (window.activeXObject)
            {
                try
                {
                    xhr = new ActiveXObject("Msxml2.XMLHTTP");
                }
                catch
                {
                    xhr = new ActiveXObject("Microsoft.XMLHTTP");
                }
            }
            else
            {
                xhr = new XMLHttpRequest();
            }
        }
        this.xhr = xhr;
    }
    
    rqt_get(adr)
    {
        this.xhr.open("GET", adr, true);
        this.xhr.send(null);
    }

    rqt_post(adr, vrb)
    {
        this.xhr.open("POST", adr, true);
        this.xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        this.xhr.send(vrb);
    }
}


var btn = document.getElementById('activate');
var spa = document.getElementById('div_close');

option  = 0;

var ele1 = document.getElementById('ele1');
var ele2 = document.getElementById('ele2');
var button_ele = document.getElementById('do_search');
var button_ele2 = document.getElementById('do_relation');

var do_chart = function() {
    var start = document.getElementById("start");
    var ret = document.getElementById("ret")
    start.style.display = "none";

}

ele1.onclick = function(event, option)
{
    ele1.style = "background:#5cb85c";
    ele2.style = "background:white";
    option = 1;
}

ele2.onclick = function(event, option)
{
    ele1.style = "background:white";
    ele2.style = "background:#5cb85c";
    option = 2;
}

button_ele2.onclick = function(event)
{
    var e = document.getElementById('do_res');
    if (ele1.style == "white" && ele2.style == "white")
       { alert("Aucun type de recherche choisi");}
    else if (e.value == null)
       { alert("Input vide");}
    else
    {
        var com = new ajax();
        if (ele1.style.backgroundColor == "rgb(92, 184, 92)")
            {com.rqt_get("/relation/" + e.value + "/0");}
        else if (ele2.style.backgroundColor == "rgb(92, 184, 92)")
            {com.rqt_get("/relation/" + e.value + "/1");}
        com.xhr.onreadystatechange  = function() 
        {
            console.log(com.xhr.readyState);
            if(com.xhr.readyState  == 4)
            {
                if(com.xhr.status  == 200)
                {
                    var txt = JSON.parse(com.xhr.responseText);
                    $('#json-container').jsonview(txt);
                }
                else
                {
                    document.getElementById("para").innerHTML = com.xhr.status;
                }
            }
        }; 
    }
}

button_ele.onclick = function(event)
{
    var e = document.getElementById('do_res');
    if (ele1.style == "white" && ele2.style == "white")
       { alert("Aucun type de recherche choisi");}
    else if (e.value == null)
       { alert("Input vide");}
    else
    {
        var com = new ajax();
        if (ele1.style.backgroundColor == "rgb(92, 184, 92)")
            {com.rqt_get("/tweet_user/" + e.value + "/50");}
        else if (ele2.style.backgroundColor == "rgb(92, 184, 92)")
            {com.rqt_get("/tweet_hast/" + e.value + "/50");}
        com.xhr.onreadystatechange  = function() 
        {
            console.log(com.xhr.readyState);
            if(com.xhr.readyState  == 4)
            {
                if(com.xhr.status  == 200)
                {
                    var txt = JSON.parse(com.xhr.responseText).return;
                    var dic = document.getElementById("ret");
                    txt.forEach(function(y) 
                    { 
                        var newpara = document.createElement('p');
                        newpara.class = "newpara";
                        var text = document.createTextNode(y);
                        newpara.appendChild(text);
                        dic.appendChild(newpara);
                    }
                    );
                }
                else
                {
                    document.getElementById("para").innerHTML = com.xhr.status;
                }
            }
        }; 
    }
}

spa.onclick = function(event)
{
	var modal = document.getElementById('myModal');
    if (event.target == modal)
        {modal.style.display = "none";}
}

btn.onclick = function()
{
	var modal = document.getElementById('myModal');
	var id_to_div = document.getElementsByClassName("modal-body");
	modal.style.display = "block";
}

window.onclick = function(event)
{
	var modal = document.getElementById('myModal');
    if (event.target == modal)
        {modal.style.display = "none";}
}
