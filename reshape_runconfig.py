import argparse
import pandas as pd
import numpy as np
import logging
import os
import sys

# argument configuration
parser = argparse.ArgumentParser(description='reshape run conditions')
parser.add_argument('-d','--date',help='Analysis Date')
parser.add_argument('-f','--format',help='Output format',default='wiki')
parser.add_argument('-o','--output',help='Output filename',default='runconfig.txt')
args=parser.parse_args()

# logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# config for stdstream
sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)
sh_formatter = logging.Formatter(
    fmt='%(message)s',
    datefmt='%m/%d %H:%M:%S')
sh.setFormatter(sh_formatter)
logger.addHandler(sh)

# file path
abspath_condition = '/Users/ssakurai/Research/Backup/MAGIC/DataConditionCSV/1ES1959+650'
convdate = args.date[0:4]+"_"+args.date[4:6]+"_"+args.date[6:8]

parameters = ['Runnumber','Trans9km','Trans6km','Trans3km',
              'Humidity','Cloudiness','NumStars',
              'CurZd','NomZd',
              'MeanHV','MeanDC','MedDC']

def output_for_wiki(outfile,date,runnum,dc_flag,hv_flag,meanmeddc,minzd,maxzd,meanT3k,meanT6k,meanT9k):
    outfile.write('| {0:s} || {1:.0f} || {4:.1f} || {2:s} || {3:s} || {5:.1f} || {6:.1f} || {7:.2f} || {8:.2f} || {9:.2f} ||\n'.format(date, runnum, dc_flag, hv_flag, meanmeddc, minzd, maxzd, meanT3k, meanT6k, meanT9k))
    outfile.write('|-\n')

def output_for_tex(outfile,date,runnum,dc_flag,hv_flag,meanmeddc,minzd,maxzd,meanT3k,meanT6k,meanT9k):
    outfile.write('{0:s} & {1:.0f} & {4:.1f} & {2:s} & {3:s} & {5:.1f} & {6:.1f} & {7:.2f} & {8:.2f} & {9:.2f} \\\\\n'.format(date, runnum, dc_flag, hv_flag, meanmeddc, minzd, maxzd, meanT3k, meanT6k, meanT9k))

def footer_for_tex(outfile):
    outfile.write('\\end{tabular}\n')
    outfile.write('\\end{table}\n')

def header_for_tex(outfile):
    outfile.write('\\begin{table}[H]\n')
    outfile.write('\\begin{tabular}{llrrrrrrrr}\n')
    outfile.write('Date & Run Number & MedDC aved in run & NSB Level & HV & Min Zd & Max Zd & Trans3km & Trans6km & Trans9km \\\\\n')


def footer_for_wiki(outfile):
    outfile.write('| || || || || || || || || || ||\n')
    outfile.write('|-\n')

def header_for_wiki(outfile):
    outfile.write('| Date || Run Number || MedDC aved in run || NSB Level || HV || Min Zd || Max Zd || Trans3km || Trans6km || Trans9km ||\n')
    outfile.write('|-')

