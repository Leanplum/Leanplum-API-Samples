#!/usr/bin/env python
# NOTE: Requires Python 2.7.10 or higher to support SSL.

"""Displays the number of sends, opens, and open rate as CSV for your push notifications.

The results are displayed as CSV for the past week. You can change the date range by customizing
START_DATE and END_DATE.
"""

import datetime
import json
import sys
import time
import urllib2


APP_ID = 'YOUR_APP_ID'
CONTENT_KEY = 'YOUR_CONTENT_READONLY_KEY'
EXPORT_KEY = 'YOUR_EXPORT_KEY'


# This is set to the last week. You can customize the dates, or provide specific dates like this:
# datetime.date(2015, 11, 10)
END_DATE = datetime.date.today()
START_DATE = END_DATE - datetime.timedelta(days=7)


API_ENDPOINT = 'https://www.leanplum.com/api'


def call_leanplum_api(action, client_key, request_json=None):
  """Makes a call to the Leanplum API."""

  print 'Making Leanplum API call to %s...' % action

  if request_json is None:
    request_json = {}

  request_json.update({
    'action': action,
    'appId': APP_ID,
    'clientKey': client_key,
    'apiVersion': '1.0.6',
  })

  request = urllib2.Request(API_ENDPOINT, json.dumps(request_json))
  try:
    response = urllib2.urlopen(request)
  except urllib2.HTTPError, e:
    response = e
  response = json.loads(response.read())['response'][0]
  if not response['success']:
    print 'Error: %s' % response['error']['message']
    sys.exit(1)
  return response


def get_message_stats():
  """Returns a two-dimensional array containing the message stats."""

  # Get messages.
  messages = call_leanplum_api('getMessages', CONTENT_KEY)['messages']
  pushes = filter(lambda message: message['messageType'] == 'Push Notification', messages)

  # Format message events.
  # Message event names are encoded like this:
  # ".mMESSAGE_ID" for send, ".mMESSAGE_ID Open" for open.
  # E.g. .m1234, .m1234 Open
  event_names = []
  for message in pushes:
    message['sendEvent'] = '.m%d' % message['id']
    message['openEvent'] = '.m%d Open' % message['id']
    event_names.extend([
      message['sendEvent'],
      message['openEvent']
    ])

  # Export report.
  job_id = call_leanplum_api('exportReport', EXPORT_KEY, {
    'startDate': START_DATE,
    'endDate': END_DATE,
    'dataType': 'UserActivity',
    'eventNames': event_names
  })['jobId']
  data = None
  while not data:
    results = call_leanplum_api('getExportResults', EXPORT_KEY, {
      'jobId': job_id,
    })
    if results['state']['value'] != 'RUNNING':
      data = results['data']
      break
    time.sleep(5)

  # Print CSV header.
  rows = []
  header = ['Date']
  for message in pushes:
    header.extend([
        '%s Sent' % message['name'],
        '%s Open' % message['name'],
        '%s Open Rate' % message['name'],
    ])
  rows.append(header)

  # Print CSV rows.
  for date in sorted(data.keys()):
    date_data = data.get(date)
    row = [date]
    def get_occurrences(event_name):
      return int((date_data.get(event_name, {})).get('Occurrences', 0))
    for message in pushes:
      sends = get_occurrences(message['sendEvent'])
      opens = get_occurrences(message['openEvent'])
      row.extend([str(sends), str(opens), str(100.0 * opens / sends) if sends else ''])
    rows.append(row)
  return rows


def print_csv(csv):
  """Prints a two-dimensional array as CSV."""
  print '\n'.join([','.join([cell for cell in row]) for row in csv])


if __name__ == '__main__':
  if sys.version_info < (2, 7, 10):
    print 'This script requires Python 2.7.10 or higher.'
    sys.exit(1)
  print_csv(get_message_stats())
