document.addEventListener('DOMContentLoaded', function() {
    let Calendar = FullCalendar.Calendar;
    let Draggable = FullCalendar.Draggable;
    var calendars = [];
    var containerEl = document.getElementById('draggable-events');

    // Treeview Initialization
    $('.tree-toggle').click(function () {
        $(this).parent().children('ul.tree').toggle(200);
    });
    $(function(){
        $('.tree-toggle').parent().children('ul.tree').toggle(200);
    });

    $('#calendar-1-tab').tab('show');
    $('.full-calendar').each(function(i, cal) {
        start_date_parsed = Date.parse(cal.getAttribute('data-start_date'))
        end_date_parsed = Date.parse(cal.getAttribute('data-end_date'))
        end_date_plus_one = end_date_parsed + (3600*1000*24)

        // Initialize external events
        new Draggable(containerEl, {
            itemSelector: '.speech-text',
            eventData: function(eventEl) {
                return {
                    title: eventEl.innerText,
                    backgroundColor: eventEl.getAttribute('data-color'),
                    duration: {minutes:eventEl.getAttribute('data-duration')},
                    extendedProps: {
                        speech_id: eventEl.getAttribute('data-speech'),
                        special_activity_id: eventEl.getAttribute('data-special')
                    }
                };
            }
        });

        // Initialize the calendar
        let calendar = new Calendar(cal, {
            editable: true,
            droppable: true,
            initialView: 'timeGridEventDates',
            allDaySlot: false,
            forceEventDuration: true,
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
                // Remove the element from the "Draggable Events" list
                info.draggedEl.parentNode.parentNode.parentNode.removeChild(info.draggedEl.parentNode.parentNode);
            }
        });
        calendars.push(calendar);
        calendar.render();
    });

    $('.room-tab').on('shown.bs.tab', function(e) {
        calendar_index = e.target.getAttribute('data-num');
        calendars[calendar_index-1].render();
    });

    $('#save').on('click', function(e) {
        events = []
        for (let i = 0; i < calendars.length; i++) {
            calendars[i].getEvents().forEach(function(event, index) {
                let room_id = $(`#calendar-${i+1}-tab`).attr('data-room-id');
                events.push({
                    'start_time': event.start,
                    'end_time': event.end,
                    'room': room_id,
                    'speech': event.extendedProps.speech_id != undefined ? event.extendedProps.speech_id : null,
                    'special': event.extendedProps.special_activity_id != undefined ? event.extendedProps.special_activity_id : null
                });
            });
        }
    });
});


