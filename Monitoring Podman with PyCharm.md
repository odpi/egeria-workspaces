# Monitoring Podman with PyCharm

This document describes how to monitor the Egeria Podman deployment using PyCharm's Services tool window.

## 1. Enable the Podman Socket
PyCharm communicates with Podman via a Unix socket.

### Configure Socket Permissions
To ensure PyCharm can access the socket without root privileges, create a systemd override:
1. Create the directory:
   ```bash
   mkdir -p ~/.config/systemd/user/podman.socket.d
   ```
2. Create the override file `~/.config/systemd/user/podman.socket.d/override.conf`:
   ```ini
   [Socket]
   SocketMode=0666
   ```
3. Reload systemd and restart the socket:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now podman.socket
   ```

Verify it is running and has the correct permissions (`srw-rw-rw-`):
```bash
ls -l /run/user/$(id -u)/podman/podman.sock
```

## 2. Configure Docker in PyCharm
1. Open PyCharm **Settings** (Ctrl+Alt+S / ⌘,).
2. Navigate to **Build, Execution, Deployment** > **Docker**.
3. Click the **+** icon to add a new Docker configuration.
4. Select **Podman** as the connection type.
5. PyCharm should automatically detect the socket path. Once it says "Connection successful," click **OK**.

## 3. Register Docker Compose Files
To see the full stack (including services like Kafka and Postgres) in the **Services** window:
1. Open the **Services** tool window (`View > Tool Windows > Services`).
2. Right-click on the **Docker** node or use the **+** (Add Service) button.
3. Register the following Compose files (depending on which deployment you are using) to ensure PyCharm groups the containers correctly:

**Shared Infrastructure:**
- `compose-configs/shared-infra/shared-infra.yaml`

**Quickstart Deployment:**
- `compose-configs/egeria-quickstart/egeria-quickstart.yaml`
- `compose-configs/egeria-quickstart/egeria-quickstart-local.yaml`

**Freshstart Deployment:**
- `compose-configs/egeria-freshstart/egeria-freshstart.yaml`
- `compose-configs/egeria-freshstart/egeria-freshstart-local.yaml`

## 4. Monitor Services
Once connected, the **Services** window will show all running containers, logs, environment variables, and resource usage. You can also start/stop services directly from this interface.

## 5. Docker Compose Configuration
To ensure PyCharm's "Down" and "Redeploy" actions work correctly with our scripts, you need to configure the Docker Compose executable:

1. Go to **Settings** > **Build, Execution, Deployment** > **Docker** > **Tools**.
2. For **Docker Compose executable**, click the folder icon and browse to:
   `/home/dan/.local/bin/podman-compose`
   *(Alternatively, if you have `docker-compose` v2 installed and prefer it, ensure `DOCKER_HOST` is set as described in step 1).*
3. When registering Compose files in the Services window, right-click the Compose node, select **Edit Configuration**, and ensure the **Project name** is set:
   - For `shared-infra.yaml` set project name to: `egeria-shared-infra`
   - For `egeria-quickstart.yaml` set project name to: `egeria-quickstart`

## 6. Removing Images
The "Down" command in Docker/Podman Compose (and the corresponding button in PyCharm) **does not remove images** by default; it only stops and removes containers, networks, and volumes.

To remove images when redeploying:
- **In PyCharm:** You can manually remove images from the **Images** node under the Docker connection in the Services tool window.
- **Via CLI:** If you want to force a fresh pull/build of everything, you can use:
  ```bash
  # Take down and remove images
  podman-compose -p egeria-quickstart down --rmi all
  
  # Or use our scripts which handle builds
  ./quick-start-local --refresh-platform
  ```

## Troubleshooting

### "Connection Refused" Error
If PyCharm reports "Connection refused" even after enabling the socket, the socket file might be stale or the service might be in a bad state. 

Run the following commands to reset it:
```bash
systemctl --user stop podman.socket
rm -f /run/user/$(id -u)/podman/podman.sock
systemctl --user start podman.socket
```

Verify it is listening again:
```bash
podman --remote info
```
If `podman --remote info` works, PyCharm should also be able to connect.

### "Permission Denied" Error
Ensure your user has the correct permissions. The socket override we use (`SocketMode=0666`) should allow PyCharm to connect. You can check the permissions with:
```bash
ls -l /run/user/$(id -u)/podman/podman.sock
```
It should show `srw-rw-rw-`.

### "Down" or "Redeploy" fails in PyCharm
If the "Down" button does nothing or returns an error:
1. **Check Executable:** Ensure the Docker Compose executable is set to `podman-compose` in Settings (see Section 5).
2. **Project Name Mismatch:** Our scripts use specific project names (`egeria-quickstart`). If PyCharm uses a different name (like the folder name), it won't find the containers. Set the Project Name in the Compose Run Configuration.
3. **Multiple Files:** We have moved the essential host mappings (`host.docker.internal`) into the main YAML files, so they work even if you only register `egeria-quickstart.yaml`. However, for a complete view of the stack, you should still include **both** files in your PyCharm Compose configuration.

### Images not being removed
As mentioned in Section 6, the "Down" command is not designed to remove images. If you need to refresh your images:
1. Go to the **Images** node in the Services window.
2. Select the images (e.g., `egeria-quickstart-platform`) and click **Delete**.
3. Re-run your deployment script or PyCharm Run configuration.
4. Alternatively, use `./quick-start-local --refresh-platform` from the terminal.

### Volume Permissions ("Permission Denied")
In rootless Podman, the host user (UID 1000) maps to the container's `root` (UID 0). Any other user inside the container (like Jupyter's `jovyan` UID 1000) will see host-mounted volumes as owned by `root` and may be unable to write to them.

We have addressed this in two ways:
1. **Running as Root:** The Jupyter service is now configured to run as `user: root` in the Compose files. This ensures it has the same permissions as your host user.
2. **Automated Permission Setup:** Our startup scripts (`./quick-start-local` and `./fresh-start-local`) now automatically run `podman unshare chmod -R a+rwX` on shared directories like `work/` and `exchange-*/`. This ensures that even non-root containers (like the Egeria platform) can write to these shared volumes.

If you encounter `Permission denied` errors when running the containers directly via PyCharm:
- Run the local startup script once (`./quick-start-local`) to initialize the directory permissions.
- Ensure you are using the latest version of the Compose files from the `podman-deployment` branch.

### Postgres or Kafka "Connection Refused" in Containers
If you see `Connection to host.docker.internal:5442 refused` (Postgres) or `No resolvable bootstrap urls given in bootstrap.servers` (Kafka), it is usually because of how Podman handles internal network resolution and port bindings.

We have updated the following to fix this:
- **Postgres:** Now binds to all interfaces (`0.0.0.0`) and containers use `host.docker.internal:5442`.
- **Kafka:** We now use the `EXTERNAL` listener on port `9194`. Containers connect via `host.docker.internal:9194`.

**To apply the fix:**
1. Pull the latest changes from the repository.
2. Restart the shared infrastructure:
   ```bash
   compose-configs/shared-infra/ensure-shared-infra.sh
   ```
3. Regenerate environment files and restart your deployment:
   ```bash
   # For Quickstart
   ./quick-start-local
   # For Freshstart
   ./fresh-start-local
   ```
