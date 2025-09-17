#!/usr/bin/env python3
"""
Boundlexx Test Environment Manager

Creates isolated test environments by:
1. Cleaning up old test containers/volumes
2. Cloning current branch to a parallel test directory
3. Setting up test environment with boundlexx-test naming
4. Optionally starting the test environment

Works on Windows (PowerShell), Linux, and macOS.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def detect_shell_environment():
    """Detect the current shell environment."""
    system = platform.system().lower()
    shell_info = {
        'system': system,
        'is_windows': system == 'windows',
        'shell': 'unknown'
    }
    
    # Detect shell type
    if shell_info['is_windows']:
        # Check if running in PowerShell
        if os.environ.get('PSModulePath'):
            shell_info['shell'] = 'powershell'
        else:
            shell_info['shell'] = 'cmd'
    else:
        # Unix-like systems
        shell = os.environ.get('SHELL', '').split('/')[-1]
        shell_info['shell'] = shell or 'bash'
    
    return shell_info


def run_command(cmd, shell_env, cwd=None, capture_output=False):
    """Run a command appropriate for the current shell environment."""
    try:
        if shell_env['is_windows'] and shell_env['shell'] == 'powershell':
            # Use PowerShell on Windows
            if isinstance(cmd, list):
                cmd_str = ' '.join(cmd)
            else:
                cmd_str = cmd
            result = subprocess.run(
                ['powershell', '-Command', cmd_str],
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=True
            )
        else:
            # Use regular subprocess for bash/cmd
            result = subprocess.run(
                cmd if isinstance(cmd, list) else cmd.split(),
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=True,
                shell=not isinstance(cmd, list)
            )
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        if capture_output and e.stdout:
            print(f"   stdout: {e.stdout}")
        if capture_output and e.stderr:
            print(f"   stderr: {e.stderr}")
        return None


def get_current_branch():
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Could not determine current branch")
        return None


def get_remote_url():
    """Get the remote origin URL."""
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Could not determine remote URL")
        return None


def cleanup_test_containers(shell_env, dry_run=False):
    """Clean up existing test containers and volumes."""
    print("🧹 Cleaning up existing test containers and volumes...")
    
    if shell_env['is_windows']:
        cleanup_commands = [
            # Stop and remove boundlexx-test containers
            ("docker ps -a --filter name=boundlexx-test --format '{{.Names}}' | "
             "ForEach-Object { docker stop $_; docker rm $_ }"),
            # Remove boundlexx-test volumes
            ("docker volume ls --filter name=boundlexx-test --format '{{.Name}}' | "
             "ForEach-Object { docker volume rm $_ }"),
            # Remove boundlexx-test networks
            ("docker network ls --filter name=boundlexx-test --format '{{.Name}}' | "
             "ForEach-Object { docker network rm $_ }")
        ]
    else:
        # Unix commands
        cleanup_commands = [
            ("docker ps -a --filter name=boundlexx-test --format '{{.Names}}' | "
             "xargs -r docker stop"),
            ("docker ps -a --filter name=boundlexx-test --format '{{.Names}}' | "
             "xargs -r docker rm"),
            ("docker volume ls --filter name=boundlexx-test --format '{{.Name}}' | "
             "xargs -r docker volume rm"),
            ("docker network ls --filter name=boundlexx-test --format '{{.Name}}' | "
             "xargs -r docker network rm")
        ]
    
    for cmd in cleanup_commands:
        if dry_run:
            print(f"   [DRY RUN] Would run: {cmd}")
        else:
            print(f"   Running: {cmd}")
            result = run_command(cmd, shell_env, capture_output=True)
            if result and result.returncode == 0:
                print("   ✅ Success")
            else:
                print("   ⚠️  Command completed (may have had nothing to clean)")


def clone_test_environment(
    source_dir, target_dir, branch_name, remote_url, dry_run=False
):
    """Clone the current branch to a test directory."""
    print(f"📂 Setting up test environment: {target_dir}")
    
    if target_dir.exists():
        if dry_run:
            print(f"   [DRY RUN] Would remove existing directory: {target_dir}")
        else:
            print(f"   Removing existing directory: {target_dir}")
            shutil.rmtree(target_dir)
    
    if dry_run:
        print(f"   [DRY RUN] Would clone {remote_url}")
        print(f"   [DRY RUN] Branch: {branch_name}, Target: {target_dir}")
        return True
    
    try:
        # Clone the repository
        print(f"   Cloning {remote_url} (branch: {branch_name})...")
        subprocess.run([
            'git', 'clone', '--branch', branch_name, '--single-branch',
            remote_url, str(target_dir)
        ], check=True, capture_output=True, text=True)
        
        print("   ✅ Repository cloned successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Clone failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False


def setup_test_container(test_dir, shell_env, dry_run=False):
    """Set up the test container configuration."""
    print("🐳 Setting up test container configuration...")
    
    setup_script = test_dir / "setup_containers.py"
    if not setup_script.exists():
        print(f"   ❌ Setup script not found: {setup_script}")
        return False
    
    # Copy .env to .local.env if it exists
    env_file = test_dir / ".env"
    local_env_file = test_dir / ".local.env"
    
    if env_file.exists() and not local_env_file.exists():
        if dry_run:
            print(f"   [DRY RUN] Would copy {env_file} to {local_env_file}")
        else:
            shutil.copy(env_file, local_env_file)
            print(f"   ✅ Copied {env_file} to {local_env_file}")
    
    # Run the setup script for test environment
    cmd = "python setup_containers.py --env test"
    if dry_run:
        cmd += " --dry-run"
    
    if dry_run:
        print(f"   [DRY RUN] Would run: {cmd}")
    else:
        print(f"   Running: {cmd}")
        result = run_command(cmd, shell_env, cwd=test_dir)
        if result:
            print("   ✅ Test environment configured")
            return True
        else:
            print("   ❌ Test environment setup failed")
            return False
    
    return True


def start_test_environment(test_dir, shell_env, dry_run=False):
    """Start the test environment containers."""
    print("🚀 Starting test environment...")
    
    cmd = "docker-compose up -d"
    
    if dry_run:
        print(f"   [DRY RUN] Would run: {cmd}")
        print("   [DRY RUN] Test environment would be available at:")
        print("   [DRY RUN] http://localhost:28001")
    else:
        print(f"   Running: {cmd}")
        result = run_command(cmd, shell_env, cwd=test_dir)
        if result:
            print("   ✅ Test environment started")
            print("   🌐 Test environment available at: http://localhost:28001")
            print("   📊 Admin interface: http://localhost:28001/admin/")
            return True
        else:
            print("   ❌ Failed to start test environment")
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Create and manage Boundlexx test environments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_test_environment.py                    # Full setup with prompts
  python create_test_environment.py --dry-run          # Preview without changes
  python create_test_environment.py --skip-cleanup    # Don't clean up old containers
  python create_test_environment.py --start           # Start containers after setup
  python create_test_environment.py --target-dir ../my-test  # Custom test directory
"""
    )
    
    parser.add_argument(
        '--target-dir',
        help='Target directory for test environment '
             '(default: ../boundlexx-yatesjj-test)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview operations without making changes'
    )
    parser.add_argument(
        '--skip-cleanup', action='store_true',
        help='Skip cleanup of existing test containers'
    )
    parser.add_argument(
        '--start', action='store_true',
        help='Start the test environment containers after setup'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Force operations without prompting'
    )
    
    args = parser.parse_args()
    
    # Detect environment
    shell_env = detect_shell_environment()
    print(f"🔍 Detected environment: {shell_env['system']} ({shell_env['shell']})")
    
    # Validate we're in a boundlexx project
    current_dir = Path.cwd()
    if not (current_dir / "docker-compose.yml").exists():
        print("❌ Error: Not in a Boundlexx project directory")
        print("   (docker-compose.yml not found)")
        sys.exit(1)
    
    # Get current branch and remote
    branch_name = get_current_branch()
    if not branch_name:
        sys.exit(1)
    
    remote_url = get_remote_url()
    if not remote_url:
        sys.exit(1)
    
    print(f"📋 Current branch: {branch_name}")
    print(f"📍 Remote URL: {remote_url}")
    
    # Determine target directory
    if args.target_dir:
        target_dir = Path(args.target_dir).resolve()
    else:
        # Default: sibling directory with -test suffix
        target_dir = current_dir.parent / f"{current_dir.name}-test"
    
    print(f"🎯 Target test directory: {target_dir}")
    
    # Confirm operation if not forced
    if not args.force and not args.dry_run:
        prompt = (f"\n💭 Create test environment for branch '{branch_name}' "
                  f"in '{target_dir}'? (y/N): ")
        response = input(prompt)
        if response.lower() != 'y':
            print("❌ Operation cancelled")
            sys.exit(0)
    
    print(f"\n🚀 Creating test environment for branch: {branch_name}")
    print("=" * 60)
    
    # Step 1: Cleanup existing test containers
    if not args.skip_cleanup:
        cleanup_test_containers(shell_env, args.dry_run)
        print()
    
    # Step 2: Clone repository to test directory
    clone_success = clone_test_environment(
        current_dir, target_dir, branch_name, remote_url, args.dry_run
    )
    if not clone_success:
        sys.exit(1)
    print()
    
    # Step 3: Set up test container configuration
    if not setup_test_container(target_dir, shell_env, args.dry_run):
        sys.exit(1)
    print()
    
    # Step 4: Start test environment (if requested)
    if args.start:
        if not start_test_environment(target_dir, shell_env, args.dry_run):
            sys.exit(1)
        print()
    
    # Success summary
    print("🎉 Test environment setup complete!")
    print(f"   📂 Location: {target_dir}")
    print(f"   🌿 Branch: {branch_name}")
    if args.start and not args.dry_run:
        print("   🌐 URL: http://localhost:28001")
        print("   📊 Admin: http://localhost:28001/admin/")
    
    print("\n💡 Next steps:")
    if args.dry_run:
        print("   1. Run without --dry-run to apply changes")
    else:
        print(f"   1. cd {target_dir}")
        if not args.start:
            print("   2. Review docker-compose.override.yml configuration")
            print("   3. docker-compose up -d")
        print("   4. Run migrations:")
        print("      docker-compose run --rm manage python manage.py migrate")
        print("   5. Create superuser:")
        print("      docker-compose run --rm manage python manage.py createsuperuser")


if __name__ == '__main__':
    main()
