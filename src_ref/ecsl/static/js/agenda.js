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
            height: 'auto',
            editable: false,
            droppable: false,
            initialView: 'timeGridEventDates',
            allDaySlot: false,
            forceEventDuration: true,
            slotDuration: { minutes:10 },
            slotLabelInterval: { hours:1 },
            slotMinTime: '07:00:00',
            slotMaxTime: '23:00:00',
            validRange: {
                start: start_date_parsed,
                end: end_date_plus_one,
            },
            headerToolbar: {
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
    });
});


