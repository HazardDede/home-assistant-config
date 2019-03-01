"""
Groups iCal events by their summary and provides a sensor for each group.
Each sensor will show the next event that will occur.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.icalendar/
"""
import logging
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_EXCLUDE, CONF_INCLUDE, CONF_URL
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

REQUIREMENTS = ['icalevents==0.1.19']

_LOGGER = logging.getLogger(__name__)

ATTR_DAYS_LEFT = 'days_left'
ATTR_FRIENDLY_DELTA = 'friendly_delta'

CONF_DATE_FORMAT = 'date_format'
CONF_DATE_FORMAT_DEFAULT = '%Y-%m-%d %H:%M'
CONF_DAYS_IN_FUTURE = 'future'
CONF_DAYS_IN_FUTURE_DEFAULT = 365

ICON_DEFAULT = 'mdi:calendar'

# Return cached results if last scan was less then this time ago.
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL):
        vol.Any(cv.url, cv.isfile),
    vol.Optional(CONF_DATE_FORMAT, default=CONF_DATE_FORMAT_DEFAULT):
        cv.string,
    vol.Optional(CONF_EXCLUDE, default=[]):
        vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_INCLUDE, default=[]):
        vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_DAYS_IN_FUTURE, default=CONF_DAYS_IN_FUTURE_DEFAULT):
        cv.positive_int
})

SCAN_INTERVAL = timedelta(minutes=5)


def setup_platform(hass, config, add_devices, discovery_info=None):
    url = config.get(CONF_URL)
    date_format = config.get(CONF_DATE_FORMAT)
    exclude = config.get(CONF_EXCLUDE)
    include = config.get(CONF_INCLUDE)
    future = config.get(CONF_DAYS_IN_FUTURE)

    data_object = ICalNextEventData(url, future, include, exclude)
    try:
        data_object.update()
        evts = data_object.data
    except Exception:
        import traceback
        _LOGGER.warning(traceback.format_exc())
        raise PlatformNotReady()

    devices = [ICalNextEventSensor(evt_name, date_format, data_object)
               for evt_name, _ in evts.items()]
    if not devices:
        _LOGGER.warning("There are no iCal events between now() and"
                        "now() + %s days", str(future))
    add_devices(devices, True)


class ICalNextEventSensor(Entity):
    """Implementation of an iCal event."""

    def __init__(self, event_name, date_format, data_object):
        """Initialize the sensor."""
        self._name = event_name
        self._event_name = event_name
        self.date_format = date_format
        self.data_object = data_object
        self._state_attrs = {}
        self._state = None
        # Regex to extract the human readable delta from the str representation
        # of event model
        self.friendly_delta_regex = re.compile(r"^.*: .* \((?P<delta>.*)\)$")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon for the frontend."""
        return ICON_DEFAULT

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs

    def _fmt_date(self, event):
        """Formats a date using the stored date_format."""
        return event.start.strftime(self.date_format)

    def _fmt_delta(self, event, dt):
        """Formats the delta (from now to event start) in a human readable
        format."""
        m = self.friendly_delta_regex.match(str(event))
        return m.group('delta') if m else None

    def update(self):
        """Fetch new state data for the sensor."""
        self.data_object.update()
        evts = self.data_object.data
        # Maybe the event is gone or there is no next event -> Unknown.
        new_state = evts.get(self._name) or None
        if new_state is None:
            self._state = None
        else:
            from dateutil.tz import UTC
            dt = datetime.now(UTC)
            self._state = self._fmt_date(new_state)
            self._state_attrs = {
                ATTR_DAYS_LEFT: new_state.time_left(dt).days,
                ATTR_FRIENDLY_DELTA: self._fmt_delta(new_state, dt)
            }


class ICalNextEventData:
    """Class for handling data retrieval."""

    def __init__(self, url, future, include, exclude):
        self.url = url  # Url or local file.
        self.future = future  # Days in future to look for events.
        self.include = include  # Include specific events.
        self.exclude = exclude  # Exclude specific events.
        self.data = {}  # Data store.

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        # Transform include/exclude to lower-case.
        # We'll later transform the other "end" to lower case, too.
        include = [inc.lower() for inc in self.include or []]
        exclude = [exc.lower() for exc in self.exclude or []]

        def _should_add(evt_name):
            # Include overrides exclude.
            if include and evt_name.lower() in include:
                return True
            if not exclude or evt_name.lower() not in exclude:
                return not include
            return False

        if os.path.isfile(self.url):
            kwargs = {'file': self.url}
        else:
            kwargs = {'url': self.url}

        from icalevents.icalevents import events
        # Get ical events from now + x (future) days.
        evts = events(
            start=datetime.now(),
            end=datetime.now() + timedelta(days=self.future),
            fix_apple=True,
            **kwargs
        )
        # Group events by summary.
        grpd = defaultdict(list)
        for e in evts:
            grpd[e.summary].append(e)
        # Only grab the next event for each group/summary.
        next_events = {k: sorted(v, key=lambda x: x.start)[0]
                       for k, v in grpd.items() if _should_add(k)}
        self.data = next_events
