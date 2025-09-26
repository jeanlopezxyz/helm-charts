# Sealed Secrets Setup

This Helm chart installs the Sealed Secrets controller for secure secret management in Kubernetes/OpenShift.

## Overview

Sealed Secrets encrypts Kubernetes secrets that can be safely stored in Git repositories. Only the controller in the cluster can decrypt them.

## Features

- ✅ Automatic controller installation
- ✅ CRD creation for SealedSecrets
- ✅ RBAC configuration
- ✅ Metrics endpoint for Prometheus
- ✅ Automatic key rotation
- ✅ Health monitoring
- ✅ Network policies support

## Prerequisites

- Kubernetes 1.19+ or OpenShift 4.x
- Helm 3.x
- kubectl or oc CLI

## Installation

### Basic Installation

```bash
helm install sealed-secrets jeanlopezxyz/setup-sealed-secrets
```

### Custom Installation

```bash
helm install sealed-secrets jeanlopezxyz/setup-sealed-secrets \
  --namespace sealed-secrets \
  --create-namespace \
  --set sealedSecrets.controller.replicas=2
```

## Usage

### 1. Install kubeseal CLI

```bash
# Download kubeseal
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.5/kubeseal-0.24.5-linux-amd64.tar.gz
tar -xvzf kubeseal-0.24.5-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

### 2. Create a Secret

```bash
# Create a regular secret
kubectl create secret generic mysecret \
  --from-literal=username=admin \
  --from-literal=password=secretpassword \
  --dry-run=client \
  -o yaml > mysecret.yaml
```

### 3. Seal the Secret

```bash
# Seal the secret
kubeseal --format yaml < mysecret.yaml > mysealedsecret.yaml

# Or with specific controller namespace
kubeseal \
  --controller-namespace sealed-secrets \
  --controller-name sealed-secrets-controller \
  --format yaml < mysecret.yaml > mysealedsecret.yaml
```

### 4. Apply Sealed Secret

```bash
# Apply the sealed secret
kubectl apply -f mysealedsecret.yaml

# The controller will automatically create the decrypted secret
kubectl get secrets
```

## Configuration Examples

### High Availability Setup

```yaml
sealedSecrets:
  controller:
    replicas: 3
  advanced:
    podDisruptionBudget:
      enabled: true
      minAvailable: 1
```

### Enable Metrics

```yaml
sealedSecrets:
  metrics:
    enabled: true
    service:
      annotations:
        prometheus.io/scrape: "true"
```

### Custom Resource Limits

```yaml
sealedSecrets:
  controller:
    resources:
      requests:
        memory: "256Mi"
        cpu: "200m"
      limits:
        memory: "1Gi"
        cpu: "1000m"
```

### Network Policy

```yaml
sealedSecrets:
  networkPolicy:
    enabled: true
    ingress:
      - from:
        - namespaceSelector:
            matchLabels:
              name: my-namespace
```

## Advanced Usage

### Scope Configuration

Sealed Secrets can be scoped in three ways:

1. **strict** (default): Secret can only be unsealed in the same namespace/name
2. **namespace-wide**: Secret can be unsealed in the same namespace with any name
3. **cluster-wide**: Secret can be unsealed in any namespace

```bash
# Namespace-wide scope
kubeseal --scope namespace-wide < secret.yaml > sealed-secret.yaml

# Cluster-wide scope
kubeseal --scope cluster-wide < secret.yaml > sealed-secret.yaml
```

### Key Rotation

Keys are automatically rotated based on configuration:

```yaml
sealedSecrets:
  keyRotation:
    enabled: true
    schedule: "0 0 * * 0"  # Weekly
```

### Backup Master Key

```bash
# Backup the master key
kubectl get secret -n sealed-secrets -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml > master-key-backup.yaml

# Restore master key
kubectl apply -f master-key-backup.yaml
```

### Using with GitOps

Example for ArgoCD:

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  encryptedData:
    username: AgBv2p6B...
    password: AgCdMp8x...
```

## Troubleshooting

### Check Controller Status

```bash
# Check pod status
kubectl get pods -n sealed-secrets

# Check logs
kubectl logs -n sealed-secrets deployment/sealed-secrets-controller

# Check events
kubectl get events -n sealed-secrets
```

### Verify Encryption

```bash
# Get public key
kubeseal --fetch-cert \
  --controller-namespace sealed-secrets \
  --controller-name sealed-secrets-controller

# Test encryption
echo -n mypassword | kubeseal --raw \
  --controller-namespace sealed-secrets \
  --controller-name sealed-secrets-controller \
  --scope strict
```

### Common Issues

1. **Cannot decrypt secret**: Check if the controller has the correct private key
2. **Secret not created**: Verify the SealedSecret is in the correct namespace
3. **kubeseal connection refused**: Check service is running and accessible

## Monitoring

### Prometheus Metrics

Available metrics at `/metrics` endpoint:

- `sealed_secrets_unseal_requests_total`
- `sealed_secrets_unseal_errors_total`
- `sealed_secrets_key_rotation_errors_total`
- `controller_runtime_reconcile_total`
- `controller_runtime_reconcile_errors_total`

### Grafana Dashboard

Import dashboard ID: `14995` for Sealed Secrets monitoring

## Security Considerations

- Never commit unsealed secrets to Git
- Regularly rotate encryption keys
- Use RBAC to limit access to SealedSecrets
- Monitor for decryption failures
- Backup master keys securely

## Values Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `sealedSecrets.namespace.name` | Namespace for controller | `sealed-secrets` |
| `sealedSecrets.controller.replicas` | Number of replicas | `1` |
| `sealedSecrets.controller.logLevel` | Log level | `info` |
| `sealedSecrets.metrics.enabled` | Enable metrics | `true` |
| `sealedSecrets.keyRotation.enabled` | Enable key rotation | `true` |

## License

Apache 2.0

## Support

- GitHub: https://github.com/jeanlopezxyz/helm-charts
- Sealed Secrets: https://github.com/bitnami-labs/sealed-secrets