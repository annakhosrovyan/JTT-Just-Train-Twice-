import rich.syntax
import rich.tree

from typing import Sequence
from omegaconf import DictConfig, OmegaConf


def print_configs(
        config: DictConfig,
        fields: Sequence[str],
        resolve: bool = True,
) -> None:
    """Prints content of DictConfig using Rich library and its tree structure.
    Args:
        config (DictConfig): Configuration composed by Hydra.
        fields (Sequence[str]): Determines which main fields from config will be printed and in what order.
        resolve (bool, optional): Whether to resolve reference fields of DictConfig.
    """

    style = "green bold"
    tree = rich.tree.Tree("CONFIG", style=style, guide_style=style)

    for field in fields:
        branch = tree.add(field, style=style, guide_style=style)

        config_section = config.get(field)
        branch_content = str(config_section)
        if isinstance(config_section, DictConfig):
            branch_content = OmegaConf.to_yaml(config_section, resolve=resolve)

        branch.add(rich.syntax.Syntax(branch_content, "yaml"))

    rich.print(tree)

    with open("config_tree.txt", "w") as fp:
        rich.print(tree, file=fp)

    OmegaConf.save(config, "config_tree.yaml")
