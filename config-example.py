#

API_KEY = 'somesecretapikeyblablba'
API_URL_LOG = 'http://localhost:8888/api/logdata/agent'
API_URL_METRICS = 'http://localhost:8888/api/metrics/agent'

# sha256sum of DER cert. or False
SSL_FINGERPRINT = '...'

IN_PIPES_DEF = [
    { 'name': 'backup', 'path': './backup'},
    { 'name': 'syslog', 'path': './syslog' },
]
