$("#topic-modal").on('hidden.bs.modal', function(){
    $("#createTopic-form").trigger('reset');
});

$("#type-modal").on('hidden.bs.modal', function(){
    $("#createType-form").trigger('reset');
    changeTimeValue(60);
});

$("#special-modal").on('hidden.bs.modal', function(){
    $("#specialActivity-form").trigger('reset');
});

// Change icon value dinamically for every topic in the speeches panel
$('.tree_toggle_icon').click(function() {
    if ($(this).hasClass('glyphicon-chevron-down') == true) {
        $(this).removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
    } else {
        $(this).removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    }
});

function changeTimeValue(val) {
    document.getElementById("eventTimeValue").innerHTML = val + " min";
}

document.addEventListener('DOMContentLoaded', function() {
    // Treeview Initialization
    $('.tree-toggle').click(function () {
        $(this).parent().children('ul.tree').toggle(200);
    });

    $(function(){
        $('.tree-toggle').parent().children('ul.tree').toggle(200);
    });

    // Handle Treeview types filter
    $(function() {
        $("#filterSpeechesType").change(function() {
            var rex = $('#filterSpeechesType').val();
            console.log(rex);
            if (rex != "all") {
                $(".speech-type-filter").show().not('.speech_' + rex).hide();
            } else {
                $(".speech-type-filter").show();
            }
          });
    });
    // When reloading page, always start with 'all' filter
    $('select[id^="filterSpeechesType"] option:selected').attr("selected",null);
    $('select[id^="filterSpeechesType"] option[value="all"]').attr("selected","selected");
});

(function(){
    $('input[name="color"]').val($('input[name="color"]').attr('value'));
})();

$("#createTopic-form").submit(function (submitEl) {
        // preventing from page reload and default actions
        submitEl.preventDefault();
        url = create_topic_url;
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: url,
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken
            },
            data: $("#createTopic-form").serialize(),
            error: function (response) {
                // alert the error if any error occurred
                if (response.status == 400) {
                    alertEl = document.getElementById("wrongTopicFormAlert")
                    alertEl.style.setProperty("display", "block");
                    alertEl.innerText = "Los datos ingresados son érroneos, corríjalos e intente de nuevo.";
                }
                else {
                    $("#createTopic-form").trigger('reset');
                    handleResponseErrors(response.status, '');
                }
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#createTopic-form").trigger('reset');
                $("#topic-modal").modal('hide');
                // Manage response status code
                handleResponseErrors(200, '¡Tema guardado correctamente!');
                // Add the new topic into the speeches panel
                var topics_obj = `<li><label class="tree-toggle glyphicon-icon-rpad">${response.name} <span class="menu-collapsible-icon glyphicon glyphicon-chevron-down"></span></label></li>`;
                $("#ul-topics-panel").append(topics_obj);
            }
        })
    });

$("#createType-form").submit(function (submitEl) {
        // preventing from page reload and default actions
        submitEl.preventDefault();
        url = create_type_url;
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: url,
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken
            },
            data: $("#createType-form").serialize(),
            error: function (response) {
                // alert the error if any error occurred
                if (response.status == 400) {
                    alertEl = document.getElementById("wrongTypeFormAlert")
                    alertEl.style.setProperty("display", "block");
                    alertEl.innerText = "Los datos ingresados son érroneos, corríjalos e intente de nuevo.";
                }
                else {
                    $("#createType-form").trigger('reset');
                    handleResponseErrors(response.status, '');
                }
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#createType-form").trigger('reset');
                $("#type-modal").modal('hide');
                // Manage response status code
                handleResponseErrors(200, '¡Tipo de actividad guardado correctamente!');
                if(response.is_special){

                     $("#specialActivity-form #id_type").append($('<option>', {
                            value: response.pk,
                            text: `${response.name} (${response.time} minutos)`,
                        }));
                }else{
                    $("#filterSpeechesType").append(`<option time={{ ${response.time} }} value={{ ${response.event} }}>${response.name} (${response.time} minutos)</option>`);
                }
            }
        })
    });

$("#specialActivity-form").submit(function (submitEl) {
        // preventing from page reload and default actions
        submitEl.preventDefault();
        url = create_special_url;
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: url,
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken
            },
            data: $("#specialActivity-form").serialize(),
            error: function (response) {
                // alert the error if any error occurred
                if (response.status == 400) {
                    alertEl = document.getElementById("wrongSpecialFormAlert")
                    alertEl.style.setProperty("display", "block");
                    alertEl.innerText = "Los datos ingresados son érroneos, corríjalos e intente de nuevo.";
                }
                else {
                    $("#specialActivity-form").trigger('reset');
                    handleResponseErrors(response.status, '');
                }
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#specialActivity-form").trigger('reset');
                $("#special-modal").modal('hide');
                handleResponseErrors(200, '¡Actividad especial guardada correctamente!');
                $("#specials").load(location.href + " #specials");
            }
        })
    });