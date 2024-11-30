import os
import json
import uuid
import threading

import pychromecast


class ChromecastGroup():

    def __init__(self, cache_file="~/.config/cc-volume/devices.json"):
        self.cache_file = os.path.expanduser(cache_file)
        self._chromecasts = []
        self.load_chromecasts(self.cache_file)

    def scan_chromecasts(self):
        uuid_set = set(self.state['uuids'])
        host_set = set(self.state['hosts'])

        scan_result = pychromecast.get_chromecasts()
        chromecasts = scan_result[0]

        # iterate UUIDs and hosts to check if there are any changes
        new_uuid_set = set([ str(c.uuid) for c in chromecasts ])
        new_host_set = set([ c.cast_info.host for c in chromecasts ])

        # if the sets are the same, do not save
        if uuid_set == new_uuid_set and host_set == new_host_set:
            return
        else:
            self._chromecasts = sorted(chromecasts, key=lambda x: x.cast_info.friendly_name)
            return True

    def load_chromecasts(self, cache_file):
        try:
            with open(cache_file, "rb") as f:
                state = json.load(f)
                scan_result = pychromecast.get_listed_chromecasts(
                    uuids=[ uuid.UUID(u) for u in state['uuids'] ],
                    known_hosts=state['hosts']
                )
                chromecasts = scan_result[0]

                # sort chromecasts by device.friendly_name
                self._chromecasts = sorted(chromecasts, key=lambda x: x.cast_info.friendly_name)
            self.scan_in_background()

        except Exception as e:
            self.refresh_chromecasts()

    def save_chromecasts(self, cache_file):
        # if directory containing cache_file does not exist, create it
        cache_dir = os.path.dirname(cache_file)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        with open(cache_file, "w") as f:
            json.dump(self.state, f)

    def refresh_chromecasts(self):
        updated = self.scan_chromecasts()
        if updated:
            self.save_chromecasts(self.cache_file)
            return True

    def scan_in_background(self):
        thread = threading.Thread(target=self.refresh_chromecasts)
        thread.start()

    @property
    def names(self):
        return [ c.cast_info.friendly_name for c in self._chromecasts ]

    @property
    def uuids(self):
        return [ str(c.uuid) for c in self._chromecasts ]

    @property
    def hosts(self):
        return [ c.cast_info.host for c in self._chromecasts ]

    @property
    def state(self):
        return {
            'uuids': self.uuids,
            'hosts': self.hosts
        }

    @property
    def chromecasts(self):
        return [ c for c in self._chromecasts if c.cast_type in ["audio", "cast"] ]
    
    @property
    def groups(self):
        return [ c for c in self._chromecasts if c.cast_type == "group" ]
