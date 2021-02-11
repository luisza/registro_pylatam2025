var lista = [];
var time_array = [];
var activities_dic = JSON.parse(activities_dicHTML);
var stored_activities_dic = JSON.parse(stored_activities_dicHTML);

$(function () {
    fill_time_array();
    fill_time_array_stored_activities();
});

function fill_time_array() {
    for (var i = 0; i < 84; i++) {
        time_array.push(null);
    }
}

function fill_time_array_stored_activities() {
    const keys = Object.keys(stored_activities_dic);
    for (var i = 0; i < keys.length; i++) {
        const start_hour = (parseInt(stored_activities_dic[keys[i]].start_time.split(":")[0]) - 7) * 6;
        const start_minute = parseInt(stored_activities_dic[keys[i]].start_time.split(":")[1]) / 10;

        const end_hour = (parseInt(stored_activities_dic[keys[i]].end_time.split(":")[0]) - 7) * 6;
        const end_minute = parseInt(stored_activities_dic[keys[i]].end_time.split(":")[1]) / 10;

        var start_time = start_hour + start_minute;
        const end_time = end_hour + end_minute;

        while (start_time < end_time) {
            time_array[start_time] = String(keys[i]);
            start_time++;
        }
    }
}

function validate_activity_scheduling(activity_pk, hour, time) {
    var can_be_stored = false;
    hour = (hour - 7) * 6;
    var valid_start_position = -1;
    if (hour == 84 && time / 10 > 6) {
        return -1;
    }
    for (var i = hour; !can_be_stored && i < hour + 6; i++) {
        var occupied = false;
        for (var j = i; !occupied && j < time / 10 + i; j++) {
            if (time_array[j] && time_array[j] != activity_pk) {
                occupied = true;
            }
        }
        if (!occupied) {
            can_be_stored = true;
            valid_start_position = i;
        }
    }
    if (can_be_stored) {
        var keys = Object.keys(stored_activities_dic);
        if (keys.includes(activity_pk)) {
            for (var i = 0; i < time_array.length; i++) {
                if (time_array[i] == activity_pk) {
                    for (var j = i; j < (parseInt(stored_activities_dic[activity_pk].time) / 10) + i; j++) {
                        time_array[j] = null;
                    }
                }
            }
        }
        for (var i = valid_start_position; i < parseInt(activities_dic[activity_pk].time) / 10 + valid_start_position; i++) {
            time_array[i] = activity_pk;

        }
        return valid_start_position;
    } else {
        return -1;
    }
}

function ArrayIndexToHour(index) {
    base = 7
    hour = Math.trunc(parseInt(index) / 6)
    min = (parseInt(index) % 6) * 10
    if (min == 0) {
        min = "00"
    }
    time = "" + (hour + base) + ":" + min
    return time
}

function update_stored_dic(start_Position, activity_pk) {
    var element = {}
    element["start_datetime"] = $("#actualDay").text() + " " + ArrayIndexToHour(start_Position) + ":00"
    element["end_datetime"] = $("#actualDay").text() + " " + ArrayIndexToHour(start_Position + (parseInt(activities_dic[activity_pk].time) / 10)) + ":00"
    element["start_time"] = ArrayIndexToHour(start_Position)
    element["start_hour"] = ArrayIndexToHour(start_Position).split(':')[0]
    element["end_time"] = ArrayIndexToHour(start_Position + (parseInt(activities_dic[activity_pk].time) / 10))
    element["time"] = activities_dic[activity_pk].time
    element["is_scheduled"] = activities_dic[activity_pk].is_scheduled
    element["activity_pk"] = parseInt(activity_pk.split('-')[1])
    element["desc"] = activities_dic[activity_pk].desc
    element["color"] = activities_dic[activity_pk].color

    if (parseInt(activity_pk.split('-')[0])) {
        element["is_speech"] = "true"
        element["title"] = activities_dic[activity_pk].title
        element["room_name"] = room_name
        element["speech_pk"] = parseInt(activity_pk.split('-')[1])
        element["speech_type"] = activities_dic[activity_pk].speech_type
    } else {
        element["is_speech"] = ""

    }
    stored_activities_dic[activity_pk] = element;
}

