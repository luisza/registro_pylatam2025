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
        handleResponseErrors(response.status, '¡Horario guardado correctamente!');
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
            slotMinTime: '07:00:00',
            slotMaxTime: '23:00:00',
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
        let panel_event_element = `<li id="speech_${event.id}" class="ui-state-default activity speech-type-filter speech_${event.speech_type_id}" style="border-style: solid; width: 100%; padding: 0; margin-top: 5px;"><div class="row" style="margin: 5px 0px 5px 0px;" data-speech="${event.id}" data-topic="${event.topic_id}" data-color="${event.color}" data-duration="${event.speech_type_time}" style="text-overflow: ellipsis;overflow: hidden;"><div class="col-sm-6 speech-text">${event.title}</div><div class="col-sm-6">${event.speech_type_time} min - ${event.speech_type_name}</div></div></li>`;
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
                html_panel_el: panel_event_element
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
        itemSelector: '.speech-type-filter',
        eventData: function(eventEl) {
            return {
                title: eventEl.children[0].children[0].innerText,
                backgroundColor: eventEl.children[0].getAttribute('data-color'),
                duration: {minutes:eventEl.children[0].getAttribute('data-duration')},
                extendedProps: {
                    speech_id: eventEl.children[0].getAttribute('data-speech'),
                    topic_id: eventEl.children[0].getAttribute('data-topic'),
                    html_panel_el: eventEl,
                }
            };
        }
    });

    new FullCalendar.Draggable(special_activity_containerEl, {
        itemSelector: '.special-draggable',
        eventData: function(eventEl) {
            return {
                title: eventEl.children[0].children[0].innerText,
                duration: {minutes:eventEl.children[0].getAttribute('data-duration')},
                extendedProps: {
                    special_activity_id: eventEl.children[0].getAttribute('data-special'),
                    html_panel_el: eventEl,
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

// Show message when create new room
$('#create_room_form').submit(function(submitEl){
    submitEl.preventDefault();
    $.ajax({
        url: create_room_url,
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data : $('#create_room_form').serialize(),
        error: function (response) {
            // alert the error if any error occurred
            if (response.status == 400) {
                alertEl = document.getElementById("wrongRoomFormAlert")
                alertEl.style.setProperty("display", "block");
                alertEl.innerText = "Los datos ingresados son érroneos, corríjalos e intente de nuevo.";
            }
            else {
                $("#create_room_form").trigger('reset');
                handleResponseErrors(response.status, '');
            }
        },
        success: function(response){
            handleResponseErrors(200, '¡Sala guardada correctamente!');

            $("#room_modal").modal('hide');

            let events = []
            for (let i = 0; i < calendars.length; i++) {
                events.push(...calendars[i].getEvents());
            }
            // Remove events from calendar
            deleteEventsFromCalendar(removed_events);
            // Save events that are currently in the calendar
            saveEvents(events);

            location.reload();

        }
    });
    return false;
});
