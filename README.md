scrambleapi
===========

Event API for Scramble app

Event format
------------

Events have a `title`, `description`, `startDate` and optional `endDate`.

Supported Endpoints
-------------------

/api/events
~~~~~~~~~~~~~~~~~~~~~

Returns a list of events.

Optional filter arguments:

`from_date`
`to_date`

/api/event/{event_id}
~~~~~~~~~~~~~~~~~~~~~

Returns a single event in json format.
