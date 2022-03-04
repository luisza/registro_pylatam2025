var calendars = [];
var removed_events = [];

window.addEventListener("load", function(){
    var saveButton = document.getElementsByClassName("fc-saveButton-button");
    for (let i=0;i<saveButton.length;i++){
        saveButton[i].style.setProperty("background-color", "green");
        saveButton[i].style.setProperty("border-color", "green");
    };
});

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
    }).then(response => {
        if(response.status == 201){
            const toast = Swal.mixin({
                toast: true,
                position: 'top',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            });

            toast.fire({
                icon: 'success',
                title: '¡Horario guardado correctamente!'
            });
        }
        return response.json()
    }).then(events => {
        for (let i = 0; i < calendars.length; i++) {
            calendars[i].setEventsID(events);
        }
    });
}

function deleteEventsFromCalendar(events_id) {
    fetch(delete_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify(Object.assign({}, removed_events))
    }).then(function(response){
        if(response.status == 200){
            removed_events = [];
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
            eventOverlap: false,
            customButtons: {
                saveButton: {
                  text: save_name,
                  click: function() {
                    let events = []
                    for (let i = 0; i < calendars.length; i++) {
                        events.push(...calendars[i].getEvents());
                    }
                    // Remove events from calendar
                    deleteEventsFromCalendar(removed_events);
                    // Save events that are currently in the calendar
                    saveEvents(events);
                  }
                }
              },
            validRange: {
                        start: start_date_parsed,
                        end: end_date_plus_one,
                    },
            headerToolbar: {
              left: 'saveButton',
              center: 'title',
              right: 'prev,next timeGridOneDay,timeGridEventDates'
            },
            views: {
                timeGridOneDay: {
                        type: 'timeGridDay',
                        buttonText: day_name,
                    },
                timeGridEventDates: {
                    type: 'timeGrid',
                    visibleRange: {
                        start: start_date_parsed,
                        end: end_date_plus_one,
                    },
                    buttonText: whole_event_name,
                },
            },
            eventReceive: function(info) {
                // Remove element from
                if(info.event.extendedProps.speech_id != undefined){
                    $(info.draggedEl).closest('.activity').remove();
                }
            },
            eventDidMount: function(info){
                // Set event UUID
                let uuid = info.event.extendedProps.html_id ? info.event.extendedProps.html_id : getRandomUUID();
                info.event.setExtendedProp('html_id', uuid);
                // Append x icon to delete
                let icon = document.createElement("i");
                icon.classList.add('far', 'fa-times-circle');
                icon.style.cssText = "position: absolute; top: 2px; right: 2px;font-size: 16px; z-index: 10000"
                info.el.prepend(icon);
                $(icon).on('click', function() {
                    removed_events.push(uuid);
                    info.event.remove();
                    console.log(info.event.extendedProps.html_panel_el);
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
            title: (event.title).toUpperCase(),
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
    let speech_containerEl = document.getElementById('draggable-events');
    let special_activity_containerEl = document.getElementById('draggable-special-activities');
    new FullCalendar.Draggable(speech_containerEl, {
        itemSelector: '.speech-text',
        eventData: function(eventEl) {
            return {
                title: eventEl.innerText,
                backgroundColor: eventEl.parentNode.getAttribute('data-color'),
                duration: {minutes:eventEl.parentNode.getAttribute('data-duration')},
                extendedProps: {
                    speech_id: eventEl.parentNode.getAttribute('data-speech'),
                    special_activity_id: eventEl.parentNode.getAttribute('data-special'),
                    topic_id: eventEl.parentNode.getAttribute('data-topic'),
                    html_panel_el: eventEl.parentNode.parentNode,
                }
            };
        }
    });

    new FullCalendar.Draggable(special_activity_containerEl, {
        itemSelector: '.special-activity',
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
        let calendar_index = e.target.getAttribute('data-num');
        calendars[calendar_index-1].render();
        calendars[calendar_index-1].getCalendar().setOption('droppable', true);
        for (let i = 0; i < calendars.length; i++) {
            if (calendar_index-1 != i){
                calendars[calendar_index-1].getCalendar().setOption('droppable', false);
            }
        }
    });
});


