#
# Copyright IBM Corp. 2016 All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests
from behave import *
from peer_basic_impl import buildUrl, getAttributeFromJSON
from bdd_test_util import bdd_log


@when(u'I request transaction certs with query parameters on "{containerAlias}"')
def step_impl(context, containerAlias):
    assert 'table' in context, "table (of query parameters) not found in context"
    assert 'userName' in context, "userName not found in context"
    assert 'compose_containers' in context, "compose_containers not found in context"

    ipAddress = context.containerAliasMap[containerAlias].ipAddress
    request_url = buildUrl(context, ipAddress, "/registrar/{0}/tcert".format(context.userName))
    bdd_log("Requesting path = {0}".format(request_url))
    queryParams = {}
    for row in context.table.rows:
        key, value = row['key'], row['value']
        queryParams[key] = value

    bdd_log("Query parameters = {0}".format(queryParams))
    resp = requests.get(request_url, params=queryParams, headers={'Accept': 'application/json'}, verify=False)

    assert resp.status_code == 200, "Failed to GET to %s:  %s" % (request_url, resp.text)
    context.response = resp
    bdd_log("")

@then(u'I should get a JSON response with "{expectedValue}" different transaction certs')
def step_impl(context, expectedValue):
    bdd_log(context.response.json())
    foundValue = getAttributeFromJSON("OK", context.response.json(), "Attribute not found in response (OK)")
    bdd_log(len(set(foundValue)))
    assert (len(set(foundValue)) == int(expectedValue)), "For attribute OK, expected different transaction cert of size (%s), instead found (%s)" % (expectedValue, len(set(foundValue)))