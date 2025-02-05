#!/usr/bin/env bash

log="config/log/log_$(date '+%Y-%m-%d').txt"
tail -f $log  | grep -i "Extracting URL\|Downloading item\|upload date\|Video unavailable\|Finished downloading playlist\|Sign in to confirm you’re not a bot\|Downloading webpage\|Downloading playlist"
