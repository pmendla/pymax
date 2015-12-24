#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import socket
from argparse import ArgumentParser

import sys

from pymax.cube import Discovery, Cube
from pymax.response import device_type_name

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('-v', '--verbose', action="count", default=1)
	parser.add_argument('-s', '--serial', help='Query cube with serial')

	args = parser.parse_args()

	logging.basicConfig(level=logging.FATAL - (10 * args.verbose), format='%(asctime)s %(levelname)-7s %(message)s')

	serial = args.serial

	if not serial:
		response = Discovery().discover()
		if response:
			serial = response.serial
		else:
			print("No cubes found.")
			sys.exit(1)

	try:
		net_cfg_response = Discovery().discover(cube_serial=serial, discovery_type=Discovery.DISCOVERY_TYPE_NETWORK_CONFIG)
		print("Discovered cube: %s" % net_cfg_response)
	except socket.timeout as st:
		print("Could not find cube '%s': %s" % (serial, st))
		sys.exit(1)

	with Cube(net_cfg_response) as cube:
		print("")
		print(cube.info)

		print("")
		print("Rooms:")
		for room in cube.rooms:
			print("  %s (ID: %s, RF address: %s):" % (room.name, room.room_id, room.rf_address))
			for device in room.devices:
				print("  - %s (%s), serial: %s, RF address: %s" % (device.name, device_type_name(device.type), device.serial, device.rf_address))
