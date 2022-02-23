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
            slotDuration: { minutes:10 },
            slotLabelInterval: { hours:1 },

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
                },
            },
            // Remove the dragged event from the panel and located into the calendar obj
            drop: function(info) {
                console.log(info)
                // Remove the element from the "Draggable Events" list
                info.draggedEl.parentNode.parentNode.parentNode.removeChild(info.draggedEl.parentNode.parentNode);
            }
        });
        calendar.render();
    });
});
