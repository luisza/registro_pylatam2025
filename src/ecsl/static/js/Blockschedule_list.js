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

function changeTimeValue(val) {
    document.getElementById("eventTimeValue").innerHTML = val + " minutos";
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
            eventOverlap: false,
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
            eventReceive: function(info) {
                // Set event UUID
                info.event.setExtendedProp('html_id', getRandomUUID());
                // Remove element from
                $(info.draggedEl).closest('.activity').remove();
            },
            eventDidMount: function(info){
                // Append x icon to delete
                let icon = document.createElement("i");
                icon.setAttribute("id", info.event._instance.instanceId);
                icon.classList.add('far', 'fa-times-circle');
                icon.style.cssText = "position: absolute; top: 2px; right: 2px;font-size: 16px; z-index: 10000"
                info.el.prepend(icon);

                $(icon).on('click', function() {
                    console.log(info.event.extendedProps);
                    info.event.remove();
                    $(`#topic_speeches_${info.event.extendedProps.topic_id}`).append(info.event.extendedProps.html_panel_el);
                })
            }
        });
    }

    getCalendar(){
        return this.calendar;
    }

    getEvents(){
        let events = [];
        let room_id = this.room;
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

    addEvent(event){
        this.calendar.addEvent({
            id: event.id,
            title: event.title,
            start: event.start_time,
            end: event.end_time,
            backgroundColor: event.color,
            extendedProps: {
                speech_id: event.speech_id,
                special_activity_id: event.special_id,
                html_id: event.html_id,
                topic_id: event.topic_id,
            }
        })
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
            console.log(eventEl);
            return {
                title: eventEl.innerText,
                backgroundColor: eventEl.getAttribute('data-color'),
                duration: {minutes:eventEl.getAttribute('data-duration')},
                extendedProps: {
                    speech_id: eventEl.getAttribute('data-speech'),
                    special_activity_id: eventEl.getAttribute('data-special'),
                    topic_id: eventEl.getAttribute('data-topic'),
                    html_panel_el: eventEl.parentNode,
                }
            };
        }
    });

    function changeTimeValue(val) {
        document.getElementById("eventTimeValue").innerHTML = val + " minutos";
    }

    $('#calendar-1-tab').tab('show');
    $('.full-calendar').each(function(i, cal) {
        start_date_parsed = Date.parse(cal.getAttribute('data-start_date'))
        end_date_parsed = Date.parse(cal.getAttribute('data-end_date'))
        end_date_plus_one = end_date_parsed + (3600*1000*24)
        let room_id = $(`#calendar-${i+1}-tab`).attr('data-room-id');

        // Initialize the calendar
        let calendar = new Calendar(cal, room_id);

        // Add events
        for (let i = 0; i < scheduled_events.length; i++) {
            if(scheduled_events[i].room == room_id){
                calendar.addEvent(scheduled_events[i]);
            }
        }

        calendars.push(calendar);
        calendar.render();
    });

    $('.room-tab').on('shown.bs.tab', function(e) {
        calendar_index = e.target.getAttribute('data-num');
        calendars[calendar_index-1].render();
        calendars[calendar_index-1].setOption('droppable', true);
        for (let i = 0; i < calendars.length; i++) {
            if(calendar_index-1 != i){
                calendars[calendar_index].setOption('droppable', false);
            }
        }


    });

    $('#save-btn').on('click', function(e) {
        events = []
        for (let i = 0; i < calendars.length; i++) {
            events.push(...calendars[i].getEvents());
        }
        saveEvents(events);
    });
});


