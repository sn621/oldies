import logging
import argparse
import glob
import termcolor

# argument configuration
parser = argparse.ArgumentParser(description='you can check MAGIC runbook with a certain keyword')
parser.add_argument('-d','--date',help='Analysis Date')
parser.add_argument('-k','--keyword',help='keyword what you wanna find',default='Crab')
args=parser.parse_args()

# logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# config for stdstream
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh_formatter = logging.Formatter(
    fmt='%(message)s',
    datefmt='%m/%d %H:%M:%S')
sh.setFormatter(sh_formatter)
logger.addHandler(sh)

# path configuration
abspath_runbook = '/Users/ssakurai/Research/Backup/MAGIC/RunBook'

def check_red(keyphrase,line):
    if keyphrase in line.lower():
        slice = line.lower().index(keyphrase)
        logger.warning(termcolor.colored('CHECK: ','red')
                    + line[:slice]
                    + termcolor.colored(line[slice:slice+len(keyphrase)],'red')
                    + line[slice+len(keyphrase):])
        return True
    else:
        return False

def check_green(keyphrase,line):
    if keyphrase in line.lower():
        slice = line.lower().index(keyphrase)
        logger.warning(termcolor.colored('CHECK: ','green')
                    + line[:slice]
                    + termcolor.colored(line[slice:slice+len(keyphrase)],'green')
                    + line[slice+len(keyphrase):])
        return True
    else:
        return False

def check_blue(keyphrase,line):
    if keyphrase in line.lower():
        slice = line.lower().index(keyphrase)
        logger.warning(termcolor.colored('CHECK: ','blue')
                    + line[:slice]
                    + termcolor.colored(line[slice:slice+len(keyphrase)],'blue')
                    + line[slice+len(keyphrase):])
        return True
    else:
        return False

def main():
    # get filename
    filename = glob.glob('{0}/*/CC_M1M2_{1}_{2}_{3}*.rbk'.format(abspath_runbook,args.date[0:4],args.date[4:6],args.date[6:8]))
    if not filename:
        filename = glob.glob('{0}/CC_M1_{1}_{2}_{3}*.rbk'.format(abspath_runbook,args.date[0:4],args.date[4:6],args.date[6:8]))
    logger.info('FILE NAME: {}'.format(filename[0]))
    # file reading
    runbook = open(filename[0],'r')
    content = runbook.read()
    lines = content.split('\n')
    # main loop
    for i_line in lines[:-1]:
        if check_green(args.keyword.lower(),i_line):
            pass
        elif check_red('error',i_line):
            pass
        elif check_red('lider',i_line):
            pass
        elif check_red('undefined',i_line):
            pass
        elif check_red('cloud',i_line):
            pass
        elif check_blue('not',i_line):
            pass
        else:
            logger.info(i_line)

if '__main__' == __name__:
    main()
