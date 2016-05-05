#!/usr/bin/env bash

(easy_install pip || (echo "Installing pip failed" && exit 1)) && pip install geopy && pip install -U googlemaps && open https://github.com/googlemaps/google-maps-services-python
