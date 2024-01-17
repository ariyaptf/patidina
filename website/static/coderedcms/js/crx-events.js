/*
Wagtail CRX (https://www.coderedcorp.com/cms/)
Copyright 2018-2023 CodeRed LLC
License: https://github.com/coderedcorp/coderedcms/blob/main/LICENSE
@license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
*/

document.addEventListener("DOMContentLoaded", function() {
    const calendars = document.querySelectorAll("[data-block='calendar']");
    calendars.forEach(function(el) {
        const pageId = el.dataset.pageId; // data-page-id
        const defaultDate = el.dataset.defaultDate; // data-default-date
        const defaultView = el.dataset.defaultView; // data-default-view
        const eventDisplay = el.dataset.eventDisplay; // data-event-display
        const eventSourceUrl = el.dataset.eventSourceUrl; // data-event-source-url
        const timezone = el.dataset.timezone; // data-timezone

        const calendar = new FullCalendar.Calendar(el, {
            locale: 'th',
            headerToolbar: {
                left: "prev",
                center: "title",
                right: "next",
            },
            themeSystem: "bootstrap5",
            buttonText: {
                prev: "←",
                next: "→",
                today:"วันนี้",
            },
            initialDate: defaultDate,
            initialView: defaultView,
            fixedWeekCount: false,
            timeZone: timezone,
            eventDisplay: eventDisplay,
            eventSources: [{
                url: eventSourceUrl,
                method: "GET",
                extraParams: {
                    pid: pageId,
                },
            }, ],
        });

        calendar.render();
    });
});
/* @license-end */