function control_validate_update(start_position, o_time, n_time) {
    var posiciones = []
    var old_posiciones = []

    old_posiciones = add_new_positions(start_position, o_time)
    old_local = old_posiciones.length
    posiciones = add_new_positions(start_position, n_time)
    if (posiciones.length == 1 && n_time == 10) {
        return true
    }
    if (posiciones != false) {
        new_local = posiciones.length
        return validator(old_local, new_local, posiciones)
    } else {
        return false
    }
}

function add_new_positions(start_position, new_time) {
    var positions = []
    new_time = new_time / 10

    for (var i = 0; i < new_time; i++) {
        if (i == 0) {
            positions.push(start_position)
        } else {
            start_position = start_position + 1
            positions.push(start_position)
        }
    }
    if (positions[positions.length - 1] > 89) {
        positions = false
    }
    return positions
}

function update_time_array_activitiy_rescheduled(speech_pk, start_position, old_time, new_time) {
    new_time = parseInt(new_time);
    activity_pk = "1-" + speech_pk;
    for (var i = start_position; i < old_time / 10 + start_position; i++) {
        time_array[i] = null;
    }
    for (var i = start_position; i < new_time / 10 + start_position; i++) {
        time_array[i] = activity_pk;
    }
}

function validator(old_local, new_local, positions) {
    cont = 0;
    checked_values = []
    result = true
    if (new_local > old_local) {
        position = new_local - old_local
    } else {
        position = old_local - new_local
    }
    if (position > positions.length) {
        checked_values.push(true)
    } else {
        for (var i = old_local; i <= positions.length; i++) {
            if (time_array[positions[i]] == null || old_local > new_local) {
                checked_values.push(true)
            } else {
                checked_values.push(false)
            }
            cont = cont + 1
        }
    }
    for (var i = 0; i < checked_values.length; i++) {
        if (checked_values[i] == false) {
            result = false
            break
        }
    }
    return result
}

$(function () {
    $("#speeches, #specials, #hour-7, #hour-8, #hour-9,#hour-10, #hour-11, #hour-12,#hour-13, #hour-14,#hour-15, #hour-16, #hour-17, #hour-18, #hour-19, #hour-20, #hour-21").sortable({
        placeholder: "ui-state-highlight",
        connectWith: ".connectedSortable",
        items: '> li'
    }).disableSelection();
});


