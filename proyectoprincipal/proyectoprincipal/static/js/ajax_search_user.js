$(function () {
    $('#search').keyup(function () {
        $.ajax({
            url: '/mainapp/users/?from=search_input&search_text='+$('#search').val(),
            dataType: "json",
            success : function (data) {
                //console.log(data);
<<<<<<< HEAD
                build_rows(data["rows"]);
=======
                build_rows(data["users"]);
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f
                buid_pagination(data['pag_links'])
            }
        });
    });
});

function buid_pagination(pag_links) {
    $( "#ul-pagination" ).empty();
    var links = pag_links["page_links"];
    var previous = pag_links["previous_url"];
    var next = pag_links["next_url"];
    var html = "";

    if(links.length > 1){
        if(previous != null){
            previous = previous.replace("from=search_input&", "");
            html += '<li><a href='+previous+'>&laquo;</a></li>';
        }else{
            html += '<li class="disabled"><span>&laquo;</span></li>';
        }

        for(var i=0; i<links.length; i++){
            if(links[i][2]){
                html += '<li class="active"><span>'+links[i][1]+' <span class="sr-only">(current)</span></span></li>';
            }else{
                var link = links[i][0];
                link = link.replace("from=search_input&", "");
                html += '<li><a href='+link+'><span>'+ links[i][1] +'</span></a></li>';
            }
        }

        if(next != null){
            next = next.replace("from=search_input&", "");
            html += '<li><a href='+next+'>&raquo;</a></li>';
        }else{
            html += '<li class="disabled"><span>&raquo;</span></li>';
        }
    }
    $( "#ul-pagination" ).append(html);
}

function build_rows(objects) {
    var html;
    $("#table-users-list > tbody").empty();
    for(var i=0; i<objects.length; i++) {
        html = "";
        html += "<tr id='table-rows'>";
        html += "<td>" + objects[i].id + "</td>";
        html += "<td>" + objects[i].username + "</td>";
        html += "<td>" + objects[i].first_name + "</td>";
        html += "<td>" + objects[i].last_name + "</td>";
        html += "<td>" + objects[i].email + "</td>";
        html += "<td>" + objects[i].is_active + "</td>";
        html += "<td><a class='btn btn-primary' href='/mainapp/user_edit/" + objects[i].id + "/' style='margin-right: 0.2rem;'>Editar</a>";
        if (!objects[i].is_superuser){
            if (objects[i].is_active == false) {
                html += "<a class=\"btn btn-info\" onclick=\"open_modal('" + objects[i].id + "','" + objects[i].first_name + "','" + objects[i].last_name + "','True')\"\>Active</a></td>";
            } else {
                html += "<a class=\"btn btn-danger\" onclick=\"open_modal('" + objects[i].id + "','" + objects[i].first_name + "','" + objects[i].last_name + "','False')\"\>Deacti</a></td>";
            }
        }
        html += "</tr>";
        $( "#table-users-list > tbody" ).append(html);
    }
}

