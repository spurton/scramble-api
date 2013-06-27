= scrambleapi

Event API for Scramble app

== Event format

Events have the following attributes: `id`, `title`, `description`, `startDate`
and optional `endDate`.

== Supported Endpoints

=== /api/events

Returns a list of events sorted by startDate.

=== /api/event/{event_id}

Returns a single event in json format.
