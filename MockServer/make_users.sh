#!/usr/bin/env bash
# make_users.sh - create MQTT broker users from the credentials in .env.
# Run:  bash make_users.sh
# Produces a 'passwd' file referenced by mosquitto.conf.
#
# Reads SENSOR_* and TWIN_* values from .env (same source as the Python clients),
# so credentials live in exactly one place and are never hard-coded.

set -e

# Load .env if present
if [ ! -f .env ]; then
  echo "ERROR: .env not found. Copy .env.example to .env and fill in your values:"
  echo "   cp .env.example .env"
  exit 1
fi

# Export all variables defined in .env into this shell
set -a
# shellcheck disable=SC1091
source .env
set +a

# Basic validation
if [ -z "$SENSOR_USERNAME" ] || [ -z "$SENSOR_PASSWORD" ] || [ -z "$TWIN_USERNAME" ] || [ -z "$TWIN_PASSWORD" ]; then
  echo "ERROR: one or more credentials are empty in .env"
  echo "   Required: SENSOR_USERNAME, SENSOR_PASSWORD, TWIN_USERNAME, TWIN_PASSWORD"
  exit 1
fi

# -c creates a NEW password file (first user); without -c it appends.
echo "==> Creating broker user '$SENSOR_USERNAME' (publisher)"
mosquitto_passwd -c -b passwd "$SENSOR_USERNAME" "$SENSOR_PASSWORD"

echo "==> Adding broker user '$TWIN_USERNAME' (subscriber)"
mosquitto_passwd -b passwd "$TWIN_USERNAME" "$TWIN_PASSWORD"

echo ""
echo "Done. 'passwd' file created with users: $SENSOR_USERNAME, $TWIN_USERNAME"
echo "(passwd is git-ignored - it stays on this machine only.)"
