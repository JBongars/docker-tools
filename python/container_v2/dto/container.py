import subprocess


class ContainerDTO:
    image = None
    hostname = None
    build_arguments = []
    run_command = None

    build = lambda self: self
    pre_run = lambda self: self
    run = lambda self: self
    cleanup = lambda self: self.cleanup()
    on_error = lambda self: self.cleanup()
    on_stop = lambda self: self.cleanup()

    SILENCE_MOUNT_RUNNER_WITH_HOOKS_WARNING = False

    def __init__(self):
        self.mount_runner_with_hooks(
            lambda self: subprocess.run(self.run_command, shell=True, check=True)
        )
        return self

    def set_image(self, image):
        self.image = image
        return self

    def set_hostname(self, hostname):
        self.hostname = hostname
        return self

    def set_build_arguments(self, build_arguments):
        self.build_arguments = build_arguments
        return self

    def set_run_command(self, run_command):
        self.run_command = run_command
        return self

    def set_build(self, build):
        self.build = build
        return self

    def set_run(self, run):
        if self.SILENCE_MOUNT_RUNNER_WITH_HOOKS_WARNING == False:
            print(
                "[WARNING]: Hooks are not mounted. Use mount_runner_with_hooks() instead of set_run() to mount hooks."
            )
        self.run = run
        return self

    def mount_runner_with_hooks(self, runnable):
        self.SILENCE_MOUNT_RUNNER_WITH_HOOKS_WARNING = True

        def wrapped_runnable(self):
            # TODO: add logging
            # TODO: add error handling
            # TODO: add cleanup
            return runnable(self)

        self.set_run(wrapped_runnable)
        return self

    def set_cleanup(self, cleanup):
        self.cleanup = cleanup
        return self

    def set_on_error(self, on_error):
        self.on_error = on_error
        return self

    def set_on_stop(self, on_stop):
        self.on_stop = on_stop
        return self

    def get_info(self):
        return {
            "image": self.image,
            "hostname": self.hostname,
            "build_arguments": self.build_arguments,
            "run_command": self.run_command,
        }

    def __str__(self):
        return f"{self.image} {self.hostname} {self.build_arguments} {self.run_command}"
