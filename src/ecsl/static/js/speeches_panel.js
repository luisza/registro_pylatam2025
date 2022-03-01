document.addEventListener('DOMContentLoaded', function() {
    // Treeview Initialization
    $('.tree-toggle').click(function () {
        $(this).parent().children('ul.tree').toggle(200);
    });

    $(function(){
        $('.tree-toggle').parent().children('ul.tree').toggle(200);
    });
});

$("#createTopic-form").submit(function (submitEl) {
        // preventing from page reload and default actions
        submitEl.preventDefault();
        url = create_topic_url;
        // serialize the data for sending the form data.
        var formData = document.forms['createTopic-form'];
        var serializedData = {
            "name": formData['id_name'].value,
            "color": formData['topicColorInput'].value
        }
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: url,
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            dataType: "json",
            data: serializedData,
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            },
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#createTopic-form").trigger('reset');

            }
        })
    })