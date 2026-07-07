# Local Monitoring Stack

This directory contains a complete local monitoring stack for the System Health Check API using Docker Compose, Prometheus, and Grafana.

## Start Monitoring

From the `monitoring/` directory:

```bash
docker compose up -d
```

Start the application separately so Prometheus can scrape it:

```bash
make run
```

## Open Grafana

- Grafana: http://localhost:3000
- Default credentials: `admin` / `admin`

The dashboard is provisioned automatically from:

- `grafana/dashboards/system-health-dashboard.json`

## Open Prometheus

- Prometheus: http://localhost:9090

## Generate Traffic

```bash
for i in {1..100}; do
curl -s http://localhost:8080/health-check \
-H "Content-Type: application/json" \
-d @../examples/sample_request.json >/dev/null
done
```

## Verify Prometheus

In Prometheus, query metrics such as:

- `api_requests_total`
- `health_checks_total`
- `api_request_duration_seconds`
- `health_check_duration_seconds`
- `healthy_components`
- `unhealthy_components`

## Verify Grafana

Open the **System Health Dashboard** and confirm the following panels populate after traffic is generated:

- API Request Rate
- Total API Requests
- Average API Latency
- API P95 Latency
- Health Check Duration
- Total Health Checks
- Healthy Components
- Unhealthy Components
- Current Dependency Failures
- Current Error Ratio

## Linux Host Access Note

Prometheus scrapes `http://host.docker.internal:8080/metrics`. The compose file maps `host.docker.internal` to the host gateway for Docker on Linux.

If your Docker setup does not support `host-gateway`, use one of the following options:

- replace the target with your host IP address, or
- run Prometheus with host networking and change the target to `localhost:8080`

## Files

- `docker-compose.yml` - local monitoring stack
- `prometheus.yml` - Prometheus scrape configuration
- `grafana/provisioning/datasources/datasource.yml` - Prometheus datasource provisioning
- `grafana/provisioning/dashboards/dashboard.yml` - dashboard provisioning
- `grafana/dashboards/system-health-dashboard.json` - provisioned dashboard
