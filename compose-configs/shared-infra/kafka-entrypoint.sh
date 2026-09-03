#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
#
# Kafka KRaft entrypoint — replaces the one baked into the cleanstart/kafka
# image (/usr/local/bin/kafka-entrypoint.sh).
#
# WHY THIS EXISTS
# ---------------
# The stock entrypoint generates server.properties from a fixed heredoc and
# substitutes only eight whitelisted variables (PROCESS_ROLES, NODE_ID,
# CONTROLLER_QUORUM_VOTERS, LISTENERS, ADVERTISED_LISTENERS,
# CONTROLLER_LISTENER_NAMES, LISTENER_SECURITY_PROTOCOL_MAP, LOG_DIRS).
# Everything else is a hardcoded literal, so the retention/segment tuning
# that shared-infra.yaml passed as KAFKA_CFG_* was silently ignored:
# the broker ran with log.retention.hours=168 (not the intended 24) and
# log.segment.bytes=1073741824 (not the intended ~102 MB).
#
# The consequence was not theoretical. On 2026-08-16 the audit-logs topic had
# grown to 14 GB in 1 GB segments and the broker died with
# java.lang.OutOfMemoryError: Java heap space. The JVM stayed alive after the
# broker shut down, so Docker's `restart: always` never fired and Kafka sat
# half-dead for five days before a deploy-time healthcheck caught it.
#
# This script keeps the stock script's structure and formatting behaviour but
# makes every tunable genuinely env-driven, so the KAFKA_CFG_* values in
# shared-infra.yaml mean what they appear to mean. Defaults below match that
# file's intent, so the config is correct even if a variable is unset.
#
# Heap is handled separately: kafka-server-start.sh defaults to -Xmx1G -Xms1G
# only when KAFKA_HEAP_OPTS is unset, so shared-infra.yaml sets it directly and
# no change is needed here.
#
# If the image is ever bumped, re-check the vendor entrypoint for new settings
# worth carrying across — this file deliberately shadows it.

set -e

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Kafka KRaft entrypoint (egeria-workspaces override)"

KAFKA_HOME=${KAFKA_HOME:-/usr/lib/kafka}
CONFIG_DIR=${CONFIG_DIR:-/opt/kafka/config}
LOG_DIR=${KAFKA_CFG_LOG_DIRS:-/opt/kafka/kraft-logs}

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Kafka installation: $KAFKA_HOME"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Config directory:   $CONFIG_DIR"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Log directory:      $LOG_DIR"

mkdir -p "$CONFIG_DIR" "$LOG_DIR"

# Retention/segment defaults mirror shared-infra.yaml's intent. Sized for a
# demo environment that produces a large, low-value audit-log stream: keep a
# day of history, cap each partition, and use ~102 MB segments so retention
# can actually reclaim space (a 1 GB segment is only deleted once *all* of it
# ages out, which is what let the audit-logs topic reach 14 GB).
RETENTION_HOURS=${KAFKA_CFG_LOG_RETENTION_HOURS:-24}
RETENTION_BYTES=${KAFKA_CFG_LOG_RETENTION_BYTES:-536870912}
SEGMENT_BYTES=${KAFKA_CFG_LOG_SEGMENT_BYTES:-107374182}
RETENTION_CHECK_MS=${KAFKA_CFG_LOG_RETENTION_CHECK_INTERVAL_MS:-300000}
CLEANER_ENABLE=${KAFKA_CFG_LOG_CLEANER_ENABLE:-true}
AUTO_CREATE_TOPICS=${KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE:-true}

