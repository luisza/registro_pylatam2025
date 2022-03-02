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
            if (rex != "all") {
                $(".ui-state-default").show().not('#' + rex).hide();
            } else {
                $(".ui-state-default").show();
            }
          });
    });
});