document.addEventListener('DOMContentLoaded', function() {
    $('.full-calendar').each(function(i, cal) {
        let calendar = new FullCalendar.Calendar(cal, {
            initialView: 'timeGridWeek',
            allDaySlot: false
        });
        calendar.render();
    });
});
