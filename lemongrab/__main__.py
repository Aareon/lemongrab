from .utils import distro, mem, motherboard, kernel, node, packages, screen, shell, uptime
import os

def get_colors(distro):
    white = "\033[1;37;49m"
    blue = "\033[0;34;49m"
    red = "\033[0;31;49m"
    light_red = "\033[1;31;49m"
    green = "\033[0;32;49m"
    yellow = "\033[1;33;49m"
    lime = "\033[1;32;49m"
    light_blue = "\033[1;34;49m"
    dark_grey = "\033[1;30;49m"
    cyan = "\033[1;36;49m"

    bold = "\033[1m"
    reset = "\033[0m"

    specs_colors = {"arch": cyan,
                    "debian": light_red,
                    "elementary": dark_grey,
                    "fedora": light_blue,
                    "mint": lime,
                    "ubuntu": light_red,
                    "windows$10": light_red,
                    "windows$8": light_red,
                    "windows7": green}

    dist_colors = {"arch":(bold+cyan, cyan, reset),
                   "debian": (bold+white, light_red),
                   "elementary": (bold+white,),
                   "fedora": (bold+light_blue, white),
                   "linux": (dark_grey, white, yellow),
                   "mint": (bold+lime, bold+white),
                   "ubuntu": (light_red, white, yellow),
                   "windows$10": (blue,),
                   "windows$8": (blue,),
                   "windows$7": (red, green, blue, yellow)}
    return specs_colors.get(distro, red), dist_colors.get(distro, (white,)), reset

def main(logofp=distro.distro_txt().lower(), color=True):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]

    if color:
        specs_color, dist_colors, reset = get_colors(logofp)
    else:
        specs_color, dist_colors, reset = "", ("",), ""
    specs = []

    username, host = node.node()
    specs.append("{}{}{}@{}{}".format(specs_color, username, reset, specs_color, host))
    specs.append("{}OS:{} {}".format(specs_color, reset, distro.distro()))
    specs.append("{}Kernel:{} {} {} {}".format(specs_color, reset, *kernel.kernel()))
    specs.append("{}Uptime:{} {}".format(specs_color, reset, uptime.uptime()))
    specs.append("{}Packages:{} {}".format(specs_color, reset, packages.packages()))
    specs.append("{}Shell:{} {}".format(specs_color, reset, shell.shell()))
    specs.append("{}HDD:{} {} / {} (Free/Total)".format(specs_color, reset, *mem.hdd()))
    specs.append("{}CPU:{} {}".format(specs_color, reset, "TBA"))
    specs.append("{}RAM:{} {} / {} (Used/Total)".format(specs_color, reset, *mem.ram()))
    resolution = screen.screen()
    if resolution:
        specs.append("{}Resolution:{} {}".format(specs_color, reset, resolution))
    specs.append("{}Motherboard:{} {} {}".format(specs_color, reset, *motherboard.motherboard()))

    with open("{}/logos/{}".format(script_dir, logofp)) as logo:
        logo = logo.read()
        colored_logo = logo.format(*dist_colors)
    
    logo_lines = len(colored_logo)
    while len(specs) < logo_lines:
        specs.append("")
    finished_logo = "".join(l+i+"\n" for i, l in zip(specs, colored_logo.split("\n")))
    print(finished_logo)
    


if __name__ == "__main__":
    main(logofp="debian")
