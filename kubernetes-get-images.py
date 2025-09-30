#!/usr/bin/env python3

import argparse

from colorama import Fore, Style
from kubernetes import client, config
from kubernetes.client import V1Pod
from tabulate import tabulate

config.load_kube_config()
v1 = client.CoreV1Api()
parser = argparse.ArgumentParser(
    description="Filter pods and their respective images from all namespaces on Kubernetes",
    prog="kubernetes-get-images.py"
)
parser.add_argument("-n", "--namespace", help="Filter pods and images from a specific namespace")

TABLE_HEADERS = [
    f"{Fore.CYAN}{Style.BRIGHT}Pods{Style.RESET_ALL}",
    f"{Fore.MAGENTA}{Style.BRIGHT}Images{Style.RESET_ALL}"
]

def get_pods_all_namespaces() -> list:
    return v1.list_pod_for_all_namespaces().items


def get_pods_from_namespace(namespace: str) -> list:
    return v1.list_namespaced_pod(namespace).items


def get_images_from_pod(pod: V1Pod) -> list:
    return [ container.image for container in pod.spec.containers ]


def add_to_table(pod: str, images: str, table: list):
    table.append([pod, images])


def list_to_comma_string(images: list) -> str:
    return ', '.join(images)


def str_to_cyan(text: str) -> str:
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def str_to_magenta(text: str) -> str:
    return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"


def main():
    args = parser.parse_args()
    table = []
    if args.namespace is None:
        pods = get_pods_all_namespaces()
    else:
        pods = get_pods_from_namespace(args.namespace)

    for pod in pods:
        images = list_to_comma_string(get_images_from_pod(pod))
        add_to_table(
            str_to_cyan(pod.metadata.name),
            str_to_magenta(images),
            table
        )
    print(tabulate(table, headers=TABLE_HEADERS, tablefmt="grid"))


if __name__ == '__main__':
    main()