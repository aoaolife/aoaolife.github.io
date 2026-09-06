#!/usr/bin/env python3
# AOAO_DOMAIN: WEB
# AOAO_TOOL: auto_deploy
# AOAO_SUMMARY: 自动化 Docker 部署、同步与备份工具

import os
import sys
import tarfile
import paramiko
import shutil
import stat
import subprocess
import datetime

# --- Configuration ---
# Ensure we are running in the script's directory so relative paths work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

SERVER_IP = "1.116.113.85"
SERVER_PORT = 22
SERVER_USER = "root"
SSH_KEY_FILE = "jiegeedukg.pem" 
REMOTE_DIR = "/app/aoao_web"
REMOTE_DATA_DIR = "/home/aoaolife"
LOCAL_DATA_DIR = "/mnt/c/aoaolife"

def get_secure_key_path():
    if not os.path.exists(SSH_KEY_FILE):
        print(f"❌ Error: Key file '{SSH_KEY_FILE}' not found")
        sys.exit(1)
    # On Linux/WSL, key permission must be strict
    if os.name != 'nt':
        secure_dir = os.path.expanduser("~/.ssh_temp_deploy")
        os.makedirs(secure_dir, exist_ok=True)
        secure_path = os.path.join(secure_dir, SSH_KEY_FILE)
        shutil.copy(SSH_KEY_FILE, secure_path)
        os.chmod(secure_path, stat.S_IRUSR | stat.S_IWUSR)
        return secure_path
    return SSH_KEY_FILE

def remote_pre_backup():
    """
    Step 0: Before touching anything, create a snapshot on the remote server.
    """
    print("\n🛡️ [0/6] Remote Pre-Backup (Safety First)...")
    secure_key = get_secure_key_path()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        key = paramiko.RSAKey.from_private_key_file(secure_key)
        ssh.connect(SERVER_IP, port=SERVER_PORT, username=SERVER_USER, pkey=key, timeout=15)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        backup_file = f"/tmp/aoaolife_snapshot_{timestamp}.tar.gz"
        
        print(f"   📦 Creating remote snapshot: {backup_file}...")
        # Backup the data directory
        cmd = f"tar -czf {backup_file} -C {os.path.dirname(REMOTE_DATA_DIR)} {os.path.basename(REMOTE_DATA_DIR)}"
        ssh.exec_command(cmd)
        print("   ✅ Remote snapshot completed.")
    except Exception as e:
        print(f"   ⚠️ Remote backup skipped: {e}")
    finally:
        ssh.close()
        if secure_key != SSH_KEY_FILE and os.path.exists(secure_key):
            os.remove(secure_key)

def smart_sync_content():
    """
    Step 1: Bidirectional sync with "Latest Wins" logic, fix mtimes, then backup to Git.
    """
    print("\n🔄 [1/6] Smart Content Synchronization (Latest Wins)")
    
    # 1. Run sync_data.py for bidirectional rsync merge
    print("   ⬇️⬆️  Merging changes between Local and Remote...")
    try:
        # sync_data.py merge uses 'rsync -avzu' which implements "latest wins"
        subprocess.run([sys.executable, "sync_data.py", "merge"], check=True)
    except Exception as e:
        print(f"   ⚠️ Sync merge partially failed: {e}")

    # 2. Local Reset Mtimes (Critical for sorting)
    print("   🕒 Resetting local file timestamps...")
    subprocess.run([sys.executable, "reset_mtime.py"], check=True)
    
    # 3. Add and Commit to local GitHub repo for backup
    print("   💾 Committing and Pushing to GitHub backup...")
    cwd = LOCAL_DATA_DIR
    def run_git(args):
        return subprocess.run(["git"] + args, cwd=cwd, check=False, capture_output=True, text=True)

    run_git(["add", "."])
    status = run_git(["status", "--porcelain"]).stdout.strip()
    if status:
        msg = f"Auto-sync content backup {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        run_git(["commit", "-m", msg])
        run_git(["push", "origin", "master"])
        print("      ✅ GitHub backup updated.")
    else:
        print("      No content changes to commit.")

