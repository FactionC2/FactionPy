import base64
from factionpy.logger import log
from kubernetes import client, config

KUBERNETES_NAMESPACE = 'factionc2'
CONNECTED_TO_KUBERNETES = False

try:
    config.load_kube_config()
    v1 = client.CoreV1Api()
    v1b = client.ExtensionsV1beta1Api()
    CONNECTED_TO_KUBERNETES = True
except Exception as e:
    log(f"Could not create Kubernetes clients. This may not be a big deal or it might be. Error: {e}",
        "warning")


def get_ingress_host():
    if CONNECTED_TO_KUBERNETES:
        result = v1b.read_namespaced_ingress('faction-ingress', KUBERNETES_NAMESPACE)
        return result.spec.rules[0].host
    return None


def get_secret(secret, data_name):
    if CONNECTED_TO_KUBERNETES:
        result = v1.read_namespaced_secret(secret, KUBERNETES_NAMESPACE)
        try:
            return base64.b64decode(result.data[data_name]).decode('utf-8')
        except Exception as e:
            log(f"Error retrieving secret: {e}", "error")
    return None

