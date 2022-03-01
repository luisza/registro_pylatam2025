var calendars = [];

function saveEvents(events){
    fetch(save_url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify(events)
    }).then(response => response.json())
    .then(events => {
        for (let i = 0; i < calendars.length; i++) {
            calendars[i].setEventsID(events);
        }
    });
}

function getRandomUUID() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

class Calendar {
    constructor(cal_html, room){
        this.room = room;
        this.calendar = new FullCalendar.Calendar(cal_html, {
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
                $(info.draggedEl).closest('.activity').remove();
            },
            eventReceive: function(info) {
                // Remove the element from the "Draggable Events" list
                info.event.setExtendedProp('html_id', getRandomUUID());
            }
        });
    }

    getCalendar(){
        return this.calendar;
    }

    getEvents(){
        let events = [];
        let room_id = $(`#calendar-${this.room+1}-tab`).attr('data-room-id');
        this.calendar.getEvents().forEach(function(event, index) {
            events.push({
                'id': event.id,
                'html_id': event.extendedProps.html_id,
                'start_time': event.start,
                'end_time': event.end,
                'room': room_id,
                'speech': event.extendedProps.speech_id != undefined ? event.extendedProps.speech_id : null,
                'special': event.extendedProps.special_activity_id != undefined ? event.extendedProps.special_activity_id : null
            });
        });
        return events;
    }

    getEventByHtmlId(id){
        this.calendar.getEvents().forEach(function(event, index) {
            event.setProp('html_id', events)
        });
    }

    setEventsID(events){
        this.calendar.getEvents().forEach(function(event, index) {
            for (let i = 0; i < events.length; i++) {
                if(events[i].html_id == event.extendedProps.html_id){
                    event.setProp('id', events[i].id);
                    continue;
                }
            }
        });
    }

    render(){
        this.calendar.render();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialize external events
    let containerEl = document.getElementById('draggable-events');
    new FullCalendar.Draggable(containerEl, {
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

    // Treeview Initialization
    $('.tree-toggle').click(function () {
        $(this).parent().children('ul.tree').toggle(200);
    });

    $(function(){
        $('.tree-toggle').parent().children('ul.tree').toggle(200);
    });

    function changeTimeValue(val) {
        document.getElementById("eventTimeValue").innerHTML = val + " minutos";
    }

    $('#calendar-1-tab').tab('show');
    $('.full-calendar').each(function(i, cal) {
        start_date_parsed = Date.parse(cal.getAttribute('data-start_date'))
        end_date_parsed = Date.parse(cal.getAttribute('data-end_date'))
        end_date_plus_one = end_date_parsed + (3600*1000*24)

        // Initialize the calendar
        let calendar = new Calendar(cal, i);
        calendars.push(calendar);
        calendar.render();
    });

    $('.room-tab').on('shown.bs.tab', function(e) {
        calendar_index = e.target.getAttribute('data-num');
        calendars[calendar_index-1].render();
    });

    $('#save-btn').on('click', function(e) {
        events = []
        for (let i = 0; i < calendars.length; i++) {
            events.push(...calendars[i].getEvents());
        }
        saveEvents(events);
    });
});

