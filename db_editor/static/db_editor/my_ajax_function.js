function get_entries(){

	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
   		crossDomain: false, // obviates need for sameOrigin test
    	beforeSend: function(xhr, settings) {
        	if (!csrfSafeMethod(settings.type)) {
         	   xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	}
	});

	$.ajax({url: '/editor/ajax_entries_request/',
		type: 'POST',
		//contentType: "application/json; charset=utf-8",
		data: {'text': $('#id_text').val()},
		success: function(html){
			var container = $(".jp_word_entries_container");
			container.html(html);
		}});
}


function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
    	var cookies = document.cookie.split(';');
    	for (var i = 0; i < cookies.length; i++) {
        	var cookie = jQuery.trim(cookies[i]);
        	// Does this cookie string begin with the name we want?
        	if (cookie.substring(0, name.length + 1) == (name + '=')) {
            	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            	break;
        	}
    	}
	}
    return cookieValue;
}

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function ajax_update_entry(component){
    var my_entry_id = component.name;
    var container = $('#'+my_entry_id);

    var my_dict = {
        'fr_1': container.find(".fr_1").text(),
        'zh_1': container.find(".zh_1").text(),
        'jp_1': container.find(".jp_1").text(),
        'jp_2': container.find(".jp_2").text()
    };

    if(my_entry_id != "new_id"){
        my_dict.push({'entry_id': my_entry_id});
    }


    var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
   		crossDomain: false, // obviates need for sameOrigin test
    	beforeSend: function(xhr, settings) {
        	if (!csrfSafeMethod(settings.type)) {
         	   xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	}
	});

	$.ajax({url: '/editor/ajax_update_request/',
		type: 'POST',
		data: my_dict,
		success: function(html){
		console.log("Ajax_Success");
			$("#"+my_entry_id).css('background-color', 'gray');
		}});
}