def create_tarball(output_filename="deploy_package.tar.gz"):
    print(f"\n📦 [3/6] Packaging Code...")
    exclude = {
        '.git', '__pycache__', '.idea', 'venv', '.venv', 
        output_filename, SSH_KEY_FILE, 'aoao.db', 
        'public', 'public_aoao', 'deploy_package.tar.gz',
        'public_html', 'temp_deploy_venv',
        '.build_cache.json', '.build_cache_aoao.json'
    }
    with tarfile.open(output_filename, "w:gz") as tar:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file not in exclude and not file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    tar.add(file_path, arcname=file_path)
    print("✅ Package created.")
    return output_filename

def deploy(tarball_path):
    print(f"\n🚀 [4/6] Deploying to {SERVER_IP}...")
    secure_key = get_secure_key_path()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        key = paramiko.RSAKey.from_private_key_file(secure_key)
        ssh.connect(SERVER_IP, port=SERVER_PORT, username=SERVER_USER, pkey=key, timeout=15)
        
        # Upload
        print(f"   ⬆️ Uploading package...")
        ssh.exec_command(f"mkdir -p {REMOTE_DIR}")
        sftp = ssh.open_sftp()
        sftp.put(tarball_path, f"{REMOTE_DIR}/{tarball_path}")
        sftp.close()
        
        # Remote Execute
        print(f"   🔄 Restarting Docker...")
        remote_script = f"""
        cd {REMOTE_DIR}
        tar -xzf {tarball_path}
        rm {tarball_path}
        
        export DOCKER_BUILDKIT=0
        if command -v docker-compose >/dev/null 2>&1; then
            docker-compose up -d --build
        else
            docker compose up -d --build
        fi
        """
        
        stdin, stdout, stderr = ssh.exec_command(remote_script)
        for line in stdout: print(f"   [Remote] {line.strip()}")
            
        if stdout.channel.recv_exit_status() == 0:
            print("✅ Deployment Success!")
            
            # 6. Remote Reset Mtime (Essential!)
            print(f"   🕒 Resetting remote file timestamps (in container)...")
            reset_cmd = f"docker exec aoao_web python3 reset_mtime.py"
            stdin, stdout, stderr = ssh.exec_command(reset_cmd)
            out = stdout.read().decode().strip()
            if out: print(f"   [Reset] {out}")

    except Exception as e:
        print(f"❌ Deploy Exception: {e}")
    finally:
        ssh.close()
        if os.path.exists(tarball_path):
            os.remove(tarball_path)
        if secure_key != SSH_KEY_FILE and os.path.exists(secure_key):
            os.remove(secure_key)

def trigger_backup():
    print("\n📧 [2/6] Local Backup & Mail...")
    try:
        subprocess.run([sys.executable, "backup_mailer.py"], check=True)
    except Exception as e:
        print(f"⚠️ Backup failed: {e}")

def run_publishers():
    print("\n🌐 [5/6] Generating Static Sites (aoao.life & emusk.cn)...")
    try:
        # Just generate, skip sync because we already synced in step 1
        subprocess.run([sys.executable, "aoao.py", "generate"], check=True)
        print("✅ Static sites generated.")
        
        print("\n🚀 [6/6] Deploying to GitHub Pages...")
        subprocess.run([sys.executable, "aoao.py", "deploy"], check=True)
        # emusk is cascaded in aoao.py 'all', but we call it explicitly for safety if needed
        subprocess.run([sys.executable, "emusk.py", "deploy"], check=True)
        print("✅ GitHub Pages updated.")
    except Exception as e:
        print(f"❌ Static site publish failed: {e}")

if __name__ == "__main__":
    # 0. Remote snapshot (Safety first)
    remote_pre_backup()
    
    # 1. Sync Content (Bidirectional, latest wins)
    smart_sync_content()
    
    # 2. Local Backup
    trigger_backup()
    
    # 3. Package
    tar_file = create_tarball()
    
    # 4. Deploy Server
    deploy(tar_file)
    
    # 5 & 6. Publish Static Sites
    run_publishers()
