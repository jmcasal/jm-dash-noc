from __future__ import annotations

import json
import os
import subprocess
import threading
from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from dash_noc import __version__


PROXMOX_REFRESH_LOCK = threading.Lock()


def utc_now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    configured = os.environ.get("DASH_NOC_REPO_ROOT")
    if configured:
        return Path(configured)
    return Path(__file__).resolve().parents[2]


def preview_path() -> Path:
    configured = os.environ.get("DASH_NOC_FRONTEND_HTML")
    if configured:
        return Path(configured)
    return repo_root() / "docs" / "design" / "previews" / "tablet-noc.html"


def proxmox_current_json_path() -> Path:
    configured = os.environ.get("DASH_NOC_PROXMOX_CURRENT_JSON")
    if configured:
        return Path(configured)
    return Path("/projects/proxmox-thermals/data/current.json")


def proxmox_collect_script_path() -> Path:
    configured = os.environ.get("DASH_NOC_PROXMOX_COLLECT_SCRIPT")
    if configured:
        return Path(configured)
    return Path("/projects/proxmox-thermals/scripts/collect_once.py")


def proxmox_max_age_seconds() -> int:
    configured = os.environ.get("DASH_NOC_PROXMOX_MAX_AGE", "30")
    try:
        return max(0, int(configured))
    except ValueError:
        return 30


