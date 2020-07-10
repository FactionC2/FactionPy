import base64
from factionpy.logger import log
from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()
v1b = client.ExtensionsV1beta1Api()


def get_ingress_host(namespace="default"):
    result = v1b.read_namespaced_ingress('faction-ingress', namespace)
    return result.spec.rules[0].host


def get_secret(secret, data_name, namespace="default"):
    result = v1.read_namespaced_secret(secret, namespace)
    try:
        return base64.b64decode(result.data[data_name])
    except Exception as e:
        log('factionpy', f"Could not get secret named {data_name} from {secret}. Error: {e}", "error")