function PaintActivities() {
    $(".painted").remove()
    var hour = 7
    var min = 0
    var pk;
    var pkinit;
    var pkend;
    var text = ""
    var select = ""
    var li = ""
    var url_mask = url_maskHTML;
    for (var i = 0; i < time_array.length; ++i) {
        if (time_array[i] != null) {
            pk = time_array[i]
            if (pk != time_array[i - 1]) {
                pkinit = hour + ":" + min
            }
            if (pk != time_array[i + 1]) {
                if (min + 10 == 60) {
                    pkend = (hour + 1) + ":00"
                } else {
                    pkend = hour + ":" + (min + 10)
                }
                var hours = parseInt((pkend.split(':')[0]) - parseInt(pkinit.split(":")[0]))
                var starthour = parseInt((pkinit.split(':')[0]))
                var first = starthour
                var limit = starthour + hours
                initprint = String(pkinit)

                if (initprint.split(':')[1] == '0') {
                    initprint = initprint.split(':')[0] + ':00'
                }
                if (stored_activities_dic[time_array[i]]["time"] >= 60) {
                    if (pkend.split(':')[1] == '00') {
                        limit = limit - 1;
                    }
                }


                for (starthour; starthour <= limit; starthour++) {
                    if (stored_activities_dic[time_array[i]].is_speech == "") {
                        text = stored_activities_dic[time_array[i]]['desc']
                        select = '<div class="col-sm-4"></div>'

                        li = '<li class="ui-state-default activity painted" style="background-color: ' + stored_activities_dic[time_array[i]]["color"] + ';"' +
                            ' activity_pk="' + stored_activities_dic[time_array[i]]["activity_pk"] + '" color="' + stored_activities_dic[time_array[i]]["color"] + '"' +
                            ' is_speech= "" ' + ' desc="' + stored_activities_dic[time_array[i]]["desc"] + '"' +
                            ' time="' + stored_activities_dic[time_array[i]]["time"] + '"' + ' start_hour= "' + stored_activities_dic[time_array[i]]["start_hour"] + '" ' +
                            'db="' + stored_activities_dic[time_array[i]]["obj_pk"] + ' "start_time="' + stored_activities_dic[time_array[i]]["start_time"] +
                            '">'

                    } else {
                        text = '<a style="margin-left: 7%;" href="' + url_mask.replace(/0/, parseInt(stored_activities_dic[time_array[i]]['activity_pk'])) + '">' +
                            stored_activities_dic[time_array[i]]['title'] +
                            '</a>'
                        select = '<div class="col-sm-4 container_type_time_' + stored_activities_dic[time_array[i]]["activity_pk"] + '">' +
                            '<select class="btn btn-primary selectType" id="type_time"' + '>' +
                            '</select>' +
                            '</div>'

                        li = '<li class="ui-state-default activity painted" style="background-color: ' + stored_activities_dic[time_array[i]]["color"] + ';"' +
                            ' activity_pk="' + stored_activities_dic[time_array[i]]["activity_pk"] + '"' + ' color="' + stored_activities_dic[time_array[i]]["color"] + '"' +
                            ' is_speech="' + stored_activities_dic[time_array[i]]["is_speech"] + '"' + ' desc="' + stored_activities_dic[time_array[i]]["desc"] + '"' +
                            ' time="' + stored_activities_dic[time_array[i]]["time"] + '"' + ' start_hour= "' + stored_activities_dic[time_array[i]]["start_hour"] + '"' +
                            'db="' + stored_activities_dic[time_array[i]]["obj_pk"] + ' "start_time="' + stored_activities_dic[time_array[i]]["start_datetime"] + '"' +
                            'end_time="' + stored_activities_dic[time_array[i]]["end_datetime"] + '"' +
                            'id="li_' + stored_activities_dic[time_array[i]]["activity_pk"] + '"' +
                            '">'

                    }
                    if (starthour == first && stored_activities_dic[time_array[i]]["is_scheduled"]) {
                        $('#hour-' + starthour).append(
                            li +
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
                            '<button onclick="delete_actity(' + stored_activities_dic[time_array[i]]["room_pk"] + ', ' + stored_activities_dic[time_array[i]]["obj_pk"] + ')" class="btn btn-danger btn-sm deleteButton"> X </button>' +
                            '</div>' +
                            '</div>' + '</li>');
                    } else {
                        if (starthour != first) {
                            $('#hour-' + starthour).append('<div class="activity painted contained ' +'paint-'+ + stored_activities_dic[time_array[i]].activity_pk +'" + style="background-color:' + stored_activities_dic[time_array[i]].color + '">' + initprint + " a " + pkend + " " + '</div>');
                        }
                    }
                }
            }
        }
        min = min + 10
        if (min == 60) {
            min = 0
            hour += 1
        }
    }
    $(".contained").draggable({containment: "parent"});
    $(".contained").draggable({axis: "y"});

    var blocks = document.getElementsByClassName("speech_actvity")
    var option = null
    for (var i = 0; i < blocks.length; i++) {
        option = '<option disabled>' + ' Asked Time ' + blocks[i].getAttribute('speech_time_asked') + ' min' + '</option>'
        $(".container_type_time_" + blocks[i].getAttribute("activity_pk")).children().append(option)
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
        $(".container_type_time_" + blocks[i].getAttribute("activity_pk")).children().attr('onchange', 'update_times(' + blocks[i].getAttribute("activity_pk") + ', this,' + blocks[i].getAttribute('time') + ',' + 1 + ')')
    }
}


