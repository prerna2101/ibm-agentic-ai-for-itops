#!/usr/bin/env bash
# set -x
set -e

# orchestrate env activate local
# SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure schemas folder is copied to tools directory so tools can reference it
# cp -r ${SCRIPT_DIR}/tools/

for python_tool in summarize_apar_and_create_snow_incident_tool.py ansible_fix_tool.py; do
  orchestrate tools import -k python -f ${SCRIPT_DIR}/tools/${python_tool} -r ${SCRIPT_DIR}/tools/requirements.txt -p ${SCRIPT_DIR}/tools
done

# for flow_tool in corporate_action_flow.py; do
#   orchestrate tools import -k flow -f ${SCRIPT_DIR}/tools/${flow_tool}
# done

# import hello message agent
for agent in itops_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done
