function toggle_editable_component(component_child){
    console.log(component_child.name);
    var container = $('#' + component_child.name);
    container.css('background-color', 'red');
    var class_tag = ['fr_1', 'jp_1', 'jp_2', 'zh_1'];
    var temp = container.find(".fr_1").attr("contenteditable");
    console.log("STATE: " + temp);
    if(temp=="true")temp = "false";
    else temp = "true";
    for(cur_tag in class_tag){
        console.log(class_tag[cur_tag]);
        container.find("." + class_tag[cur_tag]).attr('contenteditable', temp );
    }

    if(container.find(".fr_1").attr("contenteditable") == "true"){
        container.css('background-color', 'green');
    }
}

function clean_row_to_add(component_child){
    var container = $("#" + component_child.name);
    var class_tag = ['fr_1', 'jp_1', 'jp_2', 'zh_1'];
    for(cur_tag in class_tag){
        console.log(class_tag[cur_tag]);
        my_field = container.find("." + class_tag[cur_tag]);
        my_field.attr('contenteditable', 'true' );
        my_field.text('');
    }
}