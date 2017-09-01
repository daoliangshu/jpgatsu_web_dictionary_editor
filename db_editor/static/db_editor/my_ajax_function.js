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

    var levelSelected = $('#id_my_level').val();
    var thematicSelected = $('#id_my_thematic').val();
    var searchFieldsSelected = $('#id_my_field').val();
    console.log('enter get_entries() with : ');
    console.log('text:  ' + $('#id_text').val());
    console.log('thematics:  ' + thematicSelected);
    console.log('levels:  ' + levelSelected);
    console.log('fields:  ' + searchFieldsSelected);
    data = {'text': $('#id_text').val(),
            'levels' : levelSelected,
		    'thematics': thematicSelected,
		    'search_fields':　searchFieldsSelected,
		    'search_pattern': $('#id_search_pattern').val()};
    show_searching();
	$.ajax({url: '/editor/ajax_entries_request/',
		type: 'POST',
		data: data,
		success: function(html){
			var container = $("#populate_content");
			container.html(html);
			hide_searching();
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
        'fr_1': container.find(".fr_1").text().trim(),
        'zh_1': container.find(".zh_1").text().trim(),
        'jp_1': container.find(".jp_1").text().trim(),
        'jp_2': container.find(".jp_2").text().trim(),
        'lv': container.find(".lv_select").val(),
        'thematic': container.find(".thematic_select").val()
    };
    console.log(my_dict);
    if(my_entry_id != "new_id"){
        my_dict['entry_id'] =  my_entry_id;
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
		    if(my_entry_id == 'new_id'){
		        $("#populate_content").html(html);
		        show_created();
		    }
		    else{
		        //ontainer.html(html);
		        $("#"+my_entry_id).css('background-color', 'gray');
		        show_updated();
		    }


		}});
}

function ajax_remove_entry(component){
    var my_entry_id = component.name;
    var container = $('#'+my_entry_id);
    var my_dict = {
        'entry_id' : my_entry_id,
        'fr_1': container.find(".fr_1").text().trim(),
        'zh_1': container.find(".zh_1").text().trim(),
        'jp_1': container.find(".jp_1").text().trim(),
        'jp_2': container.find(".jp_2").text().trim(),
        'lv': container.find(".lv_select").val(),
        'thematic': container.find(".thematic_select").val()
    };
    my_message = '';
    for(key in my_dict){
        my_message += '{ ' + key + ' :  ' + my_dict[key] + ' }\n';
    }

    if( confirm('Do you really want to remove entry : \n' + my_message) == true){
        var csrftoken = getCookie('csrftoken');
	    $.ajaxSetup({
   		    crossDomain: false, // obviates need for sameOrigin test
    	    beforeSend: function(xhr, settings) {
        	    if (!csrfSafeMethod(settings.type)) {
         	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	    }
    	    }
	    });
	    $.ajax({url: '/editor/ajax_remove_request/',
		type: 'POST',
		data: my_dict,
		success: function(html){
			$("#"+my_entry_id).remove();
			show_removed();
		}});
    }
}