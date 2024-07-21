class SlashCommandError(Exception):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self) -> str:
        return self.detail


class NotAdministrator(SlashCommandError):
    def __init__(self):
        super().__init__("You must be a guild administrator to run this command.")


class NotRunFromChannel(SlashCommandError):
    def __init__(self):
        super().__init__("This command must be run from a channel.")


class NotRunFromGuild(SlashCommandError):
    def __init__(self):
        super().__init__("This command must be run from within a guild.")
