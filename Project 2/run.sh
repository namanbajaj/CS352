#!/usr/bin/env fish

set ts1ListenPort 1103
set ts2ListenPort 1104
set lsListenPort 1105
set ts1Hostname localhost
set ts2Hostname localhost
set lsHostname localhost

fish -c "python ts1.py $ts1ListenPort" &
sleep 3
fish -c "python ts2.py $ts2ListenPort" &
sleep 3
fish -c "python ls.py $lsListenPort $ts1Hostname $ts1ListenPort $ts2Hostname $ts2ListenPort" &
sleep 3
fish -c "python client.py $lsHostname $lsListenPort" &