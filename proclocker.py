import sys
import psutil

def check_arguments():
    if len(sys.argv) == 1:
        print('Este programa no funciona sin argumentos')
        sys.exit(0)

def get_targets():

    targets = sys.argv[1:]

    i = 0
    while i < len(targets):
        if not targets[i].endswith('.exe'):
            targets[i] = targets[i] + '.exe'
        i += 1
    return target

def lock(target):
    for proc in psutil.process_iter():
    	if proc.name().lower() == target.lower():
    		proc.kill()


if __name__ == '__main__':

    check_arguments()
    targets = get_targets()

    while True:
    	for target in targets:
    		lock(target)