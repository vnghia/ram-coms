import docker

import utils


def get_mem_usage(container: docker.client.ContainerCollection) -> float:
    return utils.byte_to_mb(
        container.stats(stream=False)["memory_stats"].get("usage", 0)
    )


def monitor_mem_usage(
    client: docker.client.DockerClient,
    base_image: str,
    command: str,
    save_progress: bool = False,
) -> float | tuple[float, list[float]]:
    container: docker.client.DockerClient = client.containers.run(
        base_image, command, detach=True
    )

    max_usage = 0.0
    current_usage = 1.0
    mem_usages = []

    # The memory usage reaches 0 if the container is exited.
    while current_usage:
        current_usage = get_mem_usage(container)
        max_usage = max(max_usage, current_usage)
        if save_progress:
            mem_usages.append(current_usage)

    container.remove()

    if save_progress:
        return max_usage, mem_usages
    else:
        return max_usage
