function toggle_editable_component(component_child){

    var container = $('#' + component_child.name);
    container.css('background-color', 'black');
    var class_tag = ['fr_1', 'jp_1', 'jp_2', 'zh_1'];
    var temp = container.find(".fr_1").attr("contenteditable");
    if(temp=="true")temp = "false";
    else temp = "true";
    for(cur_tag in class_tag){
        container.find("." + class_tag[cur_tag]).attr('contenteditable', temp );
    }

    if(container.find(".fr_1").attr("contenteditable") == "true"){
        container.css('background-color', '#d2e0d2');
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
    }
}