#!/bin/bash
# report as a puppet fact why and when puppet was locked, if it was

###############################################################################
### Configuration #############################################################
###############################################################################

if test -f /opt/ssi/etc/puppetreport; then
    . /opt/ssi/etc/puppetreport
fi

SUMMARY_FILE=${PUPPET_SUMMARY_FILE:-/opt/puppetlabs/puppet/public/last_run_summaary.yaml}
AGENT_LOCK=${PUPPET_LOCK_FILE:-/opt/puppetlabs/puppet/cache/state/agent_disabled.lock}

###############################################################################
### main () ###################################################################
###############################################################################

if [[ -f $AGENT_LOCK ]] ; then
    AGE=$(stat -c %Y "${SUMMARY_FILE}")
    AGE_HUMAN=$(date --iso-8601=seconds -d @"${AGE}")
    # shellcheck disable=SC2002
    MSG=$(cat "${AGENT_LOCK}" | jq .disabled_message | sed -e s/\"//g)
    echo "puppetlock_text: \"${MSG}\""
    echo "puppetlock_age: \"${AGE_HUMAN}\""
fi