$(function () {
    $(".droppable").droppable({
        drop: function (event, ui) {
            if ($(this).attr('id') === 'speeches' || $(this).attr('id') === 'specials') {
                delete_temp_activity(ui.draggable.attr('activity_pk'), ui.draggable.attr('is_speech'));
                if (ui.draggable.attr('db')) {
                    delete_actity(room_id, ui.draggable.attr('db'));
                }
                for (var i = 0; i < time_array.length; i++) {
                    if (time_array[i] != null) {
                        if (time_array[i].split('-')[1] == ui.draggable.attr('id').split('_')[1]) {
                            time_array[i] = null
                            $(".paint-"+ui.draggable.attr('id').split('_')[1]).remove()
                        }
                    }
                }
            } else {
                if (ui.draggable.attr('is_speech') == 'true') {
                    activity_pk = "1-" + ui.draggable.attr('activity_pk');
                } else {
                    activity_pk = "0-" + ui.draggable.attr('activity_pk');
                }
                hour = event.target.getAttribute("hora").split(":")[0];
                time = ui.draggable.attr("time");
                var startPosition = validate_activity_scheduling(activity_pk, parseInt(hour), parseInt(time));
                if (startPosition >= 0) {
                    update_stored_dic(startPosition, activity_pk)
                    ui.draggable.attr('start_time', stored_activities_dic[activity_pk]['start_datetime'])
                    ui.draggable.attr('end_time', stored_activities_dic[activity_pk]['end_datetime'])
                    var element = {
                        'activity_pk': stored_activities_dic[activity_pk]['activity_pk'],
                        'color': stored_activities_dic[activity_pk]['color'],
                        'start_time': stored_activities_dic[activity_pk]['start_datetime'],
                        'end_time': stored_activities_dic[activity_pk]['end_datetime'],
                        'is_speech': stored_activities_dic[activity_pk]['is_speech'],
                        'room': room_id,
                        'description': stored_activities_dic[activity_pk]['desc'],
                    }

                    if (ui.draggable.attr('type')) {
                        element['type'] = ui.draggable.attr('type');
                    }

                    PaintActivities();
                    var value = activities_in_list(element)
                    if (value == false) {
                        lista.push(element);
                    }
                } else {
                    ui.draggable[0].remove()
                    var alerta = '<div class="alert">' +
                        '<span class="closebtn" onclick="close_alert(this)">' + "&times;" + '</span>' +
                        '<p>' + transNoTime + '</p>' +
                        '</div>'
                    $('#info-page').empty()
                    $('#info-page').append(alerta)
                    window.scrollTo(0, 0)
                    PaintActivities()
                    if (ui.draggable.attr('is_speech') != "") {
                        send_filter(null, null)
                    } else {
                        refresh_special_poll()
                    }
                }
            }
        }
    });
});

$(function () {
    var special = document.getElementsByClassName("special_actvity")
    for (var i = 0; i < special.length; ++i) {
        var element = {
            'activity_pk': special[i].getAttribute("activity_pk"),
            'color': special[i].getAttribute("color"),
            'start_time': special[i].getAttribute("start_datetime"),
            'end_time': special[i].getAttribute("end_datetime"),
            'is_speech': special[i].getAttribute("is_speech"),
            'room': special[i].getAttribute("room_pk"),
            'description': special[i].getAttribute("desc"),
        }
        lista.push(element)
    }
});

$(function () {
    var blocks = document.getElementsByClassName("speech_actvity")
    for (var i = 0; i < blocks.length; ++i) {
        var element = {
            'activity_pk': blocks[i].getAttribute("activity_pk"),
            'color': blocks[i].getAttribute("color"),
            'start_time': blocks[i].getAttribute("start_datetime"),
            'end_time': blocks[i].getAttribute("end_datetime"),
            'is_speech': blocks[i].getAttribute("is_speech"),
            'room': blocks[i].getAttribute("room_pk"),
            'description': blocks[i].getAttribute("desc"),
            'type': blocks[i].getAttribute('speech_type')
        }
        lista.push(element)
    }
    PaintActivities()
});

function delete_temp_activity(id, is_speech) {
    if (is_speech == "") {
        is_speech = ""
    }
    for (var i = 0; i < lista.length; i++) {
        if (lista[i]['activity_pk'] == id && lista[i]['is_speech'] == is_speech) {
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
            if (lista[i]['activity_pk'] == element['activity_pk']) {
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
                document.location.reload(true)
            }
        });
    } else {
        document.location.reload(true)
    }
}

function addhoras(hora, minutos) {
    starttime = new Date($("#actualDay").text() + " " + hora)
    starttime.setMinutes(starttime.getMinutes() + parseInt(minutos))
    endtime = $("#actualDay").text() + " " + starttime.getHours() + ":" + starttime.getMinutes() + ":00"
    return (endtime)
}

