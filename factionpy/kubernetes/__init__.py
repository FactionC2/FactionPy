import base64
from factionpy.logger import log
from kubernetes import client, config

KUBERNETES_NAMESPACE = 'factionc2'

config.load_kube_config()

v1 = client.CoreV1Api()
v1b = client.ExtensionsV1beta1Api()


def get_ingress_host():
    result = v1b.read_namespaced_ingress('faction-ingress', KUBERNETES_NAMESPACE)
    return result.spec.rules[0].host


def get_secret(secret, data_name):
    result = v1.read_namespaced_secret(secret, KUBERNETES_NAMESPACE)
    try:
        return base64.b64decode(result.data[data_name]).decode('utf-8')
    except Exception as e:
        log('factionpy', f"Could not get secret named {data_name} from {secret}. Error: {e}", "error")


