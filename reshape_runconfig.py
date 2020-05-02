import argparse
import pandas as pd
import numpy as np

# argument configuration
parser = argparse.ArgumentParser(description='reshape run conditions')
parser.add_argument('-d','--date',help='Analysis Date')
args=parser.parse_args()



abspath_condition = '/Users/ssakurai/Research/Backup/MAGIC/DataConditionCSV/1ES1959+650'
convdate = args.date[0:4]+"_"+args.date[4:6]+"_"+args.date[6:8]

parameters = ['Runnumber','Trans9km','Trans6km','Trans3km',
              'Humidity','Cloudiness','NumStars',
              'CurZd','NomZd',
              'MeanHV','MeanDC','MedDC']

def main():
    datalist = pd.read_csv(abspath_condition+'/'+convdate+'_check_quality_1ES1959+650_moon.csv')
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

    print(tmp_values)

    item = []
    for i in range(dataset.shape[0]):
        item = dataset.iloc[i]['Name']
        value = dataset.iloc[i][' Value']
        if(item=="Runnumber"):
            if(priv_runnumber!=value):
                runnums.append(priv_runnumber)
                for i_key in parameters:
                    if (len(tmp_values[i_key]) != 0):
                        min_values[i_key].append(np.min(tmp_values[i_key]))
                        max_values[i_key].append(np.max(tmp_values[i_key]))
                        mean_values[i_key].append(np.mean(tmp_values[i_key]))
                    else:
                        min_values[i_key].append(0)
                        max_values[i_key].append(0)
                        mean_values[i_key].append(0)

                priv_runnumber=value

                for i_param in parameters:
                    tmp_values[i_param] = []

            else:
                continue
        tmp_values[item].append(value)
    for i_key in parameters:
        if (len(tmp_values[i_key]) != 0):
            min_values[i_key].append(np.min(tmp_values[i_key]))
            max_values[i_key].append(np.max(tmp_values[i_key]))
            mean_values[i_key].append(np.mean(tmp_values[i_key]))
        else:
            min_values[i_key].append(0)
            max_values[i_key].append(0)
            mean_values[i_key].append(0)
    runnums.append(priv_runnumber)
    
    print(runnums)
    print(mean_values['MeanHV'])
    print(mean_values['MedDC'])
    for i in range(len(runnums)):

        # HV check
        if (mean_values['MeanHV'][i] >= 900):
            hvflag='Nominal'
        else :
            hvflag='Reduced'

            # NSB check
        if (hvflag=='Nominal'):
            if(mean_values['MedDC'][i] < 2.2):
                dcflag='NSB1-2'
            elif (mean_values['MedDC'][i] >= 2.2 and mean_values['MedDC'][i] < 3.3):
                dcflag='NSB2-3'
            elif (mean_values['MedDC'][i] >= 3.3 and mean_values['MedDC'][i] < 5.5):
                dcflag='NSB3-5'
            elif (mean_values['MedDC'][i] >= 5.5 and mean_values['MedDC'][i] < 8.8):
                dcflag='NSB5-8'
            elif (mean_values['MedDC'][i] >= 8.8 and mean_values['MedDC'][i] < 13.2):
                dcflag='NSB8-12'
            else:
                dcflag='TooBlight'
        else:
            if(mean_values['MedDC'][i] < 3.2):
                dcflag='TooDark'
            elif (mean_values['MedDC'][i] >= 3.2 and meanmeddcs[i] < 5.2):
                dcflag='NSBr5-8'
            elif (mean_values['MedDC'][i] >= 5.2 and meanmeddcs[i] < 7.8):
                dcflag='NSBr8-12'
            elif (mean_values['MedDC'][i] >= 7.8 and meanmeddcs[i] < 11.6):
                dcflag='NSBr12-18'
            else:
                dcflag='TooBlight'


        # Zd Check
        if (max_values['CurZd'][i] <= 62):
            zdvalue=''
        else:
            zdvalue='Zd > 62'

        #clouf Check
        if (max_values['Cloudiness'][i] <= 35):
            cdvalue=''
        else:
            cdvalue='Cloud > 35'

        print('| {:s} || {:.0f} || {:.1f} || {:.1f} || {:.1f} || {:s} || {:s} || {:.1f} || {:.1f} || {:s} || {:.2f} || {:.2f} || {:.2f} || {:.1f} || {:s} || {:.1f} || {:.1f}'.format(
            args.date,
            runnums[i],#minmeddcs[i],maxmeddcs[i],meanmeddcs[i],dcflag,hvflag,
            min_values['MedDC'][i],max_values['MedDC'][i],mean_values['MedDC'][i],dcflag,hvflag,
            #minnzds[i],maxnzds[i],zdvalue,
            min_values['NomZd'][i],max_values['NomZd'][i],zdvalue,
            #meantrans3[i],meantrans6[i],meantrans9[i],
            mean_values['Trans3km'][i],mean_values['Trans6km'][i],mean_values['Trans9km'][i],
            #meanclouds[i],cdvalue,meanhumis[i],meannstars[i]))
            mean_values['Cloudiness'][i],cdvalue,mean_values['Humidity'][i],mean_values['NumStars'][i]))
        print('|-')

if __name__ == "__main__":
    main()
