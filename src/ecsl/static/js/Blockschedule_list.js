document.addEventListener('DOMContentLoaded', function() {
    $('.full-calendar').each(function(i, cal) {
        var Calendar = FullCalendar.Calendar;
        var Draggable = FullCalendar.Draggable;

        var containerEl = document.getElementById('draggable-events');
        var calendarEl = document.getElementById('calendar');

        // Initialize external events
        new Draggable(containerEl, {
            itemSelector: '.ui-state-default',
            eventData: function(eventEl) {
                return {
                    title: eventEl.innerText
                };
            }
        });

        // Initialize the calendar
        var calendar = new Calendar(cal, {
            editable: true,
            droppable: true,
            initialView: 'timeGridWeek',
            allDaySlot: false
        });

        calendar.render();
    });
});
