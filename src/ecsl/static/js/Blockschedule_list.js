document.addEventListener('DOMContentLoaded', function() {
    let Calendar = FullCalendar.Calendar;
    let Draggable = FullCalendar.Draggable;
    var containerEl = document.getElementById('draggable-events');
    $('.full-calendar').each(function(i, cal) {
        // Initialize external events
        new Draggable(containerEl, {
            itemSelector: '.speech-text',
            eventData: function(eventEl) {
                return {
                    title: eventEl.innerText
                };
            }
        });

        // Initialize the calendar
        let calendar = new Calendar(cal, {
            editable: true,
            droppable: true,
            initialView: 'timeGridWeek',
            allDaySlot: false
        });

        calendar.render();
    });
});