def parse_iso_z(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def age_seconds(sampled_at: str | None, now: datetime) -> int | None:
    if not sampled_at:
        return None
    parsed = parse_iso_z(sampled_at)
    if parsed is None:
        return None
    return max(0, int((now - parsed).total_seconds()))


def pct_state(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value >= 90:
        return "crit"
    if value >= 70:
        return "warn"
    return "ok"


def temp_state(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value >= 70:
        return "crit"
    if value >= 55:
        return "warn"
    return "ok"


def worst_status(*statuses: str) -> str:
    rank = {"ok": 0, "unknown": 1, "warn": 2, "stale": 3, "down": 4, "crit": 5}
    return max(statuses, key=lambda item: rank.get(item, 1), default="unknown")


def health_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "dash-noc",
        "version": __version__,
        "time": iso_z(utc_now()),
    }


def load_proxmox_current_json() -> dict[str, Any] | None:
    path = proxmox_current_json_path()
    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def refresh_proxmox_current_json(timeout_seconds: int = 25) -> tuple[bool, str | None]:
    script = proxmox_collect_script_path()
    if not script.exists():
        return False, "collector script not found"

    if not PROXMOX_REFRESH_LOCK.acquire(blocking=False):
        return False, "collector busy"

    try:
        env = os.environ.copy()
        env["PROXMOX_THERMALS_DATA_DIR"] = str(proxmox_current_json_path().parent)
        subprocess.run(
            ["/usr/bin/python3", str(script)],
            check=True,
            timeout=timeout_seconds,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True, None
    except subprocess.TimeoutExpired:
        return False, "collector timeout"
    except subprocess.CalledProcessError:
        return False, "collector failed"
    finally:
        PROXMOX_REFRESH_LOCK.release()


def ensure_fresh_proxmox_snapshot(now: datetime) -> tuple[dict[str, Any] | None, str | None]:
    raw = load_proxmox_current_json()
    age = age_seconds((raw or {}).get("timestamp"), now) if raw else None
    refresh_enabled = os.environ.get("DASH_NOC_PROXMOX_REFRESH", "1") != "0"
    if refresh_enabled and (age is None or age > proxmox_max_age_seconds()):
        refreshed, reason = refresh_proxmox_current_json()
        fresh_raw = load_proxmox_current_json()
        return fresh_raw or raw, None if refreshed else reason
    return raw, None


def mock_proxmox(now: datetime) -> dict[str, Any]:
    sampled_at = now - timedelta(seconds=18)
    return {
        "status": "warn",
        "source": "mock",
        "sampled_at": iso_z(sampled_at),
        "age_seconds": 18,
        "summary": {
            "cpu_used_percent": 21.0,
            "load_average": [2.3, 2.6, 2.4],
            "memory_used_percent": 77.6,
            "memory_used_bytes": 104_582_987_366,
            "memory_total_bytes": 134_861_973_094,
            "storage_used_percent": 42.1,
            "vm_count": 11,
            "lxc_count": 7,
            "max_temperature_c": 85.0,
            "max_temperature_label": "nvme1n1 sensor2",
        },
        "temperatures": [
            {
                "id": "nvme1n1",
                "label": "NVMe 2",
                "device": "/dev/nvme1n1",
                "temperature_c": 64.0,
                "sensor2_c": 85.0,
                "state": "crit",
            },
            {
                "id": "nvme0n1",
                "label": "NVMe 1",
                "device": "/dev/nvme0n1",
                "temperature_c": 47.0,
                "sensor2_c": 82.0,
                "state": "crit",
            },
            {
                "id": "sdb",
                "label": "temp-storage",
                "device": "/dev/sdb",
                "temperature_c": 26.0,
                "sensor2_c": None,
                "state": "ok",
            },
        ],
        "storage": [
            {
                "id": "root",
                "label": "root fs",
                "used_bytes": 8_589_934_592,
                "total_bytes": 100_824_612_454,
                "used_percent": 10.0,
                "mountpoint": "/",
                "state": "ok",
            },
            {
                "id": "local-lvm",
                "label": "local-lvm",
                "used_bytes": 2_170_224_676_454,
                "total_bytes": 3_932_763_881_472,
                "used_percent": 55.2,
                "mountpoint": None,
                "state": "ok",
            },
        ],
        "vms": [],
        "lxc": [],
    }


def proxmox_from_current_json(now: datetime) -> dict[str, Any] | None:
    raw, refresh_warning = ensure_fresh_proxmox_snapshot(now)
    if raw is None:
        return None

    sampled_at = raw.get("timestamp")
    age = age_seconds(sampled_at, now)
    memory = raw.get("memory") or {}
    cpu = raw.get("cpu") or {}
    load = raw.get("load") or {}
    storages = raw.get("storages") or {}
    disks = raw.get("disks") or {}
    filesystems = raw.get("filesystems") or {}
    temperatures_raw = raw.get("temperatures") or {}

    temperature_items: list[dict[str, Any]] = []
    max_temperature_c: float | None = None
    max_temperature_label: str | None = None

    for key, value in sorted(temperatures_raw.items()):
        if not isinstance(value, (int, float)):
            continue
        label = key.removesuffix("_c").replace("_", " ")
        temperature_items.append(
            {
                "id": key,
                "label": label,
                "device": None,
                "temperature_c": float(value),
                "sensor2_c": None,
                "state": temp_state(float(value)),
            }
        )
        if max_temperature_c is None or float(value) > max_temperature_c:
            max_temperature_c = float(value)
            max_temperature_label = label

    for serial, disk in sorted(disks.items()):
        temp = disk.get("temperature_c")
        sensor2 = disk.get("sensor2_c")
        effective = sensor2 if isinstance(sensor2, (int, float)) else temp
        disk_used_percent = None
        for mountpoint in disk.get("mountpoints") or []:
            fs = filesystems.get(mountpoint)
            if fs and isinstance(fs.get("used_percent"), (int, float)):
                candidate = float(fs["used_percent"])
                disk_used_percent = candidate if disk_used_percent is None else max(disk_used_percent, candidate)
        item = {
            "id": disk.get("linux_name") or serial,
            "label": disk.get("role") or disk.get("linux_name") or serial,
            "device": disk.get("device"),
            "temperature_c": temp,
            "sensor2_c": sensor2,
            "used_percent": disk_used_percent,
            "mountpoints": disk.get("mountpoints") or [],
            "model": disk.get("model"),
            "serial": serial,
            "state": temp_state(effective),
        }
        temperature_items.append(item)
        if isinstance(effective, (int, float)):
            value = float(effective)
            if max_temperature_c is None or value > max_temperature_c:
                max_temperature_c = value
                max_temperature_label = f"{item['id']} sensor2" if sensor2 is not None else item["id"]

    storage_items = []
    for storage_id, storage in sorted(storages.items()):
        used_percent = storage.get("used_percent")
        storage_items.append(
            {
                "id": storage_id,
                "label": storage_id,
                "used_bytes": storage.get("used_bytes"),
                "total_bytes": storage.get("total_bytes"),
                "used_percent": used_percent,
                "mountpoint": None,
                "state": pct_state(used_percent),
            }
        )

    temp_status = worst_status(*(item["state"] for item in temperature_items))
    memory_status = pct_state(memory.get("used_percent"))
    storage_status = worst_status(*(item["state"] for item in storage_items))
    status = worst_status(temp_status, memory_status, storage_status)
    if age is None or age > 300:
        status = "stale"

    payload = {
        "status": status,
        "source": "proxmox-thermals-file",
        "sampled_at": sampled_at,
        "age_seconds": age,
        "summary": {
            "cpu_used_percent": cpu.get("used_percent"),
            "load_average": [load.get("1m"), load.get("5m"), load.get("15m")],
            "memory_used_percent": memory.get("used_percent"),
            "memory_used_bytes": memory.get("used_bytes"),
            "memory_total_bytes": memory.get("total_bytes"),
            "storage_used_percent": max((s.get("used_percent") or 0 for s in storage_items), default=None),
            "vm_count": len(raw.get("vms_running") or []),
            "lxc_count": None,
            "max_temperature_c": max_temperature_c,
            "max_temperature_label": max_temperature_label,
        },
        "temperatures": temperature_items,
        "storage": storage_items,
        "vms": raw.get("vms_running") or [],
        "lxc": [],
    }
    if refresh_warning:
        payload["refresh_warning"] = refresh_warning
    return payload


def proxmox_payload(now: datetime) -> dict[str, Any]:
    return proxmox_from_current_json(now) or mock_proxmox(now)


def mock_jm22w11(now: datetime) -> dict[str, Any]:
    sampled_at = now - timedelta(seconds=5)
    return {
        "status": "ok",
        "source": "mock",
        "sampled_at": iso_z(sampled_at),
        "age_seconds": 5,
        "hostname": "JM22W11",
        "os": {
            "name": "Windows",
            "version": "unknown",
        },
        "uptime_seconds": 386_760,
        "cpu_used_percent": 18.0,
        "memory_used_percent": 51.0,
        "memory_used_bytes": 17_501_991_731,
        "memory_total_bytes": 34_359_738_368,
        "disks": [
            {
                "id": "system",
                "label": "System",
                "mountpoint": "C:",
                "used_bytes": 676_457_349_120,
                "total_bytes": 1_073_741_824_000,
                "used_percent": 63.0,
                "state": "ok",
            }
        ],
        "network": {
            "status": "ok",
            "primary_ipv4": "192.168.1.50",
        },
        "battery": {
            "present": False,
        },
    }


def mock_notifications(now: datetime) -> dict[str, Any]:
    sampled_at = now - timedelta(seconds=5)
    return {
        "status": "ok",
        "source": "mock",
        "sampled_at": iso_z(sampled_at),
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
                "read": False,
                "tags": ["backup", "important"],
            },
            {
                "id": "mail-20260528-0718-storage-warning",
                "severity": "warn",
                "source": "mail",
                "title": "Storage warning from homelab",
                "summary": "Storage warning message matched alert filters",
                "received_at": "2026-05-28T05:18:00Z",
                "read": False,
                "tags": ["storage", "important"],
            },
        ],
    }


def mock_alerts() -> list[dict[str, Any]]:
    return [
        {
            "id": "proxmox-nvme1n1-sensor2-hot",
            "severity": "crit",
            "source": "proxmox",
            "title": "NVMe temperature critical",
            "summary": "nvme1n1 sensor2 at 85.0 C for more than 5 minutes",
            "created_at": "2026-05-28T17:16:00Z",
            "state": "open",
        },
        {
            "id": "proxmox-memory-high",
            "severity": "warn",
            "source": "proxmox",
            "title": "Memory usage above threshold",
            "summary": "Proxmox RAM above 75 percent",
            "created_at": "2026-05-28T15:30:00Z",
            "state": "open",
        },
    ]


def noc_current_payload() -> dict[str, Any]:
    now = utc_now()
    proxmox = proxmox_payload(now)
    jm22w11 = mock_jm22w11(now)
    notifications = mock_notifications(now)
    alerts = mock_alerts()
    source_modes = {proxmox.get("source"), jm22w11.get("source"), notifications.get("source")}
    return {
        "schema_version": 1,
        "generated_at": iso_z(now),
        "mode": "mock" if source_modes == {"mock"} else "mixed",
        "overall": {
            "status": worst_status(proxmox["status"], jm22w11["status"], "warn" if alerts else "ok"),
            "active_alerts": len(alerts),
            "important_notifications": notifications["unread_count"],
            "stale_sources": ["proxmox"] if proxmox["status"] == "stale" else [],
        },
        "clock": {
            "timezone": "Europe/Madrid",
        },
        "proxmox": proxmox,
        "jm22w11": jm22w11,
        "alerts": alerts,
        "notifications": notifications["items"],
    }


class DashNocHandler(BaseHTTPRequestHandler):
    server_version = f"dash-noc/{__version__}"

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html", "/tablet-noc.html"}:
            self.serve_frontend(send_body=False)
            return
        if parsed.path == "/health":
            self.send_json(health_payload(), send_body=False)
            return
        self.send_error_json(HTTPStatus.NOT_FOUND, "not found", send_body=False)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path in {"/", "/index.html", "/tablet-noc.html"}:
            self.serve_frontend()
            return

        if path == "/health":
            self.send_json(health_payload())
            return

        if path == "/api/noc/current":
            self.send_json(noc_current_payload())
            return

        if path == "/api/proxmox/status":
            self.send_json(proxmox_payload(utc_now()))
            return

        if path == "/api/jm22w11/status":
            self.send_json(mock_jm22w11(utc_now()))
            return

        if path == "/api/notifications/important":
            self.send_json(mock_notifications(utc_now()))
            return

        self.send_error_json(HTTPStatus.NOT_FOUND, "not found")

    def log_message(self, format: str, *args: Any) -> None:
        return

    def send_json(
        self,
        payload: Any,
        status: HTTPStatus = HTTPStatus.OK,
        send_body: bool = True,
    ) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def send_error_json(
        self,
        status: HTTPStatus,
        message: str,
        send_body: bool = True,
    ) -> None:
        self.send_json({"error": message, "status": status.value}, status=status, send_body=send_body)

    def serve_frontend(self, send_body: bool = True) -> None:
        path = preview_path()
        if not path.exists():
            self.send_error_json(HTTPStatus.NOT_FOUND, "frontend not found")
            return
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)


def main() -> int:
    host = os.environ.get("DASH_NOC_BIND", "127.0.0.1")
    port = int(os.environ.get("DASH_NOC_PORT", "8124"))
    server = ThreadingHTTPServer((host, port), DashNocHandler)
    print(f"dash-noc api listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
