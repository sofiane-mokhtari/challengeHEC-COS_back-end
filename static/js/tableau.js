// var tab = document.getElementById("tab");

// function qdd_row() {
// 	var nouvelleLigne = document.getElementById("tab").insertRow(-1);
// 	var cellule = nouvelleLigne.insertCell(0);
// 	var cellule = nouvelleLigne.insertCell(1);
// 	var cellule = nouvelleLigne.insertCell(2);
// 	var cellule = nouvelleLigne.insertCell(3);
// 	var cellule = nouvelleLigne.insertCell(4);

// }

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