function send_filter(types, topics) {
    filter_speech = []
    activities_dic_list = Object.values(activities_dic)
    if (types == null && topics == null) {
        type = types
        topic = topics
    } else {
        type = $('#type').val()
        topic = $('#topic').val()
    }
    for (var i = 0; i < activities_dic_list.length; i++) {
        if (activities_dic_list[i]['is_scheduled'] == false && activities_dic_list[i]['is_speech'] == "true") {
            if (activities_dic_list[i]['speech_type'] == parseInt($('#type').val()) && $('#topic').val() == 'None') {
                filter_speech.push(activities_dic_list[i])
            } else if (activities_dic_list[i]['speech_topic'] == parseInt($('#topic').val()) && $('#type').val() == 'None') {
                filter_speech.push(activities_dic_list[i])
            } else if ($('#type').val() == 'None' && $('#topic').val() == 'None') {
                filter_speech.push(activities_dic_list[i])
            }
        }
    }

    var option = null
    $.ajax({
        url: "proposal/filterSpeeches/",
        type: "post",
        data: $("#filter").serialize(),
        success: function (data) {
            $('#speeches').empty()
            if (filter_speech.length != 0) {
                for (var i = 0; i < filter_speech.length; i++) {
                    $('#speeches').append('<li class="ui-state-default activity" style="background-color:' + filter_speech[i]['color'] + ';"' +
                        'activity_pk="' + filter_speech[i]['activity_pk'] + '" color="' + filter_speech[i]['color'] + '"' +
                        'id="li_' + filter_speech[i]['activity_pk'] +
                        '" is_speech="true"' + 'desc="none"' + 'time="' + filter_speech[i]['time'] + '">' +
                        '<div class="row">' +
                        '<div class="col-sm-8">' +
                        filter_speech[i]['title'] +
                        '</div>' +
                        '<div class="col-sm-4 container_type_time_' + filter_speech[i]['activity_pk'] + '">' +
                        '<select class="btn btn-primary" id="type_time"' + '>' +
                        '</select>' +
                        '</div>' +
                        '</div>' +
                        '</li>')
                }

                result_types = JSON.parse(data.types)
                for (var i = 0; i < filter_speech.length; i++) {
                    $(".container_type_time_" + filter_speech[i]['activity_pk']).children().empty()
                    option = '<option disabled>' + ' Asked Time ' + filter_speech[i]['speech_time_asked'] + ' min' + '</option>'
                    $(".container_type_time_" + filter_speech[i]['activity_pk']).children().append(option)
                    for (var j = 0; j < result_types.length; j++) {
                        if (Object.values(result_types[j])[1] == filter_speech[i]['speech_type']) {

                            option = '<option selected value="' + Object.values(result_types[j]['fields'])[1] +
                                "-" + Object.values(result_types[j])[1] + '">' + Object.values(result_types[j]['fields'])[0] + " (" + Object.values(result_types[j]['fields'])[1] + " minutos)"
                            '</option>'
                        } else {
                            option = '<option value="' + Object.values(result_types[j]['fields'])[1] +
                                "-" + Object.values(result_types[j])[1] + '">' + Object.values(result_types[j]['fields'])[0] + " (" + Object.values(result_types[j]['fields'])[1] + " minutos)"
                            '</option>'
                        }
                        $(".container_type_time_" + filter_speech[i]['activity_pk']).children().append(option)
                    }
                    $(".container_type_time_" + filter_speech[i]['activity_pk']).children().attr('onchange', 'update_times(' + filter_speech[i]['activity_pk'] + ', this ,' + data.times[i] + ',' + 0 + ')')

                }
            } else {
                $('#speeches').append('<p>' + transNoResult + '</p>')
            }
        }
    });
}

