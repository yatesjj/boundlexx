#!/usr/bin/env python3
"""
run_for_parallel_test_containers.py

Manages parallel test containers by dynamically offsetting ports based on instance number.
Allows running multiple test environments simultaneously without port conflicts.

Usage:
  python run_for_parallel_test_containers.py --instance 1  # ports +1
  python run_for_parallel_test_containers.py --instance 2  # ports +2
  python run_for_parallel_test_containers.py --instance 3  # ports +3
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path


def get_current_folder_name():
    """Get the current folder name for prefixing."""
    return Path.cwd().parent.name


def offset_port_by_instance(match, instance_num):
    """Offset port by instance number."""
    prefix, host_port, suffix, container_port = match.groups()
    try:
        new_host_port = str(int(host_port) + instance_num)
    except ValueError:
        new_host_port = host_port
    return f"{prefix}{new_host_port}{suffix}:{container_port}"


def create_temp_compose_files(instance_num):
    """Create temporary compose files with instance-specific ports and names."""
    folder_name = get_current_folder_name()
    instance_suffix = f"-instance{instance_num}"

    # Files to process
    compose_files = [
        Path("docker-compose.yml"),
        Path("docker-compose.override.yml"),
    ]
    env_file = Path(".env")

    # Patterns
    port_pattern = re.compile(r'(["\']?)(\d{4,5})(["\']?):(\d{4,5})')
    name_pattern = re.compile(r"(container_name|service|network|name):\s*([\w-]+)")

    temp_files = []

    # Process compose files
    for compose_file in compose_files:
        if not compose_file.exists():
            continue

        temp_file = compose_file.with_suffix(
            f".instance{instance_num}{compose_file.suffix}"
        )
        text = compose_file.read_text(encoding="utf-8")

        # Offset ports
        text = port_pattern.sub(
            lambda m: offset_port_by_instance(m, instance_num), text
        )

        # Prefix names with folder and instance
        def prefix_name_with_instance(match):
            key, value = match.groups()
            if value.startswith(f"{folder_name}{instance_suffix}"):
                return match.group(0)
            elif value.startswith(folder_name):
                # Replace existing folder prefix with folder + instance
                new_value = value.replace(
                    folder_name, f"{folder_name}{instance_suffix}", 1
                )
                return f"{key}: {new_value}"
            else:
                return f"{key}: {folder_name}{instance_suffix}-{value}"

        text = name_pattern.sub(prefix_name_with_instance, text)

        temp_file.write_text(text, encoding="utf-8")
        temp_files.append(temp_file)
        print(f"Created temporary file: {temp_file}")

    # Process .env file
    if env_file.exists():
        temp_env_file = Path(f".env.instance{instance_num}")
        lines = env_file.read_text(encoding="utf-8").splitlines()
        new_lines = []

        for line in lines:
            # Offset port numbers in env vars
            port_match = re.match(r"([A-Z_]+)=(\d{4,5})", line)
            if port_match:
                key, port = port_match.groups()
                try:
                    new_port = str(int(port) + instance_num)
                    new_lines.append(f"{key}={new_port}")
                    continue
                except ValueError:
                    pass

            # Prefix names in env vars
            name_match = re.match(r"([A-Z_]+)=(.+)", line)
            if name_match and not name_match.group(2).startswith(
                f"{folder_name}{instance_suffix}"
            ):
                key, value = name_match.groups()
                if "NAME" in key or "SERVICE" in key or "NETWORK" in key:
                    if value.startswith(folder_name):
                        new_value = value.replace(
                            folder_name, f"{folder_name}{instance_suffix}", 1
                        )
                        new_lines.append(f"{key}={new_value}")
                    else:
                        new_lines.append(
                            f"{key}={folder_name}{instance_suffix}-{value}"
                        )
                    continue

            new_lines.append(line)

        temp_env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        temp_files.append(temp_env_file)
        print(f"Created temporary env file: {temp_env_file}")

    return temp_files


def run_docker_compose(instance_num, command_args):
    """Run docker-compose with instance-specific files."""
    compose_args = []

    # Add compose file arguments
    for file_name in ["docker-compose.yml", "docker-compose.override.yml"]:
        temp_file = Path(file_name).with_suffix(f".instance{instance_num}.yml")
        if temp_file.exists():
            compose_args.extend(["-f", str(temp_file)])

    # Add env file argument
    temp_env_file = Path(f".env.instance{instance_num}")
    if temp_env_file.exists():
        compose_args.extend(["--env-file", str(temp_env_file)])

    # Build full command
    cmd = ["docker-compose"] + compose_args + command_args

    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd)


def cleanup_temp_files(instance_num):
    """Clean up temporary files for the instance."""
    patterns = [
        f"docker-compose.instance{instance_num}.yml",
        f"docker-compose.override.instance{instance_num}.yml",
        f".env.instance{instance_num}",
    ]

    for pattern in patterns:
        temp_file = Path(pattern)
        if temp_file.exists():
            temp_file.unlink()
            print(f"Cleaned up: {temp_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run parallel test containers with instance-specific ports and names"
    )
    parser.add_argument(
        "--instance",
        type=int,
        required=True,
        help="Instance number (ports will be offset by this amount)",
    )
    parser.add_argument(
        "--cleanup-only",
        action="store_true",
        help="Only clean up temporary files for the instance",
    )
    parser.add_argument(
        "compose_args",
        nargs="*",
        default=["up", "-d"],
        help="Arguments to pass to docker-compose (default: up -d)",
    )

    args = parser.parse_args()

    if args.instance < 1:
        print("Error: Instance number must be 1 or greater")
        sys.exit(1)

    # Cleanup mode
    if args.cleanup_only:
        cleanup_temp_files(args.instance)
        return

    try:
        # Create temporary files
        temp_files = create_temp_compose_files(args.instance)

        if not temp_files:
            print("Error: No compose files found to process")
            sys.exit(1)

        # Run docker-compose
        result = run_docker_compose(args.instance, args.compose_args)

        # If the command was 'down', cleanup temp files
        if "down" in args.compose_args:
            cleanup_temp_files(args.instance)

        sys.exit(result.returncode)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        cleanup_temp_files(args.instance)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        cleanup_temp_files(args.instance)
        sys.exit(1)


if __name__ == "__main__":
    main()
