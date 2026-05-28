#!/usr/bin/env bash

# 1. Smart Engine Detection
if [[ -z "${CONTAINER_ENGINE:-}" ]]; then
    if command -v podman &> /dev/null && ! docker version 2>&1 | grep -q "Docker Engine"; then
        echo "[Engine] Podman detected as the primary container runtime."
        CONTAINER_ENGINE="podman"
        
        # Auto-detect the active rootless user socket path
        USER_ID=$(id -u)
        if [ -S "/run/user/$USER_ID/podman/podman.sock" ]; then
            export DOCKER_HOST="unix:///run/user/$USER_ID/podman/podman.sock"
        elif [ -S "/run/podman/podman.sock" ]; then
            export DOCKER_HOST="unix:///run/podman/podman.sock"
        fi
    else
        echo "[Engine] Standard Docker Engine detected."
        CONTAINER_ENGINE="docker"
    fi
fi

if [[ -z "${COMPOSE_CMD:-}" ]]; then
    if [[ "$CONTAINER_ENGINE" == "podman" ]]; then
        if command -v podman-compose &> /dev/null; then
            COMPOSE_CMD="podman-compose"
        else
            COMPOSE_CMD="docker compose"
        fi
    else
        COMPOSE_CMD="docker compose"
    fi
fi

export CONTAINER_ENGINE
export COMPOSE_CMD

if [[ "$COMPOSE_CMD" == "podman-compose" ]]; then
    # podman-compose does not support --pull as an argument to build/up
    export COMPOSE_PULL_FLAGS=""
    export COMPOSE_BUILD_PULL_FLAGS=""
else
    export COMPOSE_PULL_FLAGS="--pull always"
    export COMPOSE_BUILD_PULL_FLAGS="--pull"
fi

if [[ "$CONTAINER_ENGINE" == "podman" ]]; then
    # Podman uses .State.Healthcheck.Status, Docker uses .State.Health.Status
    export INSPECT_STATUS_FORMAT='{{if .State.Healthcheck.Status}}{{.State.Healthcheck.Status}}{{else}}{{.State.Status}}{{end}}'
    # podman-compose ignores external: true networks and attaches containers to the default
    # 'podman' bridge instead. Use the default podman network gateway for host resolution.
    GW_IP=$(podman network inspect podman 2>/dev/null | grep '"gateway"' | cut -d'"' -f4 | head -n 1 || true)
    export HOST_GATEWAY_IP="${GW_IP:-10.88.0.1}"
else
    export INSPECT_STATUS_FORMAT='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}'
    export HOST_GATEWAY_IP="host-gateway"
fi

if [[ "$CONTAINER_ENGINE" == "podman" && -n "${DOCKER_HOST:-}" ]]; then
    echo "[Engine] Directing API traffic to: $DOCKER_HOST"
fi

# Helper to prepare a directory with proper permissions for containers
# Handles both Docker and Podman (including rootless)
prepare_runtime_dir() {
    local dir="$1"
    mkdir -p "$dir"
    local success=0
    if [[ "$CONTAINER_ENGINE" == "podman" ]]; then
        # In rootless Podman, unshare enters the user namespace where container-owned files are manageable
        $CONTAINER_ENGINE unshare chmod -R a+rwX "$dir" 2>/dev/null || chmod -R a+rwX "$dir" 2>/dev/null || success=1
    else
        chmod -R a+rwX "$dir" 2>/dev/null || success=1
    fi
    if [[ $success -ne 0 ]]; then
         echo "[Engine] Warning: Could not fully set permissions on $dir. If you encounter errors, you may need to use sudo to fix ownership (e.g. sudo chown -R $(id -u):$(id -g) $dir)" >&2
    fi
    return 0
}

# Helper to safely remove a directory that might be owned by a container user
# If deletion fails (e.g. root-owned leftovers from Docker), it attempts to move it aside.
safe_rm_rf() {
    local dir="$1"
    [[ ! -e "$dir" ]] && return 0

    if [[ "$CONTAINER_ENGINE" == "podman" ]]; then
        $CONTAINER_ENGINE unshare rm -rf "$dir" 2>/dev/null || rm -rf "$dir" 2>/dev/null || true
    else
        rm -rf "$dir" 2>/dev/null || true
    fi

    if [[ -e "$dir" ]]; then
        # If it still exists, try moving it aside as a last resort if we have write access to parent
        local parent="$(dirname "$dir")"
        if [[ -w "$parent" ]]; then
            local timestamp=$(date +%Y%m%d%H%M%S)
            local junk="${dir}.root-owned.${timestamp}"
            if mv "$dir" "$junk" 2>/dev/null; then
                echo "[Engine] Warning: Could not delete $dir (likely root-owned). Moved it to $junk to allow progress." >&2
                return 0
            fi
        fi
        echo "[Engine] ERROR: Could not remove $dir. If this was created by a different container engine (e.g. Docker), you must remove it with sudo." >&2
        return 1
    fi
    return 0
}
