import src.MacularScriptLauncher as msl
import sys

if __name__ == '__main__':
    # DEFAULT PARAMS TO CHANGE BETWEEN DIRECTORY OR FILE
    launcher = msl.MacularScriptLauncher(sys.argv[1])
    launcher.multiple_runs()