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
                else if (response.status == 500) {
                    $("#createTopic-form").trigger('reset');
                    alertEl = document.getElementById("wrongTopicFormAlert")
                    alertEl.style.setProperty("display", "block");
                    alertEl.innerText = "Hubo un error procesando sus datos, inténtelo más tarde.";
                }
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#createTopic-form").trigger('reset');
                $("#topic-modal").modal('hide');
                const Toast = Swal.mixin({
                                    toast: true,
                                    position: 'top',
                                    showConfirmButton: false,
                                    timer: 3000,
                                    timerProgressBar: true,
                                    didOpen: (toast) => {
                                        toast.addEventListener('mouseenter', Swal.stopTimer)
                                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                                    }
                                    })

                Toast.fire({
                            icon: 'success',
                            title: 'Tema guardado correctamente'
                            });

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
                else if (response.status == 500) {
                    $("#createType-form").trigger('reset');
                    alertEl = document.getElementById("wrongTypeFormAlert")
                    alertEl.style.setProperty("display", "block");
                    alertEl.innerText = "Hubo un error procesando sus datos, inténtelo más tarde.";
                }
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#createType-form").trigger('reset');
                $("#type-modal").modal('hide');
                $("#filterSpeechesType").append(`<option time={{ ${response.time} }} value={{ ${response.event} }}>${response.name} (${response.time} minutos)</option>`)
                const Toast = Swal.mixin({
                                    toast: true,
                                    position: 'top-end',
                                    showConfirmButton: false,
                                    timer: 3000,
                                    timerProgressBar: true,
                                    didOpen: (toast) => {
                                        toast.addEventListener('mouseenter', Swal.stopTimer)
                                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                                    }
                                    })

                Toast.fire({
                            icon: 'success',
                            title: 'Tipo de actividad guardado correctamente'
                            });
                if(response.is_special){
                     new_option = `<option value={{ ${response.pk} }}>${response.name} (${response.time} minutos)</option>`;
                     $("#specialActivity-form")[0][2].append(new_option);
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
                else if (response.status == 500) {
                    $("#specialActivity-form").trigger('reset');
                    alertEl = document.getElementById("wrongSpecialFormAlert")
                    alertEl.style.setProperty("display", "block");
                    alertEl.innerText = "Hubo un error procesando sus datos, inténtelo más tarde.";
                }
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#specialActivity-form").trigger('reset');
                $("#special-modal").modal('hide');
                const Toast = Swal.mixin({
                                    toast: true,
                                    position: 'top',
                                    showConfirmButton: false,
                                    timer: 3000,
                                    timerProgressBar: true,
                                    didOpen: (toast) => {
                                        toast.addEventListener('mouseenter', Swal.stopTimer)
                                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                                    }
                                    })

                Toast.fire({
                            icon: 'success',
                            title: 'Actividad especial guardada correctamente'
                            });
            }
        })
    });