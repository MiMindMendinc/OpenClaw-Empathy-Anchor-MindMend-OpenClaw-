#!/usr/bin/env python3
"""Live API walkthrough for MindMend Empathy Anchor. Start the server first: make demo"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8000')


def request(method: str, path: str, body: dict | None = None, token: str | None = None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f'{BASE_URL}{path}', data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.load(resp)


def main() -> int:
    print(f'MindMend Empathy Anchor API demo against {BASE_URL}')
    try:
        status, health = request('GET', '/api/v1/health')
    except urllib.error.URLError as exc:
        print(f'Could not reach {BASE_URL}: {exc}')
        print('Start the server with: make demo')
        return 1
    print('health', status, health.get('service'), health.get('status'))

    _, ready = request('GET', '/api/v1/ready')
    print('ready', ready.get('status'))

    _, login = request('POST', '/api/v1/auth/login', {'user_id': 'demo_user'})
    token = login['token']
    print('login demo_auth', login.get('demo_auth'))

    _, scan = request(
        'POST',
        '/api/v1/scan',
        {'message': 'I feel anxious and overwhelmed'},
        token=token,
    )
    summary = scan['data']['summary']
    print('scan severity', summary['severity'], 'alert', summary['alert_persisted'])

    _, resources = request('GET', '/api/v1/resources')
    print('988', resources['crisis_resources']['988'])
    print('crisis text', resources['crisis_resources']['crisis_text'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
