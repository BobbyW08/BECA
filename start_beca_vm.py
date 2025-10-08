#!/usr/bin/env python3
"""
Automate starting the BECA Compute Engine instance with GPU zone fallback.

The script first attempts to start the existing instance in the zone where it
currently lives. If the zone is out of GPU capacity, it removes the terminated
instance and recreates it from the configured snapshot in the first zone that
accepts the request.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional


class GCloudError(RuntimeError):
    """Raised when a gcloud command fails for an unexpected reason."""


@dataclass
class InstanceInfo:
    name: str
    zone: str
    status: str


GCLOUD_BIN = shutil.which("gcloud") or shutil.which("gcloud.cmd") or shutil.which("gcloud.exe")


def run_gcloud(args: List[str], *, quiet: bool = False) -> subprocess.CompletedProcess[str]:
    """Run a gcloud command and capture stdout/stderr."""
    if GCLOUD_BIN is None:
        raise GCloudError(
            "gcloud CLI not found in PATH. Install Google Cloud SDK or add it to PATH."
        )

    command = [GCLOUD_BIN, *args]
    if not quiet:
        print(f"$ {' '.join(command)}")

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    return result


def get_instance(project: str, instance: str) -> Optional[InstanceInfo]:
    """Return instance metadata if it exists, otherwise None."""
    result = run_gcloud(
        [
            "compute",
            "instances",
            "list",
            f"--project={project}",
            f"--filter=name={instance}",
            "--format=json",
        ],
        quiet=True,
    )

    if result.returncode != 0:
        raise GCloudError(
            f"Failed to query instance list: {result.stderr.strip() or result.stdout.strip()}"
        )

    if not result.stdout.strip():
        return None

    instances = json.loads(result.stdout)
    if not instances:
        return None

    entry = instances[0]
    return InstanceInfo(
        name=entry["name"],
        zone=entry["zone"].split("/")[-1],
        status=entry["status"],
    )


def contains_capacity_error(output: str) -> bool:
    """Identify the 'zone resource pool exhausted' message."""
    return "ZONE_RESOURCE_POOL_EXHAUSTED" in output or "stockout" in output.lower()


def start_existing_instance(project: str, instance: InstanceInfo) -> bool:
    """Try to start the existing instance. Return True if it is now running."""
    print(f"Attempting to start {instance.name} in {instance.zone} (current status: {instance.status})")
    result = run_gcloud(
        [
            "compute",
            "instances",
            "start",
            instance.name,
            f"--zone={instance.zone}",
            f"--project={project}",
        ]
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if result.returncode == 0:
        if stdout:
            print(stdout)
        print(f"Instance {instance.name} is running in {instance.zone}.")
        return True

    combined = "\n".join(filter(None, [stdout, stderr]))
    if contains_capacity_error(combined):
        print(f"Zone {instance.zone} is out of GPU capacity; will recreate in another zone.")
        delete_instance(project, instance.name, instance.zone)
        return False

    raise GCloudError(f"Failed to start instance:\n{combined}")


def delete_instance(project: str, instance: str, zone: str) -> None:
    """Delete the specified instance."""
    print(f"Deleting {instance} from {zone}...")
    result = run_gcloud(
        [
            "compute",
            "instances",
            "delete",
            instance,
            f"--zone={zone}",
            f"--project={project}",
            "--quiet",
        ]
    )

    if result.returncode != 0:
        combined = "\n".join(filter(None, [result.stdout.strip(), result.stderr.strip()]))
        raise GCloudError(f"Failed to delete instance {instance}: {combined}")

    print(f"Deleted {instance} from {zone}.")


def create_instance(
    project: str,
    instance: str,
    zone: str,
    *,
    machine_type: str,
    accelerator: str,
    scopes: str,
    tags: str,
    boot_disk_type: str,
    boot_disk_size: int,
    snapshot: str,
    preemptible: bool,
) -> bool:
    """Attempt to create the instance in the given zone. Return True on success."""
    print(f"Creating {instance} in {zone}...")
    args = [
        "compute",
        "instances",
        "create",
        instance,
        f"--zone={zone}",
        f"--project={project}",
        f"--machine-type={machine_type}",
        f"--accelerator={accelerator}",
        "--maintenance-policy=TERMINATE",
        f"--scopes={scopes}",
        f"--tags={tags}",
        f"--boot-disk-type={boot_disk_type}",
        f"--boot-disk-size={boot_disk_size}",
        f"--source-snapshot={snapshot}",
    ]

    if preemptible:
        args.append("--preemptible")

    result = run_gcloud(args)
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if result.returncode == 0:
        if stdout:
            print(stdout)
        print(f"Instance {instance} created successfully in {zone}.")
        return True

    combined = "\n".join(filter(None, [stdout, stderr]))
    if contains_capacity_error(combined):
        print(f"Zone {zone} is out of GPU capacity. Trying next zone...")
        return False

    raise GCloudError(f"Failed to create instance in {zone}:\n{combined}")


def ensure_instance_running(args: argparse.Namespace) -> None:
    """Ensure the target instance is running somewhere."""
    instance = get_instance(args.project, args.instance)

    if instance:
        if instance.status.upper() == "RUNNING":
            print(f"{instance.name} is already running in {instance.zone}. Nothing to do.")
            return

        if start_existing_instance(args.project, instance):
            return

        # If we reach here the instance was deleted due to capacity constraints.

    else:
        print(f"{args.instance} does not exist. It will be created from snapshot {args.snapshot}.")

    for zone in args.zones:
        try:
            if create_instance(
                args.project,
                args.instance,
                zone,
                machine_type=args.machine_type,
                accelerator=args.accelerator,
                scopes=args.scopes,
                tags=args.tags,
                boot_disk_type=args.boot_disk_type,
                boot_disk_size=args.boot_disk_size,
                snapshot=args.snapshot,
                preemptible=args.preemptible,
            ):
                print(f"Instance {args.instance} is ready in {zone}.")
                return
        except GCloudError as exc:
            raise

    zones = ", ".join(args.zones)
    raise GCloudError(
        f"Unable to create {args.instance} in any preferred zone ({zones}). "
        "All zones reported insufficient GPU capacity."
    )


def parse_arguments(argv: Iterable[str]) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Start the BECA VM, recreating it in another zone if GPU capacity is unavailable."
    )
    parser.add_argument("--project", default="beca-0001", help="GCP project ID (default: beca-0001)")
    parser.add_argument("--instance", default="beca-ollama", help="Instance name (default: beca-ollama)")
    parser.add_argument(
        "--zones",
        nargs="+",
        default=["us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f"],
        help="Preferred zones to try in order (default: us-central1-a us-central1-b us-central1-c us-central1-f)",
    )
    parser.add_argument("--machine-type", default="n1-standard-2", help="Machine type for new instances")
    parser.add_argument(
        "--accelerator",
        default="type=nvidia-tesla-t4,count=1",
        help="GPU accelerator specification (default: type=nvidia-tesla-t4,count=1)",
    )
    parser.add_argument(
        "--snapshot",
        default="beca-ollama-snap-20251007-140005",
        help="Snapshot to use when recreating the instance",
    )
    parser.add_argument("--boot-disk-type", default="pd-ssd", help="Boot disk type (default: pd-ssd)")
    parser.add_argument("--boot-disk-size", type=int, default=50, help="Boot disk size in GB (default: 50)")
    parser.add_argument("--scopes", default="https://www.googleapis.com/auth/cloud-platform", help="Scopes for the instance")
    parser.add_argument("--tags", default="ollama", help="Network tags for the instance (default: ollama)")
    parser.add_argument(
        "--preemptible",
        action="store_true",
        help="Create the instance as preemptible (matches prior configuration)",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_arguments(argv)
    try:
        ensure_instance_running(args)
    except GCloudError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Cancelled by user.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
