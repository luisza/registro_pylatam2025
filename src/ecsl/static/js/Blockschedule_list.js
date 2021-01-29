        var time_array = [];
        var activities_dic = JSON.parse(activities_dicHTML);


        $(function (){
            fill_time_array();
            fill_time_array_activities();
        });

        function fill_time_array(){
            for(var i = 0; i < 84; i++){
                time_array.push(null);
            }
        }

        function fill_time_array_activities(){
            const keys = Object.keys(activities_dic);
            for(var i = 0; i < keys.length; i++){
                const start_hour = (parseInt(activities_dic[keys[i]].start_time.split(":")[0]) - 7 ) * 6;
                const start_minute = parseInt(activities_dic[keys[i]].start_time.split(":")[1]) / 10;

                const end_hour = (parseInt(activities_dic[keys[i]].end_time.split(":")[0]) - 7 ) * 6;
                const end_minute = parseInt(activities_dic[keys[i]].end_time.split(":")[1])/10;

                var start_time = start_hour+start_minute;
                const end_time = end_hour+end_minute;

                while(start_time < end_time){
                    time_array[start_time] = String(keys[i]);
                    start_time++;
                }
            }
        }

        var lista = [];
        //var types = null;

        $(function () {
            $("#speeches, #specials, #hour-7, #hour-8, #hour-9,#hour-10, #hour-11, #hour-12,#hour-13, #hour-14,#hour-15, #hour-16, #hour-17, #hour-18, #hour-19, #hour-20, #hour-21").sortable({
                placeholder: "ui-state-highlight",
                connectWith: ".connectedSortable",
            }).disableSelection();
        });

        function difHours(hour1, hour2) {
            starttime = new Date($("#actualDay").text() + " " + hour1)
            endime = new Date($("#actualDay").text() + " " + hour2)
            diff = endime - starttime
            return millisToMinutesAndSeconds(diff)
        }

        function millisToMinutesAndSeconds(millis) {
            var minutes = Math.floor(millis / 60000);
            var seconds = ((millis % 60000) / 1000).toFixed(0);
            return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
        }

        function update_last_hours() {
            for (var i = 7; i <= 20; ++i) {
                var minutes_left_to_assign = parseInt(difHours($('#td-' + (i + 1)).attr('hora'), $('#td-' + i).attr('lasthour')).split(":")[0])
                if (minutes_left_to_assign > 0) {
                    $('#td-' + i).attr('lasthour', addLastHour($('#td-' + i).attr('hora'), 60));
                    $('#td-' + (i + 1)).attr('lasthour', addLastHour($('#td-' + (i + 1)).attr('lasthour'), minutes_left_to_assign));
                }
            }
        }

        function PaintActivities(){
            $(".painted").remove()
            var hour=7
            var min=0
            var pk;
            var pkinit;
            var pkend;
            var text=""
            var select=""
            var li=""
            var url_mask = "{% url 'detail_charla' pk=0 %}";
            for(var i=0;i<time_array.length;++i){
                if(time_array[i]!=null){
                    pk=time_array[i]
                    if(pk!=time_array[i-1]){
                        pkinit=hour+":"+min
                    }
                    if(pk!=time_array[i+1]){
                        if(min+10==60){
                            pkend=(hour+1)+":00"
                        }else{
                            pkend=hour+":"+(min+10)
                        }
                        var hours = parseInt((pkend.split(':')[0])-parseInt(pkinit.split(":")[0]))
                        var starthour=parseInt((pkinit.split(':')[0]))
                        var first= starthour
                        var limit=starthour+hours
                        initprint = String(pkinit)

                        if(initprint.split(':')[1]=='0'){
                            initprint= initprint.split(':')[0]+':00'
                        }
                        if(activities_dic[time_array[i]]["time"]>=60){
                            if(pkend.split(':')[1] == '00'){
                                limit=limit-1;
                            }
                        }


                        for(starthour;starthour<=limit;starthour++){
                            if(activities_dic[time_array[i]].is_speech == ""){
                                text = activities_dic[time_array[i]]['desc']
                                select ='<div class="col-sm-4"></div>'

                                li= '<li class="ui-state-default activity painted" style="background-color: ' + activities_dic[time_array[i]]["color"] + ';"' +
                                    ' value="' + activities_dic[time_array[i]]["value"] + '" color="' + activities_dic[time_array[i]]["color"] + '"' +
                                    ' is_speech= "" ' + ' desc="' + activities_dic[time_array[i]]["desc"] + '"' +
                                    ' time="' + activities_dic[time_array[i]]["time"] + '"' + ' start_hour= "' + activities_dic[time_array[i]]["start_hour"] + '" ' +
                                    'db="' + activities_dic[time_array[i]]["obj_pk"] + ' "start_time="' + activities_dic[time_array[i]]["start_time"] +
                                    '">'

                            }else{
                                text = '<a style="margin-left: 7%;" href=' + url_mask.replace(/0/, activities_dic[time_array[i]]['speech_pk']) + '>' +
                                    activities_dic[time_array[i]]['title'] +
                                    '</a>'
                                select= '<div class="col-sm-4 container_type_time_'+ activities_dic[time_array[i]]["activity_pk"] + '">' +
                                        '<select class="btn btn-primary" id="type_time"' + '>' +
                                        '</select>' +
                                        '</div>'

                                li=  '<li class="ui-state-default activity painted" style="background-color: ' + activities_dic[time_array[i]]["color"] + ';"' +
                                    ' value="' + activities_dic[time_array[i]]["activity_pk"] + '"' + ' color="' + activities_dic[time_array[i]]["color"] + '"' +
                                    ' is_speech="' + activities_dic[time_array[i]]["is_speech"] + '"' + ' desc="' + activities_dic[time_array[i]]["desc"] + '"' +
                                    ' time="' + activities_dic[time_array[i]]["time"] + '"' + ' start_hour= "' + activities_dic[time_array[i]]["start_hour"] + '"' +
                                    'db="' + activities_dic[time_array[i]]["obj_pk"] + ' "start_time="' + activities_dic[time_array[i]]["start_time"] + '"' +
                                    'end_time="' + addhoras(activities_dic[time_array[i]]["start_time"], activities_dic[time_array[i]]["time"]) + '"' +
                                    'id="li_' + activities_dic[time_array[i]]["activity_pk"] + '"' +
                                    '">'

                            }
                            if(starthour==first){
                                $('#hour-' + starthour).append(
                                    li+
                                    '<div class="row">' +
                                    '<div class="col-md-2 text-center">' +
                                    initprint + ' a ' + pkend +
                                    '</div>' +
                                    '<div class="col-md-5 text-center">' +
                                    text
                                    +
                                    '</div>' +
                                    select +
                                    '<div class="col-md-1 text-center">' +
                                    '<button onclick="delete_actity(' + activities_dic[time_array[i]]["room_pk"] + ', ' + activities_dic[time_array[i]]["obj_pk"] + ')" class="btn btn-danger btn-sm deleteButton"> X </button>' +
                                    '</div>' +
                                    '</div>' +'</li>');
                            }else{
                                $('#hour-' + starthour).append('<li class="activity painted" style="background-color:' + activities_dic[time_array[i]].color + '">' + initprint + " a "+ pkend +" "+  '</li>');
                            }
                        }
                    }
                }
                min = min +10
                if(min==60){
                    min=0
                    hour+=1
                }
            }
            var blocks = document.getElementsByClassName("speech_actvity")
            var option = null
            //var types = {{ types_serializer|safe }};
            for (var i = 0; i < blocks.length; i++) {
                for (var j = 0; j < types.length; j++) {
                    if (Object.values(types[j])[1] == blocks[i].getAttribute('speech_type')) {
                        option = '<option selected value="' + Object.values(types[j]['fields'])[1] +
                            "-" + Object.values(types[j])[1] + '">' + Object.values(types[j]['fields'])[0] + " (" + Object.values(types[j]['fields'])[1] + " minutos)"
                        '</option>'
                    } else {
                        option = '<option value="' + Object.values(types[j]['fields'])[1] +
                            "-" + Object.values(types[j])[1] + '">' + Object.values(types[j]['fields'])[0] + " (" + Object.values(types[j]['fields'])[1] + " minutos)"
                        '</option>'
                    }
                    $(".container_type_time_" + blocks[i].getAttribute("activity_pk")).children().append(option)
                }
                $(".container_type_time_" + blocks[i].getAttribute("activity_pk")).children().attr('onchange', 'update_times(' + blocks[i].getAttribute("activity_pk") + ', this)')
            }
            update_last_hours();

        }


        $(function () {
            $(".droppable").droppable({
                drop: function (event, ui) {

                    ui.draggable.attr('start_time', $("#actualDay").text() + " " + $(this).attr("lasthour"))
                    ui.draggable.attr('end_time', addhoras($(this).attr("lasthour"), ui.draggable.attr("time")))

                    hour = parseInt(ui.draggable.attr('start_hour'));

                    if ($('#td-' + hour).attr('lasthour')) {
                        if ($('#td-' + hour).attr('hora') < substractLastHour($('#td-' + hour).attr('lasthour'), ui.draggable.attr("time"))) {
                            $('#td-' + hour).attr('lasthour', substractLastHour($('#td-' + hour).attr('lasthour'), ui.draggable.attr("time")))
                        }
                    }
                    $(this).attr('lasthour', addLastHour($(this).attr('lasthour'), ui.draggable.attr("time")))
                    update_last_hours();


                    ui.draggable.attr('room', $("#actualRoom").text())
                    $("#id_speech").val(ui.draggable.val());
                    $("#id_start_time").val($("#actualDay").text() + " " + $(this).attr("lasthour"));
                    $("#id_end_time").val(addhoras($(this).attr("hora"), ui.draggable.attr("time")));
                    $("#id_color").val((ui.draggable.attr("color")));
                    var is_speech = null
                    if (ui.draggable.attr("is_speech") == 1 || ui.draggable.attr("is_speech") == 'true') {
                        $("#id_is_speech").prop("checked", true);
                        is_speech = 'true'
                    } else {
                        $("#id_is_speech").prop("checked", false);
                        is_speech = ""
                    }
                    $("#id_room").val($("#actualRoom").text());
                    $("#id_text").val(ui.draggable.attr("desc"));
                    var element = {
                        'pk_speech': ui.draggable.val(),
                        'color': ui.draggable.attr("color"),
                        'start_time': ui.draggable.attr('start_time'),
                        'end_time': ui.draggable.attr('end_time'),
                        'is_speech': is_speech,
                        'room': ui.draggable.attr('room'),
                        'description': ui.draggable.attr("desc"),
                    }
                    $('.' + is_speech + ui.draggable.val() + '').remove();
                    if (ui.draggable.attr('type')) {
                        element['type'] = ui.draggable.attr('type')
                    }

                    PaintActivities()
                    var value = activities_in_list(element)
                    if (value == false) {
                        lista.push(element)
                    }
                    if ($(this).attr('id') === 'speeches' || $(this).attr('id') === 'specials') {
                        delete_temp_activity(ui.draggable.attr('value'), ui.draggable.attr('is_speech'))
                        if (ui.draggable.attr('db')) {
                            delete_actity(ui.draggable.attr('room'), ui.draggable.attr('db'))
                        }
                    }
                }
            });
            update_last_hours();
        });


        $(function () {
            var special = document.getElementsByClassName("special_actvity")
            for (var i = 0; i < special.length; ++i) {
                var element = {
                    'pk_speech': special[i].getAttribute("value"),
                    'color': special[i].getAttribute("color"),
                    'start_time': special[i].getAttribute("start_datetime"),
                    'end_time': special[i].getAttribute("end_datetime"),
                    'is_speech': special[i].getAttribute("is_speech"),
                    'room': special[i].getAttribute("room_pk"),
                    'description': special[i].getAttribute("desc"),
                }
                lista.push(element)
            }
            PaintActivities()
            update_last_hours();
        });

        $(function () {
            var blocks = document.getElementsByClassName("speech_actvity")

            var url_mask = "{% url 'detail_charla' pk=0 %}";

            for (var i = 0; i < blocks.length; ++i) {
                var element = {
                    'pk_speech': blocks[i].getAttribute("activity_pk"),
                    'color': blocks[i].getAttribute("color"),
                    'start_time': blocks[i].getAttribute("start_datetime"),
                    'end_time': blocks[i].getAttribute("end_datetime"),
                    'is_speech': blocks[i].getAttribute("is_speech"),
                    'room': blocks[i].getAttribute("room_pk"),
                    'description': blocks[i].getAttribute("desc"),
                }
                lista.push(element)
            }
            PaintActivities()
        });

        function delete_temp_activity(id, is_speech) {
            if (is_speech == 0) {
                is_speech = ""
            }
            for (var i = 0; i < lista.length; i++) {
                if (lista[i]['pk_speech'] == id && lista[i]['is_speech'] == is_speech) {
                    lista.splice(i, 1)
                }
            }
        }

        function delete_actity(room_pk, obj_pk) {
            $('#obj_pk').val(parseInt(obj_pk))
            $('#room_pk').val(parseInt(room_pk))
            $('#delete_activity').submit()

        }

        function activities_in_list(element) {
            value = false
            for (var i = 0; i < lista.length; i++) {
                if (lista[i]['is_speech'] === element['is_speech']) {
                    if (lista[i]['pk_speech'] == element['pk_speech']) {
                        lista.splice(i, 1)
                        lista.push(element)
                        value = true
                    }
                }
            }
            return value
        }

        function send_activities_list() {
            var token = tokenHTML;
            if (lista.length != 0) {
                $.ajax({
                    headers: {"X-CSRFToken": token},
                    type: "post",
                    data: {
                        'agenda': JSON.stringify(lista),
                    },
                    success: function (data) {
                        console.log(data)
                        location.reload()
                    }
                });
            } else {
                location.reload()
            }
        }

        function addhoras(hora, minutos) {
            starttime = new Date($("#actualDay").text() + " " + hora)
            starttime.setMinutes(starttime.getMinutes() + parseInt(minutos))
            endtime = $("#actualDay").text() + " " + starttime.getHours() + ":" + starttime.getMinutes() + ":00"
            return (endtime)
        }

        function addLastHour(hora, minutos) {
            starttime = new Date($("#actualDay").text() + " " + hora)
            starttime.setMinutes(starttime.getMinutes() + parseInt(minutos))
            endtime = "" + starttime.getHours() + ":" + starttime.getMinutes() + ":00"
            return (endtime)
        }

        function substractLastHour(hora, minutos) {
            starttime = new Date($("#actualDay").text() + " " + hora)
            starttime.setMinutes(starttime.getMinutes() - parseInt(minutos))
            endtime = "" + starttime.getHours() + ":" + starttime.getMinutes() + ":00"
            return (endtime)
        }

        function send_filter() {
            var option = null
            $('#speeches').empty()
            $.ajax({
                url: "proposal/filterSpeeches/",
                type: "post",
                data: $("#filter").serialize(),
                success: function (data) {
                    if (data.result.length != 0) {
                        result = JSON.parse(data.result)
                        if (Object.entries(result).length == 0) {
                            result = null
                        }
                    } else {
                        result = null
                    }
                    if (result != null) {
                        for (var i = 0; i < result.length; i++)
                            $('#speeches').append('<li class="ui-state-default activity" style="background-color:' + data.color[i] + ';"' +
                                'value="' + Object.values(result[i])[1] + '" color="' + data.color[i] + '"' +
                                'id="li_' + Object.values(result[i])[1] +
                                '" is_speech="1"' + 'desc="none"' + 'time="' + data.times[i] + '">' +
                                '<div class="row">' +
                                '<div class="col-sm-8">' +
                                Object.values(result[i]['fields'])[2] +
                                '</div>' +
                                '<div class="col-sm-4 container_type_time_' + Object.values(result[i])[1] + '">' +
                                '<select class="btn btn-primary" id="type_time"' + '>' +
                                '</select>' +
                                '</div>' +
                                '</div>' +
                                '</li>')
                        result_types = JSON.parse(data.types)
                        for (var i = 0; i < result.length; i++) {
                            for (var j = 0; j < result_types.length; j++) {
                                if (Object.values(result_types[j])[1] == Object.values(result[i]['fields'])[4]) {

                                    option = '<option selected value="' + Object.values(result_types[j]['fields'])[1] +
                                        "-" + Object.values(result_types[j])[1] + '">' + Object.values(result_types[j]['fields'])[0] + " (" + Object.values(result_types[j]['fields'])[1] + " minutos)"
                                    '</option>'
                                } else {
                                    option = '<option value="' + Object.values(result_types[j]['fields'])[1] +
                                        "-" + Object.values(result_types[j])[1] + '">' + Object.values(result_types[j]['fields'])[0] + " (" + Object.values(result_types[j]['fields'])[1] + " minutos)"
                                    '</option>'
                                }
                                $(".container_type_time_" + Object.values(result[i])[1]).children().append(option)
                            }
                            $(".container_type_time_" + Object.values(result[i])[1]).children().attr('onchange', 'update_times(' + Object.values(result[i])[1] + ', this)')

                        }
                        $('.draggable').draggable();
                    } else {
                        $('#speeches').append('<p>transResult</p>')
                    }
                }
            });
        }

        function update_times(speech_pk, speech_time) {

            var type_values = speech_time.value.split('-')
            $("#li_" + speech_pk).attr('time', type_values[0])
            $("#li_" + speech_pk).attr('type', type_values[1])
            $("#li_" + speech_pk).attr('start_time', $("#actualDay").text() + " " + $("#li_" + speech_pk).parent().attr('hora'))
            $("#li_" + speech_pk).attr('end_time', addhoras($("#li_" + speech_pk).parent().attr('hora'), type_values[0]))
            for (var i = 0; i < lista.length; i++) {
                if (lista[i]['pk_speech'] == speech_pk) {
                    lista[i]['type'] = type_values[1]
                    lista[i]['start_time'] = $("#actualDay").text() + " " + $("#li_" + speech_pk).parent().attr('hora')
                    lista[i]['end_time'] = addhoras($("#li_" + speech_pk).parent().attr('hora'), type_values[0])
                }
            }
        }

        $(function displayOrEdit() {
            var action = '{{ view }}'
            if (action == 'display') {
                $("#filterPanel").remove();
                $("#send_activities").remove();
                $(".deleteButton").remove();
                $("#addroom").remove();
                $('.activity').draggable({disabled: true});
                $('.connectedSortable').sortable({disabled: true});
            }
        });