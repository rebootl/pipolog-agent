# pipolog-agent

Fully asynchronous agent for pipolog. Installed on clients.

Currently this supports pipes as inputs and sends the data to
the pipolog server via http(s).

## Setup

create virtual env.:

    $ python3 -m venv myvenv

    $ source myvenv/bin/activate

    $ pip install aiofiles
    $ pip install aiohttp[speedups]

create pipe(s) for output:

    $ mkfifo syslog
    $ chmod 666 syslog # if needed
    $ mkfifo foo

## Configure rsyslog to output to pipe

`/etc/rsyslog.conf`

    # pipe
    Module (load="builtin:ompipe")
    *.* action(type="ompipe" Pipe="/home/cem/pipolog-agent/syslog")

## Output to multiple files/pipes

Example:

    backup.sh 2>&1 | tee ./backup.log ../pipolog-agent/backup-fifo > /dev/null

## Systemd service

Install service file: `pipolog-agent.service`

Copy to `/etc/systemd/system/`.
