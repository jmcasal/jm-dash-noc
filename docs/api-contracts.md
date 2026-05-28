# API contracts

## Principios

- Todas las fechas usan ISO 8601 en UTC con sufijo `Z`.
- Todas las muestras incluyen `sampled_at` y `age_seconds` cuando el dato viene de un collector.
- Los porcentajes usan rango `0..100`.
- Los bytes se exponen como enteros en campos `*_bytes`.
- Los grados Celsius se exponen como numeros en campos `*_c`.
- Si una fuente no existe todavia, el campo debe omitirse o tener `status: "unknown"`, no inventarse.
- La API central puede servir datos mock durante desarrollo, pero debe marcarlos con `source: "mock"`.

## `GET /health`

Comprueba que el proceso central responde.

```json
{
  "status": "ok",
  "service": "dash-noc",
  "version": "0.1.0",
  "time": "2026-05-28T17:30:00Z"
}
```

## `GET /api/noc/current`

Snapshot agregado para la pantalla principal. Es el endpoint que consumira la tablet.

```json
{
  "schema_version": 1,
  "generated_at": "2026-05-28T17:30:00Z",
  "mode": "live",
  "overall": {
    "status": "warn",
    "active_alerts": 3,
    "important_notifications": 5,
    "stale_sources": []
  },
  "clock": {
    "timezone": "Europe/Madrid"
  },
  "proxmox": {
    "status": "warn",
    "source": "proxmox-thermals",
    "sampled_at": "2026-05-28T17:29:42Z",
    "age_seconds": 18,
    "summary": {
      "cpu_used_percent": 21.0,
      "load_average": [2.3, 2.6, 2.4],
      "memory_used_percent": 77.6,
      "memory_used_bytes": 104582987366,
      "memory_total_bytes": 134861973094,
      "storage_used_percent": 42.1,
      "vm_count": 11,
      "lxc_count": 7,
      "max_temperature_c": 85.0,
      "max_temperature_label": "nvme1n1 sensor2"
    },
    "temperatures": [
      {
        "id": "nvme1n1",
        "label": "NVMe 2",
        "device": "/dev/nvme1n1",
        "temperature_c": 64.0,
        "sensor2_c": 85.0,
        "state": "crit"
      }
    ],
    "storage": [
      {
        "id": "root",
        "label": "root fs",
        "used_bytes": 8589934592,
        "total_bytes": 100824612454,
        "used_percent": 10.0,
        "mountpoint": "/",
        "state": "ok"
      }
    ]
  },
  "jm22w11": {
    "status": "ok",
    "source": "jm22w11-status-agent",
    "sampled_at": "2026-05-28T17:29:55Z",
    "age_seconds": 5,
    "hostname": "JM22W11",
    "os": {
      "name": "Windows",
      "version": "unknown"
    },
    "uptime_seconds": 386760,
    "cpu_used_percent": 18.0,
    "memory_used_percent": 51.0,
    "memory_used_bytes": 17501991731,
    "memory_total_bytes": 34359738368,
    "disks": [
      {
        "id": "system",
        "label": "System",
        "mountpoint": "C:",
        "used_bytes": 676457349120,
        "total_bytes": 1073741824000,
        "used_percent": 63.0,
        "state": "ok"
      }
    ],
    "network": {
      "status": "ok",
      "primary_ipv4": "192.168.1.50"
    },
    "battery": {
      "present": false
    }
  },
  "alerts": [
    {
      "id": "proxmox-nvme1n1-sensor2-hot",
      "severity": "crit",
      "source": "proxmox",
      "title": "NVMe temperature critical",
      "summary": "nvme1n1 sensor2 at 85.0 C for more than 5 minutes",
      "created_at": "2026-05-28T17:16:00Z",
      "state": "open"
    }
  ],
  "notifications": [
    {
      "id": "mail-20260528-0842-backup-report",
      "severity": "crit",
      "source": "mail",
      "title": "Backup report requires attention",
      "summary": "Important backup monitor message matched alert filters",
      "received_at": "2026-05-28T06:42:00Z",
      "read": false
    }
  ]
}
```

### Status values

- `ok`: source is reachable and values are inside expected range.
- `warn`: source is reachable but one or more values need attention.
- `crit`: source is reachable and at least one value is critical.
- `unknown`: source has no data yet.
- `stale`: source has data, but the sample is older than the accepted age.
- `down`: source cannot be reached.

### Severity values

- `info`
- `warn`
- `crit`

## `GET /api/proxmox/status`

Proxmox-only projection used by `/api/noc/current`. It should be derivable from the same local collector data used by `proxmox-thermals`.

Required top-level fields:

```json
{
  "status": "warn",
  "source": "proxmox-thermals",
  "sampled_at": "2026-05-28T17:29:42Z",
  "age_seconds": 18,
  "summary": {},
  "temperatures": [],
  "storage": [],
  "vms": [],
  "lxc": []
}
```

`vms` and `lxc` can start empty until the Proxmox collector exposes reliable data.

## `GET /api/jm22w11/status`

Proxy/cache of the workstation status agent.

```json
{
  "status": "ok",
  "source": "jm22w11-status-agent",
  "sampled_at": "2026-05-28T17:29:55Z",
  "age_seconds": 5,
  "hostname": "JM22W11",
  "os": {
    "name": "Windows",
    "version": "unknown"
  },
  "uptime_seconds": 386760,
  "cpu_used_percent": 18.0,
  "memory_used_percent": 51.0,
  "memory_used_bytes": 17501991731,
  "memory_total_bytes": 34359738368,
  "disks": [],
  "network": {
    "status": "ok",
    "primary_ipv4": "192.168.1.50"
  },
  "battery": {
    "present": false
  }
}
```

## `GET /api/notifications/important`

Proxy/cache of filtered notifications from `JM22W11`.

```json
{
  "status": "ok",
  "source": "jm22w11-notifications-agent",
  "sampled_at": "2026-05-28T17:29:55Z",
  "age_seconds": 5,
  "unread_count": 5,
  "items": [
    {
      "id": "mail-20260528-0842-backup-report",
      "severity": "crit",
      "source": "mail",
      "title": "Backup report requires attention",
      "summary": "Important backup monitor message matched alert filters",
      "received_at": "2026-05-28T06:42:00Z",
      "read": false,
      "tags": ["backup", "important"]
    }
  ]
}
```

The notification agent is responsible for filtering noise before data reaches Proxmox.
