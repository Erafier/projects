#     Copyright 2020 getcarrier.io
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
from copy import deepcopy

from requests import post

from tools import VaultClient


def set_grafana_datasources(project_id: int):
    DATASOURCE = {
        "name": "",
        "type": "influxdb",
        "typeLogoUrl": "public/app/plugins/datasource/influxdb/img/influxdb_logo.svg",
        "access": "proxy",
        "url": "http://carrier-influx:8086",
        "password": "",
        "user": "",
        "database": "",
        "jsonData": {"keepCookies": []},
    }
    vault_client = VaultClient.from_project(project_id)
    secrets = vault_client.get_secrets()
    hidden_secrets = vault_client.get_hidden_secrets()
    influx_user = secrets.get("influx_user") if "influx_user" in secrets else hidden_secrets.get("influx_user", "")
    influx_password = secrets.get("influx_password") if "influx_password" in secrets else \
        hidden_secrets.get("influx_password", "")
    grafana_api_key = secrets.get("gf_api_key") if "gf_api_key" in secrets else hidden_secrets.get("gf_api_key", "")
    url = "http://carrier-grafana:3000/grafana/api/datasources"
    headers = {
        "Authorization": f"Bearer {grafana_api_key}",
        "Content-Type": "application/json"
    }
    for each in ["jmeter", "gatling", "telegraf"]:
        data = deepcopy(DATASOURCE)
        data["name"] = f"{each}_{project_id}"
        data["database"] = f"{each}_{project_id}"
        data["user"] = influx_user
        data["password"] = influx_password

        post(url, json=data, headers=headers)
