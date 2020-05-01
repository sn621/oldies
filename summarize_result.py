import argparse
import glob

# argument configuration
parser = argparse.ArgumentParser(description='make summary plot')
parser.add_argument('-d','--date',help='Analysis Date')
parser.add_argument('-n','--nsb',help='NSB Levels',type=str,nargs='*')
args=parser.parse_args()

def make_preamble(outfile):
    outfile.write('\\documentclass[a4paper,10pt]{article}\n')
    outfile.write('\\usepackage{graphicx}\n')
    outfile.write('\\usepackage{a4wide}\n')
    outfile.write('\\usepackage{here}\n')

def begin_document(outfile):
    outfile.write('\\begin{document}\n')

def end_document(outfile):
    outfile.write('\\end{document}\n')

def change_section(outfile,title):
    outfile.write('\\section{'+title+'}\n')

def change_subsection(outfile,title):
    outfile.write('\\subsection{'+title+'}\n')

def change_page(outfile):
    outfile.write('\\clearpage\n\n')

def add_figure(out_file,figurepath,caption,label):
    out_file.write('\\begin{figure}[H]\n')
    out_file.write('\\center\n')
    out_file.write('\\includegraphics[width=1.0\\linewidth]{'+figurepath+'}\n')
    out_file.write('\\caption{'+caption+'}\n')
    out_file.write('\\label{'+label+'}\n')
    out_file.write('\\end{figure}\n\n')

def add_figures(out_file,figurepaths,captions,labels):
    width_minip = 1.0/len(figurepaths)
    out_file.write('\\begin{figure}[H]\n')
    for i_fig in range(len(figurepaths)):
        out_file.write('\\begin{minipage}{'+str(width_minip)+'\\hsize}\n')
        out_file.write('\\center\n')
        out_file.write('\\includegraphics[width=1.0\\linewidth]{'+figurepaths[i_fig]+'}\n')
        out_file.write('\\caption{'+captions[i_fig]+'}\n')
        out_file.write('\\label{'+labels[i_fig]+'}\n')
        out_file.write('\\end{minipage}\n')
    out_file.write('\\end{figure}\n\n')

abspath_condition = '/Users/ssakurai/Research/Backup/MAGIC/DataConditionPlot/1ES1959+650'

def main():
    # get filenames
    plotname = glob.glob('{0}/*/{1}_{2}_{3}*_moon.png'.format(abspath_condition,args.date[0:4],args.date[4:6],args.date[6:8]))
    figpath_star = {}
    for i_nsb in args.nsb:
        figpath_star[i_nsb] = [glob.glob('./star_{}_{}_M1*pdf'.format(i_nsb,args.date))[0],glob.glob('./star_{}_{}_M2*pdf'.format(i_nsb,args.date))[0]]
    figpath_odie = {}
    for i_nsb in args.nsb:
        figpath_odie[i_nsb] = [glob.glob('./Output_odie_LE_{}_{}*pdf'.format(i_nsb,args.date))[0],glob.glob('./Output_odie_FR_{}_{}*pdf'.format(i_nsb,args.date))[0]]
    figpath_flute = {}
    for i_nsb in args.nsb:
        figpath_flute[i_nsb] = [glob.glob('./Status_flute_{}_{}*SED.pdf'.format(i_nsb,args.date))[0],glob.glob('./Status_flute_{}_{}*LightCurve.pdf'.format(i_nsb,args.date))[0]]

    # set filenames
    texfile = open('./summary_{0.date}.tex'.format(args),"w")

    # text
    make_preamble(texfile)
    begin_document(texfile)
    # part 1
    change_section(texfile,'Run Conditions')
    texfile.write('Observation Date: {}\\\\\n'.format(args.date))
    texfile.write('NSB Levels: {0}\\\\\n'.format(args.nsb))
    texfile.write('Comments from Run Book\\\\\n')
    texfile.write('Deatail in Fig.\\ref{'+'runplot'+'}\n')
    add_figure(texfile,plotname[0],'Run Condition', 'runplot')
    # part 2
    change_section(texfile,'Image Cleaning')
    for i_nsb in args.nsb:
        change_subsection(texfile,'NSB{}'.format(i_nsb))
        cap_tmp = ['NSB{} M1'.format(i_nsb),'NSB{} M2'.format(i_nsb)]
        lab_tmp = ['star_{}_M1'.format(i_nsb),'star_{}_M2'.format(i_nsb)]
        texfile.write('Fraction of surviving pedestal M1: Fig.\\ref{'+lab_tmp[0]+'} and M2: Fig.\\ref{'+lab_tmp[1]+'}\n')
        add_figures(texfile,figpath_star[i_nsb],cap_tmp,lab_tmp)
    # part 3
    change_section(texfile,'$\\theta^2$ plot')
    for i_nsb in args.nsb:
        change_subsection(texfile,'NSB{}'.format(i_nsb))
        cap_tmp = ['NSB{} LE'.format(i_nsb),'NSB{} FR'.format(i_nsb)]
        lab_tmp = ['odie_{}_LE'.format(i_nsb),'odie_{}_FR'.format(i_nsb)]
        texfile.write('$\\theta^2$ plot in LE: Fig.\\ref{'+lab_tmp[0]+'} and FR: Fig.\\ref{'+lab_tmp[1]+'}\n')
        add_figure(texfile,figpath_odie[i_nsb][0],cap_tmp[0],lab_tmp[0])
        add_figure(texfile,figpath_odie[i_nsb][1],cap_tmp[1],lab_tmp[1])
    # part 4
    change_section(texfile,'SED and Light Curve')
    for i_nsb in args.nsb:
        change_subsection(texfile,'NSB{}'.format(i_nsb))
        cap_tmp = ['NSB{} SED'.format(i_nsb),'NSB{} Light Curve'.format(i_nsb)]
        lab_tmp = ['flute_{}_SED'.format(i_nsb),'flute_{}_LC'.format(i_nsb)]
        texfile.write('SED: Fig.\\ref{'+lab_tmp[0]+'} and Light Curve: Fig.\\ref{'+lab_tmp[1]+'}\n')
        add_figures(texfile,figpath_flute[i_nsb],cap_tmp,lab_tmp)
    end_document(texfile)

    texfile.close()

if __name__ == "__main__":
    main()

# memo
#runprocess(['pdflatex','./tex_{0.nsb}_{0.date}.tex'.format(args)])
#runprocess(['open','./tex_{0.nsb}_{0.date}.pdf'.format(args)])
