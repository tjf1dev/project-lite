from parser import command
from logger import logger
from main import __version__


@command(
    name="projectlite",
    aliases=["project.lite", "plite", "project-lite", "pl", "info"],
    description="shows information about project.lite",
)
def projectlite():
    logger.info(f"project-lite v{__version__}")