def main():
    filename = abspath_condition+'/'+convdate+'_check_quality_1ES1959+650_moon.csv'
    if os.path.exists(filename):
        datalist = pd.read_csv(filename)
    else:
        logger.error('FILE DOES NOT EXIST')
        sys.exit()
    dataset = datalist.sort_values(by=datalist.columns[1])
    dataset.set_index(datalist.columns[1],inplace=True)

    # main loop
    priv_runnumber = np.unique(np.sort(dataset.query('Name=="Runnumber"')[datalist.columns[2]]))[0]
    runnums=[]
    tmp_values = {}
    max_values = {}
    min_values = {}
    mean_values = {}
    for i_param in parameters:
        tmp_values[i_param] = []
        max_values[i_param] = []
        min_values[i_param] = []
        mean_values[i_param] = []

    for i_line in range(dataset.shape[0]):
        item = dataset.iloc[i_line][datalist.columns[0]]
        value = dataset.iloc[i_line][datalist.columns[2]]
        if(item == "Runnumber"):
            if(priv_runnumber!=value):
                # mean_values[item].append(priv_runnumber)
                runnums.append(priv_runnumber)
                # calculate mean, max, min for a certain runnumber
                for i_key in parameters[1:]:
                    if (len(tmp_values[i_key]) != 0):
                        min_values[i_key].append(np.min(tmp_values[i_key]))
                        max_values[i_key].append(np.max(tmp_values[i_key]))
                        mean_values[i_key].append(np.mean(tmp_values[i_key]))
                    else:
                        min_values[i_key].append(0)
                        max_values[i_key].append(0)
                        mean_values[i_key].append(0)
                # keep runnumber
                priv_runnumber=value
                # initialize values
                for i_param in parameters:
                    tmp_values[i_param] = []
            else:
                continue
        else:
            #store values
            tmp_values[item].append(value)
    # exceptional handling
    runnums.append(priv_runnumber)
    # mean_values['Runnumber'].append(priv_runnumber)
    for i_key in parameters[1:]:
        if (len(tmp_values[i_key]) != 0):
            min_values[i_key].append(np.min(tmp_values[i_key]))
            max_values[i_key].append(np.max(tmp_values[i_key]))
            mean_values[i_key].append(np.mean(tmp_values[i_key]))
        else:
            min_values[i_key].append(0)
            max_values[i_key].append(0)
            mean_values[i_key].append(0)

    # check observational condition and print it
    out_file = open(args.output,'a')
    if args.format == 'tex':
        header_for_tex(out_file)
    for i_run, number in enumerate(runnums):

        # HV check
        if (mean_values['MeanHV'][i_run] >= 900):
            hvflag='Nominal'
        else :
            hvflag='Reduced'

        # NSB check
        if (hvflag=='Nominal'):
            if(mean_values['MedDC'][i_run] < 2.2):
                dcflag='NSB1-2'
            elif (mean_values['MedDC'][i_run] >= 2.2 and mean_values['MedDC'][i_run] < 3.3):
                dcflag='NSB2-3'
            elif (mean_values['MedDC'][i_run] >= 3.3 and mean_values['MedDC'][i_run] < 5.5):
                dcflag='NSB3-5'
            elif (mean_values['MedDC'][i_run] >= 5.5 and mean_values['MedDC'][i_run] < 8.8):
                dcflag='NSB5-8'
            elif (mean_values['MedDC'][i_run] >= 8.8 and mean_values['MedDC'][i_run] < 13.2):
                dcflag='NSB8-12'
            else:
                dcflag='TooBlight'
        else:
            if(mean_values['MedDC'][i_run] < 3.2):
                dcflag='TooDark'
            elif (mean_values['MedDC'][i_run] >= 3.2 and mean_values['MedDC'][i_run] < 5.2):
                dcflag='NSBr5-8'
            elif (mean_values['MedDC'][i_run] >= 5.2 and mean_values['MedDC'][i_run] < 7.8):
                dcflag='NSBr8-12'
            elif (mean_values['MedDC'][i_run] >= 7.8 and mean_values['MedDC'][i_run] < 11.6):
                dcflag='NSBr12-18'
            else:
                dcflag='TooBlight'

        # Zd Check
        if (max_values['CurZd'][i_run] <= 50):
            zdvalue=''
        else:
            zdvalue='Zd > 50'

        #cloud Check
        if (max_values['Cloudiness'][i_run] <= 35):
            cdvalue=''
        else:
            cdvalue='Cloud > 35'

        # output format
        if args.format == 'wiki':
            output_for_wiki(out_file,args.date,runnums[i_run],dcflag,hvflag,
                            mean_values['MedDC'][i_run],min_values['NomZd'][i_run],max_values['NomZd'][i_run],
                            mean_values['Trans3km'][i_run],mean_values['Trans6km'][i_run],mean_values['Trans9km'][i_run])
        elif args.format == 'tex':
            output_for_tex(out_file,args.date,runnums[i_run],dcflag,hvflag,
                            mean_values['MedDC'][i_run],min_values['NomZd'][i_run],max_values['NomZd'][i_run],
                            mean_values['Trans3km'][i_run],mean_values['Trans6km'][i_run],mean_values['Trans9km'][i_run])
    if args.format == 'wiki':
        footer_for_wiki(out_file)
    elif args.format == 'tex':
        footer_for_tex(out_file)
if __name__ == "__main__":
    main()
