from bvolt.infrastructure.lifecycle import ApplicationLifecycle


def main() -> None:
    """
    Application entrypoint.
    """
    lifecycle = ApplicationLifecycle()
    lifecycle.start()
