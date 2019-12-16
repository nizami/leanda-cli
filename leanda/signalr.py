from signalrcore.hub_connection_builder import HubConnectionBuilder


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


server_url = 'ws://localhost/core-api/v1/signalr'
token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGSjg2R2NGM2pUYk5MT2NvNE52WmtVQ0lVbWZZQ3FvcXRPUWVNZmJoTmxFIn0.eyJqdGkiOiJiYzcwOWFlNi1kMjlmLTQ1NmUtOTkwOC1hY2U2OWU1M2FjZjciLCJleHAiOjE1NzY1MTMzMjYsIm5iZiI6MCwiaWF0IjoxNTc2NTEyNDI2LCJpc3MiOiJodHRwczovL2lkLmxlYW5kYS5pby9hdXRoL3JlYWxtcy9PU0RSIiwiYXVkIjoibGVhbmRhX2FuZ3VsYXIiLCJzdWIiOiIyZmZiZDJiMC04Y2VlLTQzYWItYmI3Ni03MTc5ZmFmMTY0ZTAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJsZWFuZGFfYW5ndWxhciIsIm5vbmNlIjoiMzNhOTljNGQzYTQzNDZlNGI5ZDVkM2ZmMWY0MTIxODQiLCJhdXRoX3RpbWUiOjE1NzY1MDk5MDAsInNlc3Npb25fc3RhdGUiOiJkMmIwOTQ4NC0zZDQ5LTRlOTUtOTI1Yy1jYjY0Njk3M2NkZTMiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVzb3VyY2VfYWNjZXNzIjp7fSwibmFtZSI6Ik5pemFtaSBBbWlyb3YiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJuaXphbWkiLCJnaXZlbl9uYW1lIjoiTml6YW1pIiwiZmFtaWx5X25hbWUiOiJBbWlyb3YiLCJlbWFpbCI6Im5pemFtaS5kZXZAZ21haWwuY29tIn0.gEVUj1_7qKpT_6mniGVTVwj_74K55pNYFkusjgEDwwDBFuSu7DtzEhAp-KVtk66mFv_KwhdbjiGPAgsVqVEFDFc7wmeDtG7jWprin1mjyH54CQ4phrFsiHaze3Ja0jPM440xXqJqSdwNQANvzVyQBHnmbNfD9mF2zC8U4HNiZKE'
hub_connection = HubConnectionBuilder()\
            .with_url(server_url,
            options={
                "access_token_factory": lambda: token,
            })\
            .build()

hub_connection.on('organizeUpdate', print)
hub_connection.on('updateNotficationBar', print)
hub_connection.start()

message = ''
while message != "exit()":
    message = input(">> ")
hub_connection.stop()