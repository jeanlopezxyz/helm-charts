# SonarQube Community Edition Helm Chart

Helm chart for deploying SonarQube Community Edition on OpenShift/Kubernetes for code quality and security analysis.

## Features

- ✅ **Latest Stable**: SonarQube Community Edition 2025.1 LTA
- ✅ **PostgreSQL Database**: Integrated PostgreSQL for production use
- ✅ **OpenShift Compatible**: Security contexts and SCCs compliant
- ✅ **Persistent Storage**: Separate PVCs for data, extensions, and logs
- ✅ **Auto-Route**: OpenShift route with TLS termination
- ✅ **Security**: Non-root containers with minimal privileges
- ✅ **Production Ready**: Resource limits and comprehensive health checks

## Quick Start

### Basic Installation
```bash
helm install sonarqube charts/setup-platform-sonarqube \
  --namespace sonarqube --create-namespace
```

### With Custom Storage
```bash
helm install sonarqube charts/setup-platform-sonarqube \
  --namespace sonarqube --create-namespace \
  --set persistence.data.size=20Gi \
  --set persistence.data.storageClass=gp3 \
  --set postgresql.primary.persistence.size=50Gi
```

### With Custom Admin Password
```bash
helm install sonarqube charts/setup-platform-sonarqube \
  --namespace sonarqube --create-namespace \
  --set sonarqube.defaultAdminPassword="MySecurePassword123"
```

## Configuration

### Database Configuration

By default, the chart includes PostgreSQL:

```yaml
postgresql:
  enabled: true
  auth:
    username: "sonarqube"
    password: "sonarqube"
    database: "sonarqube"
  primary:
    persistence:
      enabled: true
      size: 20Gi
```

### Storage Configuration

SonarQube uses three separate storage volumes:

```yaml
persistence:
  enabled: true
  data:
    size: "10Gi"        # SonarQube data
    storageClass: "gp3"
  extensions:
    size: "5Gi"         # Plugins and extensions
    storageClass: "gp3"
  logs:
    size: "5Gi"         # Application logs
    storageClass: "gp3"
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
sonarqube:
  jvm:
    options: "-Xmx4G -Xms1G -XX:+HeapDumpOnOutOfMemoryError"
```

## Access

After deployment, SonarQube will be available at:
- **OpenShift**: Automatic route creation with TLS
- **Kubernetes**: Configure ingress in values.yaml

Default credentials:
- **Username**: `admin`
- **Password**: Value from `sonarqube.defaultAdminPassword` (default: `admin`)

**⚠️ Important**: Change the admin password after first login!

## Code Analysis

SonarQube supports analysis for:
- **Java**: Maven, Gradle projects
- **JavaScript/TypeScript**: Node.js projects
- **C#**: .NET projects
- **Python**: Python projects
- **Go**: Go projects
- **PHP**: PHP projects
- **And many more languages**

## Security

- Non-root containers
- OpenShift SCC compliant
- TLS encryption for web interface
- Secure database connections
- Minimal container capabilities

## Monitoring

Optional Prometheus metrics:

```yaml
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s
    path: /api/monitoring/metrics
```

## Plugins

Install additional plugins:

```yaml
plugins:
  install:
    - "https://github.com/dependency-check/dependency-check-sonar-plugin/releases/download/3.0.1/sonar-dependency-check-plugin-3.0.1.jar"
    - "https://github.com/checkstyle/sonar-checkstyle/releases/download/10.12.1/checkstyle-sonar-plugin-10.12.1.jar"
```

## External Database

To use external PostgreSQL:

```yaml
postgresql:
  enabled: false

sonarqube:
  jdbc:
    url: "jdbc:postgresql://external-postgres:5432/sonarqube"
    username: "sonarqube"
    password: "your-password"
```

## High Availability

For production environments with multiple replicas:

```yaml
replicaCount: 2
postgresql:
  architecture: replication
  primary:
    persistence:
      size: 100Gi
  readReplicas:
    replicaCount: 1
```