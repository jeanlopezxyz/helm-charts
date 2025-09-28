# Nexus Repository OSS Helm Chart

Helm chart for deploying Nexus Repository OSS on OpenShift/Kubernetes for artifact management and storage.

## Features

- ✅ **Latest Version**: Nexus Repository OSS 3.45.0
- ✅ **OpenShift Compatible**: Security contexts and SCCs compliant
- ✅ **Persistent Storage**: Configurable PVC for artifact storage
- ✅ **Auto-Route**: OpenShift route with TLS termination
- ✅ **Security**: Non-root containers with minimal privileges
- ✅ **Production Ready**: Resource limits and health checks

## Quick Start

### Basic Installation
```bash
helm install nexus charts/setup-platform-nexus \
  --namespace nexus --create-namespace
```

### With Custom Storage
```bash
helm install nexus charts/setup-platform-nexus \
  --namespace nexus --create-namespace \
  --set persistence.size=100Gi \
  --set persistence.storageClass=gp3
```

### With Custom Admin Password
```bash
helm install nexus charts/setup-platform-nexus \
  --namespace nexus --create-namespace \
  --set nexus.defaultAdminPassword="MySecurePassword123"
```

## Configuration

### Repository Types

The chart supports enabling/disabling default repository types:

```yaml
nexus:
  repositories:
    maven: 
      enabled: true    # Maven Central proxy
    npm:
      enabled: true    # NPM registry proxy  
    docker:
      enabled: true    # Docker registry
    pypi:
      enabled: true    # Python Package Index
```

### Storage Configuration

```yaml
persistence:
  enabled: true
  storageClass: "gp3"
  size: "100Gi"
  accessMode: "ReadWriteOnce"
```

### Resource Configuration

```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "500m"
  limits:
    memory: "4Gi" 
    cpu: "2000m"
```

### JVM Tuning

```yaml
nexus:
  jvm:
    minHeapSize: "2G"
    maxHeapSize: "4G"
```

## Access

After deployment, Nexus will be available at:
- **OpenShift**: Automatic route creation with TLS
- **Kubernetes**: Configure ingress in values.yaml

Default credentials:
- **Username**: `admin`
- **Password**: Value from `nexus.defaultAdminPassword` (default: `admin123`)

**⚠️ Important**: Change the admin password after first login!

## Repository Management

Nexus supports multiple repository types:
- **Maven**: For Java artifacts
- **NPM**: For Node.js packages
- **Docker**: For container images
- **PyPI**: For Python packages
- **Raw**: For any file type

## Security

- Non-root containers
- Read-only root filesystem where possible
- Minimal capabilities
- OpenShift SCC compliant
- TLS encryption for web interface

## Monitoring

Optional ServiceMonitor for Prometheus:

```yaml
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s
```

## Backup

Optional backup configuration:

```yaml
backup:
  enabled: true
  schedule: "0 2 * * *"  # Daily at 2 AM
  retention: "30d"
  storageSize: "10Gi"
```