function update_times(speech_pk, speech_time, old_time, in_schedule) {
    if ($("#li_" + speech_pk).parent().attr('id') != 'speeches') {
        in_schedule = true
    }
    var type_values = speech_time.value.split('-')
    var start_hour = (parseInt($("#li_" + speech_pk).parent().attr('hora').split(":")[0]) - 7) * 6;
    var start_minute = parseInt($("#li_" + speech_pk).parent().attr('hora').split(":")[1]) / 10
    var start_position = start_hour + start_minute
    if (in_schedule == true) {
        var type_values = speech_time.value.split('-')
        var start_hour = (parseInt($("#li_" + speech_pk).attr('start_time').split(" ")[1].split(":")[0]) - 7) * 6;
        var start_minute = parseInt($("#li_" + speech_pk).attr('start_time').split(" ")[1].split(":")[1]) / 10
        var start_position = start_hour + start_minute
        if (control_validate_update(start_position, old_time, type_values[0]) == true) {
            update_time_array_activitiy_rescheduled(speech_pk, start_position, old_time, type_values[0])
            $(".container_type_time_" + speech_pk)[0].firstElementChild.setAttribute('onchange',
                'update_times(' + speech_pk + ',' + 'this,' + type_values[0] + ',' + 0 + ')')
            stored_activities_dic["1-" + speech_pk]['time'] = type_values[0];
            $("#li_" + speech_pk).attr('time', type_values[0])
            $("#li_" + speech_pk).attr('type', type_values[1])
            $("#li_" + speech_pk).attr('start_time', $("#li_" + speech_pk).attr('start_time'))
            $("#li_" + speech_pk).attr('end_time', addhoras($("#li_" + speech_pk).attr('start_time').split(" ")[1], type_values[0]))
            $('#' + speech_pk).attr('speech_type', type_values[1])
            $('#' + speech_pk).attr('time', type_values[0])
            stored_activities_dic["1-" + speech_pk]['start_datetime'] = $("#li_" + speech_pk).attr('start_time');
            stored_activities_dic["1-" + speech_pk]['end_datetime'] = $("#li_" + speech_pk).attr('end_time');
            for (var i = 0; i < lista.length; i++) {
                if (lista[i]['activity_pk'] == speech_pk) {
                    lista[i]['type'] = type_values[1]
                    lista[i]['start_time'] = $("#li_" + speech_pk).attr('start_time')
                    lista[i]['end_time'] = addhoras($("#li_" + speech_pk).attr('start_time').split(" ")[1], type_values[0])
                }
            }
            PaintActivities();
        } else if (control_validate_update(start_position, old_time, type_values[0]) == false) {
            var time = null
            var old_time = stored_activities_dic["1-" + speech_pk]['time']
            for (var i = 0; i < types.length; i++)
                if (Object.values(types[i])[1] == stored_activities_dic["1-" + speech_pk].speech_type) {
                    stored_activities_dic["1-" + speech_pk]['time'] = Object.values(types[i])[2]['time'];
                    time = Object.values(types[i])[2]['time']
                    update_time_array_activitiy_rescheduled(speech_pk, start_position, old_time, time)
                }
            PaintActivities();
            alert(transNoTime);
        }
    } else {
        activities_dic["1-" + speech_pk]['time'] = type_values[0];
        $(".container_type_time_" + speech_pk)[0].firstElementChild.setAttribute('onchange',
            'update_times(' + speech_pk + ',' + 'this,' + type_values[0] + ',' + 0 + ')')
        $("#li_" + speech_pk).attr('time', type_values[0])
        $("#li_" + speech_pk).attr('type', type_values[1])
        $("#li_" + speech_pk).attr('start_time', $("#actualDay").text() + " " + $("#li_" + speech_pk).parent().attr('hora'))
        $("#li_" + speech_pk).attr('end_time', addhoras($("#li_" + speech_pk).parent().attr('hora'), type_values[0]))
        for (var i = 0; i < lista.length; i++) {
            if (lista[i]['activity_pk'] == speech_pk) {
                lista[i]['type'] = type_values[1]
                lista[i]['start_time'] = $("#actualDay").text() + " " + $("#li_" + speech_pk).parent().attr('hora')
                lista[i]['end_time'] = addhoras($("#li_" + speech_pk).parent().attr('hora'), type_values[0])
            }
        }
    }
}

function refresh_special_poll() {
    special_activities = []
    activities_dic_list = Object.values(activities_dic)
    for (var i = 0; i < activities_dic_list.length; i++) {
        if (activities_dic_list[i]['is_scheduled'] == false && activities_dic_list[i]['is_speech'] == "") {
            special_activities.push(activities_dic_list[i])
        }
    }

    $('#specials').empty()
    if (special_activities.length != 0) {
        for (var i = 0; i < special_activities.length; i++) {
            $('#specials').append('<li class="ui-state-default activity" style="background-color:' + special_activities[i]['color'] + ';"' +
                'activity_pk="' + special_activities[i]['activity_pk'] + '" color="' + special_activities[i]['color'] +
                '" is_speech=""' + 'desc="none"' + special_activities[i]['desc'] + 'time="' + special_activities[i]['time'] + '">' +
                special_activities[i]['name'] +
                '</li>')
        }
    }


}

function close_alert(menssaje) {
    menssaje.parentNode.style.display = "none"

}

$(function displayOrEdit() {
    var action = editOrDisplay
    if (action == 'display') {
        $("#filterPanel").remove();
        $("#send_activities").remove();
        $(".deleteButton").remove();
        $("#addroom").remove();
        $('.activity').draggable({disabled: true});
        $('.connectedSortable').sortable({disabled: true});
        $('.selectType').remove();
        $('.container').css({'margin-left': 'auto'})
    }
});