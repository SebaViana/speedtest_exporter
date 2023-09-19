# speedtest_exporter
## Overview
The speedtest_exporter is a simple tool developed for monitoring the upload and download speed of the localhost. It exposes both results as metrics in Prometheus format over HTTP.

## Exposed port
The application exposes Prometheus metrics over HTTP, and by default, it listens on port 8085.

## Volumes
You can configure the speedtest interval by specifying the following parameter:

https://github.com/SebaViana/speedtest_exporter/blob/742898abfdc99e995aed7b87f100ff2ac4d9d02b/default.yml#L1

This parameter should be added to a mounted volume in the location /app/custom.yml.
