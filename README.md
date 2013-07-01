# scrambleapi

Event API for Scramble app

## Event format

Events have the following attributes: `id`, `title`, `description`, `startDate`
and optional `endDate`.

## Supported Endpoints

### /api/events

Returns a list of events sorted by startDate.

Optional filtering:
  - `starts_on_or_after_date`: integer number of seconds since the epoch in UTC
  - `starts_before_date`: integer number of seconds since the epoch in UTC
  - `limit`: integer greater than zero
  - `offset`: integer greater than zero

### /api/event/{event_id}

Returns a single event in json format.
