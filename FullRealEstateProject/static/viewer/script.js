document.addEventListener('DOMContentLoaded', function() {
    date();
    configureCalander();
    showOwners();
    

});


function showOwners() {
    if (document.getElementById('current_owner')) {
        var currentOwner = document.getElementById('current_owner')
        var owner = document.getElementById('current_owner').value;

        // hide all the divs of class true-people except the one with the id of the current owner
        var people = document.getElementsByClassName('true-people');
        for (var i = 0; i < people.length; i++) {
            people[i].style.display = 'none';
        }
        document.getElementById(owner).style.display = 'block';

        currentOwner.onchange = function() {
            // get what it was 
            var owner = document.getElementById('current_owner').value;

            // hide all the divs of class true-people except the one with the id of the current owner
            var people = document.getElementsByClassName('true-people');
            for (var i = 0; i < people.length; i++) {
                people[i].style.display = 'none';
            }
            document.getElementById(owner).style.display = 'block';
        }
    }
}


function date() {  
    if (!document.getElementsByClassName('mini-window')) {
        return;
    }
    
    var miniWindows = document.getElementsByClassName('mini-window');
    var fullWindows = document.getElementsByClassName('full-window');
        // check if its a full window or a popup
    if (window.opener) {
        for (var i = 0; i < miniWindows.length; i++) {
            miniWindows[i].style.display = 'block';
        }

        for (var i = 0; i < fullWindows.length; i++) {
            fullWindows[i].style.display = 'none';
        }
        
        // $(calendarInput).datepicker('hide'); 

        document.getElementById('events').style.display = 'none';
        
        document.getElementById('toggleBtn').onclick = function() {
            if (document.getElementById('form').style.display == 'none') {
                document.getElementById('toggleBtn').innerText = 'Views Event';
                document.getElementById('events').style.display = 'none';
                document.getElementById('form').style.display = 'block';
            } else {
                document.getElementById('toggleBtn').innerText = 'Add Event';
                document.getElementById('events').style.display = 'block';
                document.getElementById('form').style.display = 'none';
            }
        }

    } else {
        for (var i = 0; i < fullWindows.length; i++) {
            fullWindows[i].style.display = 'block';
        }

        for (var i = 0; i < miniWindows.length; i++) {
            miniWindows[i].style.display = 'none';
        }
    }
}



function configureCalander () {

    var calendarInput = document.getElementById('datepicker');

    $(calendarInput).datepicker({
        showOn: "button",
        buttonText: "Calendar",
        beforeShow: function() {
            $(calendarInput).show();
        },
        onClose: function() {
            $(calendarInput).hide();
        },
        onSelect: function(dateText) {

            modifiedDate = dateText.replace('/', '-').replace('/', '-');

            var popupWindow = window.open(`https://debtfreesolutions.duckdns.org/date/${modifiedDate}`, "PopupWindow", "width=600,height=600");
            
            console.log(dateText);
        }
    });

    // Add class to the button
    $('button.ui-datepicker-trigger').addClass('btn btn-primary');

    $(calendarInput).hide();
}