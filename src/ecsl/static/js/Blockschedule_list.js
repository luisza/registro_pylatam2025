document.addEventListener('DOMContentLoaded', function() {
    let Calendar = FullCalendar.Calendar;
    let Draggable = FullCalendar.Draggable;


    var containerEl = document.getElementById('draggable-events');
    $('.full-calendar').each(function(i, cal) {
        start_date_parsed = Date.parse(cal.getAttribute('data-start_date'))
        end_date_parsed = Date.parse(cal.getAttribute('data-end_date'))
        end_date_plus_one = end_date_parsed + (3600*1000*24)

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
});