# __consumer_offsets partition count. Only takes effect the first time this
# topic is auto-created — changing it later does nothing to an
# already-formatted log dir (Kafka can't shrink an existing topic's
# partition count, only grow it, and won't do even that for an internal
# topic via the normal path). Kafka's own compiled-in default is 50,
# sized for multi-broker production clusters with many consumer groups;
# for this single-broker demo instance that's 50x more coordinator-managed
# partitions than there's any benefit to, for a single node. 2026-09-04:
# confirmed 100+ live consumer groups registered (Egeria integration
# connectors/survey/governance engines across quickstart and freshstart)
# against the stock 50-partition topic, alongside a chronic
# GroupCoordinator write-timeout/rebalance-storm pattern in qs-engine-host/
# qs-integration-daemon logs (see project memory
# kafka_coordinator_rebalance_storm.md) -- unconfirmed whether this
# actually contributed, but there's no benefit to 50 on one broker either
# way. Lowered as part of a fresh-database redeploy, where the existing
# topic's committed offsets aren't being preserved anyway -- this value is
# irrelevant to an already-formatted log dir; changing it further after
# this redeploy would need the same delete-and-recreate treatment.
OFFSETS_TOPIC_PARTITIONS=${KAFKA_CFG_OFFSETS_TOPIC_NUM_PARTITIONS:-10}

cat > "$CONFIG_DIR/server.properties" << EOF
# KRaft mode configuration
process.roles=${KAFKA_CFG_PROCESS_ROLES}
node.id=${KAFKA_CFG_NODE_ID}
controller.quorum.voters=${KAFKA_CFG_CONTROLLER_QUORUM_VOTERS}

# Listeners
listeners=${KAFKA_CFG_LISTENERS}
advertised.listeners=${KAFKA_CFG_ADVERTISED_LISTENERS}
controller.listener.names=${KAFKA_CFG_CONTROLLER_LISTENER_NAMES}
listener.security.protocol.map=${KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP}

# Logs
log.dirs=${KAFKA_CFG_LOG_DIRS}

# Basic settings
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# Log settings
num.partitions=1
num.recovery.threads.per.data.dir=1
offsets.topic.replication.factor=1
offsets.topic.num.partitions=${OFFSETS_TOPIC_PARTITIONS}
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1
auto.create.topics.enable=${AUTO_CREATE_TOPICS}

# Retention — the settings the stock entrypoint hardcoded past. See header.
log.retention.hours=${RETENTION_HOURS}
log.retention.bytes=${RETENTION_BYTES}
log.segment.bytes=${SEGMENT_BYTES}
log.retention.check.interval.ms=${RETENTION_CHECK_MS}
log.cleaner.enable=${CLEANER_ENABLE}

# Group coordinator settings
group.initial.rebalance.delay.ms=0
EOF

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generated Kafka KRaft configuration"
echo "[$(date '+%Y-%m-%d %H:%M:%S')]   log.retention.hours=${RETENTION_HOURS}" \
     "log.retention.bytes=${RETENTION_BYTES} log.segment.bytes=${SEGMENT_BYTES}"
echo "[$(date '+%Y-%m-%d %H:%M:%S')]   offsets.topic.num.partitions=${OFFSETS_TOPIC_PARTITIONS}" \
     "(only takes effect if __consumer_offsets doesn't already exist)"
echo "[$(date '+%Y-%m-%d %H:%M:%S')]   KAFKA_HEAP_OPTS=${KAFKA_HEAP_OPTS:-<unset, kafka-server-start.sh will use -Xmx1G -Xms1G>}"

# Format only on a genuinely empty log dir. meta.properties is what makes this
# safe to re-run against an existing volume — never remove this guard, it is
# all that stands between a restart and wiping the metadata store's topics.
if [ ! -f "$LOG_DIR/meta.properties" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Formatting log directory with cluster UUID: $KAFKA_KRAFT_CLUSTER_ID"
    "$KAFKA_HOME/bin/kafka-storage.sh" format -t "$KAFKA_KRAFT_CLUSTER_ID" -c "$CONFIG_DIR/server.properties"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Log directory formatted successfully"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Log directory already formatted, skipping format"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Kafka server in KRaft mode"
exec "$KAFKA_HOME/bin/kafka-server-start.sh" "$CONFIG_DIR/server.properties"
