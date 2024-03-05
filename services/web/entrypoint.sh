#!/bin/sh

# Runs database migrations on deployment, ensuring the database
# remains in sync with the code.
flask db upgrade

exec "$@"