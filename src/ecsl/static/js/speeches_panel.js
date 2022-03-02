document.addEventListener('DOMContentLoaded', function() {
    // Treeview Initialization
    $('.tree-toggle').click(function () {
        $(this).parent().children('ul.tree').toggle(200);
    });

    $(function(){
        $('.tree-toggle').parent().children('ul.tree').toggle(200);
    });
});

(function(){
    $('input[name="color"]').val($('input[name="color"]').attr('value'));
})();

$("#createTopic-form").submit(function (submitEl) {
        // preventing from page reload and default actions
        submitEl.preventDefault();
        url = create_topic_url;
        // serialize the data for sending the form data.
       /** var formData = document.forms['createTopic-form'];
        var serializedData = {
            "name": formData['id_name'].value,
            "color": formData['topicColorInput'].value,
            "csrfmiddlewaretoken": formData['csrfmiddlewaretoken'].value,
            "event": formData['event'].value
        }
        */
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: url,
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken
            },
           // dataType: "json",
            //data: serializedData,
            data: $("#createTopic-form").serialize(),
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#createTopic-form").trigger('reset');
                $("#topic-modal").modal('hide');
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
                                    title: 'Element saved successfully.'
                                    });


            }
        })
    })