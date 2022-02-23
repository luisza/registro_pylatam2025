document.addEventListener('DOMContentLoaded', function() {
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
    var calendar = new Calendar(calendarEl, {
        editable: true,
        droppable: true,
        initialView: 'timeGridWeek',
        allDaySlot: false
    });

    calendar.render();
});
