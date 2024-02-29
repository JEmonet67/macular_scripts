import src.MacularScriptLauncher as msl
import sys

if __name__ == '__main__':
    # DEFAULT PARAMS TO CHANGE BETWEEN DIRECTORY OR FILE
    try:
        launcher = msl.MacularScriptLauncher(sys.argv[1])
    except IndexError:
        print("No config file given.")
        exit()

    launcher.multiple_runs()