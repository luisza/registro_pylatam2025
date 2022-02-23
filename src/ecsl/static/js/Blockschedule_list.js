document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    start_date_parsed = Date.parse(calendarEl.getAttribute('data-start_date'))
    end_date_parsed = Date.parse(calendarEl.getAttribute('data-end_date'))
    end_date_plus_one = end_date_parsed + (3600*1000*24)

    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridEventDates',
        allDaySlot: false,

        headerToolbar: {
          right: 'timeGridDay,timeGridEventDates'
        },
        views: {
            timeGridEventDates: {
                type: 'timeGrid',
                visibleRange: {
                    start: start_date_parsed,
                    end: end_date_plus_one,
                },
                buttonText: 'whole event',
          }
    }});
    calendar.render();
});
