function toggle_editable_component(component_child){

    var container = $('#' + component_child.name);
    var class_tag = ['fr_1', 'jp_1', 'jp_2', 'zh_1'];
    var temp = container.find(".fr_1").attr("contenteditable");
    if(temp=="true")temp = "false";
    else temp = "true";
    for(cur_tag in class_tag){
        container.find("." + class_tag[cur_tag]).attr('contenteditable', temp );
    }
}

function clean_row_to_add(component_child){
    var container = $("#" + component_child.name);
    var class_tag = ['fr_1', 'jp_1', 'jp_2', 'zh_1'];
    for(cur_tag in class_tag){
        my_field = container.find("." + class_tag[cur_tag]);
        my_field.attr('contenteditable', 'true' );
        my_field.text('');
    }
    container.find('.thematic_select option').each(function(){
    var $this = $(this); // cache this jQuery object to avoid overhead
    $this.prop('selected', false);
    });

    container.find('.lv_select option').each(function(){
    var $this = $(this); // cache this jQuery object to avoid overhead
    $this.prop('selected', false);
    });
}

function enterSearchBarKeyPress(event){
    if(event.keyCode == 13){
         //prevent return carriage + search when press enter
         event.preventDefault();
         get_entries();
         $('#id_text').blur();
    }
}

function toogleAddPanelDisplay(component){
    //component = documnet.getElementById('toggle_add');
    container = document.getElementById('new_id');
    container_fields = document.getElementById('new_id_fields');
    if(container.style.display != 'none'){
        container.style.display = 'none';
        container_fields.style.display = 'none';
        component.innerHTML = "<p><span class='glyphicon glyphicon-plus'></span> Show Add Panel</p>";
    }else{
        container.style.display = 'block';
        container_fields.style.display = 'block';
        component.innerHTML = "<p><span class='glyphicon glyphicon-minus'></span> Hide Add Panel</p>";
    }
}


function show_updated(){
    $('#display_state_panel').css('display', 'block');
    $('#display_state_panel').html('Update Completed');

	setTimeout(function(){
		$('#display_state_panel').css('display', 'none');
        }, 3000);
}

function show_created(){
    $('#display_state_panel').css('display', 'block');
    $('#display_state_panel').html('Entry Created');

	setTimeout(function(){
		$('#display_state_panel').css('display', 'none');
        }, 3000);
}

function show_removed(){
    $('#display_state_panel').css('display', 'block');
    $('#display_state_panel').html('Entry Removed');

	setTimeout(function(){
		$('#display_state_panel').css('display', 'none');
        }, 3000);
}

function show_searching(){
    $('#display_state_panel').css('display', 'block');
    $('#display_state_panel').css('opacity', '0.7');
    $('#display_state_panel').css('height', '100%');
    $('#display_state_panel').css('font-size', '3em');
    $('#display_state_panel').html('Searching ... ');
}

function hide_searching(){
    $('#display_state_panel').css('display', 'none');
    $('#display_state_panel').css('opacity', '1');
    $('#display_state_panel').css('font-size', '1em');
    $('#display_state_panel').css('height', '15%');
}