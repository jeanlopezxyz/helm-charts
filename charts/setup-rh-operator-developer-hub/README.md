# Red Hat Developer Hub (Backstage) Operator Setup

This Helm chart installs and configures Red Hat Developer Hub (RHDH) with support for dynamic plugins.

## Features

- ✅ Automatic operator installation
- ✅ Backstage CR creation with full configuration
- ✅ Dynamic plugins support
- ✅ ConfigMap-based plugin management
- ✅ Integration with GitHub, ArgoCD, Kubernetes
- ✅ Health monitoring via status checker

## Prerequisites

- OpenShift 4.12+ cluster
- Helm 3.x installed
- Cluster admin permissions

## Quick Start

### 1. Install the Chart

```bash
helm install rhdh jeanlopezxyz/setup-rh-operator-developer-hub
```

### 2. Create Secrets

```bash
kubectl create secret generic rhdh-secrets \
  --from-literal=GITHUB_TOKEN=ghp_xxxxxxxxxxxx \
  --from-literal=GITHUB_ORG=myorganization \
  -n rhdh
```

## Architecture

When installed, the following components are created:

- **PostgreSQL Database** (embedded or external)
- **Backstage Pod** with Frontend and Backend
- **Dynamic Plugin Loader**
- **ConfigMaps** for configuration
- **Route** for external access

## Configuration Examples

### Basic Configuration

```yaml
# values-custom.yaml
backstage:
  namespace:
    name: rhdh
  instance:
    enabled: true
    name: developer-hub
  route:
    enabled: true
    host: developer-hub.apps.mycluster.com
```

### External Database

```yaml
backstage:
  database:
    enableLocalDb: false
    authSecretName: postgresql-secret
```

### High Availability

```yaml
backstage:
  replicas: 3
  database:
    enableLocalDb: false
```

## Plugin Installation

### Method 1: Dynamic Plugins (Recommended)

```yaml
backstage:
  dynamicPlugins:
    enabled: true
    plugins:
      - package: './dynamic-plugins/dist/backstage-plugin-kubernetes-backend-dynamic'
        disabled: false
```

### Method 2: NPM Registry

```yaml
backstage:
  dynamicPlugins:
    plugins:
      - package: '@roadiehq/backstage-plugin-github-pull-requests'
        disabled: false
```

### Method 3: Direct URL

```yaml
backstage:
  dynamicPlugins:
    plugins:
      - package: 'https://github.com/org/plugin/releases/download/v1.0.0/plugin.tgz'
        disabled: false
```

## Microservices Documentation

### Adding a Service to the Catalog

Create `catalog-info.yaml` in your microservice repository:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Payment processing microservice
  annotations:
    github.com/project-slug: myorg/payment-service
    backstage.io/kubernetes-id: payment-service
    backstage.io/techdocs-ref: dir:.
  tags:
    - java
    - spring-boot
spec:
  type: service
  lifecycle: production
  owner: team-payments
  system: payment-platform
  providesApis:
    - payment-api-v1
```

### Auto-Discovery Configuration

```yaml
backstage:
  appConfig:
    catalog:
      locations:
        - type: github-discovery
          target: https://github.com/myorg/*/blob/main/catalog-info.yaml
      providers:
        github:
          myorg:
            organization: 'myorg'
            catalogPath: '/catalog-info.yaml'
            schedule:
              frequency: { minutes: 30 }
```

### TechDocs Setup

Create `mkdocs.yml` in your repository:

```yaml
site_name: Payment Service Documentation
site_description: Complete documentation

nav:
  - Home: index.md
  - API Reference: api.md
  - Architecture: architecture.md

plugins:
  - techdocs-core
```

## Creating Custom Plugins

### 1. Generate Plugin

```bash
npx @backstage/create-app@latest
cd my-backstage-app
yarn new --select plugin
```

### 2. Build as Dynamic Plugin

```bash
cd plugins/my-custom-plugin
yarn install
yarn tsc
yarn build
yarn export-dynamic
npm pack
```

### 3. Deploy Plugin

Add to `values.yaml`:

```yaml
backstage:
  dynamicPlugins:
    plugins:
      - package: '@mycompany/backstage-plugin-custom'
        disabled: false
        pluginConfig:
          myCustomPlugin:
            apiUrl: ${CUSTOM_API_URL}
```

## Complete Deployment Script

```bash
#!/bin/bash

# Create namespace
kubectl create namespace rhdh

# Create secrets
kubectl create secret generic rhdh-secrets \
  --from-literal=BACKEND_SECRET=$(openssl rand -base64 32) \
  --from-literal=GITHUB_TOKEN=ghp_xxxxxxxxxxxx \
  --from-literal=GITHUB_ORG=myorganization \
  -n rhdh

# Install chart
helm install rhdh jeanlopezxyz/setup-rh-operator-developer-hub \
  --namespace rhdh \
  --set backstage.route.host=developer-hub.apps.mycluster.com

# Wait for deployment
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=backstage \
  -n rhdh \
  --timeout=300s

# Get URL
echo "URL: https://$(kubectl get route developer-hub -n rhdh -o jsonpath='{.spec.host}')"
```

## Available Plugins

### Enabled by Default
- GitHub Catalog Backend
- Kubernetes Backend
- TechDocs Backend
- ArgoCD Plugin

### Disabled by Default (Configurable)
- Jira (requires JIRA_URL, JIRA_TOKEN)
- SonarQube (requires SONARQUBE_URL, SONARQUBE_TOKEN)
- Jenkins (requires JENKINS_URL, JENKINS_API_KEY)
- GitLab (requires GITLAB_HOST, GITLAB_TOKEN)
- Prometheus (requires PROMETHEUS_URL)

## Troubleshooting

### Check Plugin Status

```bash
# List loaded plugins
curl https://developer-hub.apps.mycluster.com/api/dynamic-plugins-info/loaded-plugins

# Check logs
kubectl logs -n rhdh deployment/developer-hub-backstage

# Restart to reload configuration
kubectl rollout restart deployment/developer-hub-backstage -n rhdh
```

### Common Issues

1. **Plugin not loading**: Verify `disabled: false`
2. **Authentication errors**: Check secret values
3. **Database connection**: Verify PostgreSQL is running

## Values Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backstage.namespace.name` | Namespace for Backstage | `rhdh` |
| `backstage.instance.enabled` | Create Backstage instance | `true` |
| `backstage.replicas` | Number of replicas | `1` |
| `backstage.database.enableLocalDb` | Use embedded database | `true` |
| `backstage.dynamicPlugins.enabled` | Enable dynamic plugins | `true` |

## License

MIT

## Support

- GitHub Issues: https://github.com/jeanlopezxyz/helm-charts/issues
- Red Hat Documentation: https://docs.redhat.com/en/documentation/red_hat_developer_hub