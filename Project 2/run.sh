#!/usr/bin/env fish

set ts1ListenPort 10004
set ts2ListenPort 10001
set lsListenPort 10002
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