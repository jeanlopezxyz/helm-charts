#!/bin/bash

# Variables
CHART_DESTINATION="/opt/helm-charts"  # Directorio temporal para empaquetar charts
NGINX_HELM_DIR="/var/www/html/helm-charts"  # Directorio expuesto por Nginx

# Array de charts con sus rutas
CHARTS=(
    # "/opt/helm-charts/helper-operator"
    # "/opt/helm-charts/helper-status-checker"
    # "/opt/helm-charts/etcd-backup"
    # "/opt/helm-charts/etcd-defrag"
    "/opt/helm-charts/gitea-setup"
)

# Empaquetar y copiar cada chart
for CHART_PATH in "${CHARTS[@]}"; do
    if [ ! -d "$CHART_PATH" ]; then
        echo "Error: El directorio $CHART_PATH no existe. Saltando este chart."
        continue
    fi

    CHART_NAME=$(basename "$CHART_PATH")
    
    # Actualizar dependencias
    helm dependency update "$CHART_PATH" || {
        echo "Error: Falló la actualización de dependencias para $CHART_NAME"
        continue
    }
    
    # Empaquetar el chart
    helm package "$CHART_PATH" --destination "$CHART_DESTINATION" || {
        echo "Error: Falló el empaquetado del chart $CHART_NAME"
        continue
    }
    
    # Copiar el archivo empaquetado al directorio de Nginx
    CHART_TGZ="$CHART_DESTINATION/$CHART_NAME-*.tgz"
    if ls $CHART_TGZ 1> /dev/null 2>&1; then
        cp $CHART_TGZ "$NGINX_HELM_DIR" || {
            echo "Error: Falló al copiar $CHART_NAME a $NGINX_HELM_DIR"
            continue
        }
        echo "El archivo $CHART_TGZ se copió exitosamente a $NGINX_HELM_DIR"
    else
        echo "Error: No se encontró el archivo empaquetado para $CHART_NAME"
        continue
    fi
done

# Actualizar el índice del repositorio de Helm
helm repo index "$NGINX_HELM_DIR" --url "https://helm1.labjp.xyz:8443/helm-charts" || {
    echo "Error: Falló la actualización del índice del repositorio en $NGINX_HELM_DIR"
    exit 1
}

echo "Proceso completado. Los charts están disponibles en el directorio $NGINX_HELM_DIR."
