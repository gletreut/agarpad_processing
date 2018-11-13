#################### imports ####################
# standard
import sys
import os
import numpy as np
import yaml
import argparse
import shutil

# custom
import acquisitionlib as acq

#################### global params ####################
# yaml formats
npfloat_representer = lambda dumper,value: dumper.represent_float(float(value))
nparray_representer = lambda dumper,value: dumper.represent_list(value.tolist())
float_representer = lambda dumper,value: dumper.represent_scalar(u'tag:yaml.org,2002:float', "{:<.8e}".format(value))
unicode_representer = lambda dumper,value: dumper.represent_unicode(value.encode('utf-8'))
yaml.add_representer(float,float_representer)
yaml.add_representer(np.float_,npfloat_representer)
yaml.add_representer(np.ndarray,nparray_representer)
yaml.add_representer(unicode,unicode_representer)

#################### function ####################
def default_parameters():
    """Generate a default parameter dictionary."""

    print "Loading default parameters"
    params={}
    # filtering - select only a subset
    params['get_nd2_images_args']={}
    mydict = params['get_nd2_images_args']
    mydict['tstart'] = 0
    mydict['tend'] = 2
    mydict['fovs'] = [0,1,2]
    mydict['colors'] = [0,1]
    mydict['xcrop'] = [0,7]
    mydict['ycrop'] = [0,7]

    return params

#################### main ####################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Read and handle nd2 files.")
    parser.add_argument('ND2',  type=str, help='ND2 file to open.')
    parser.add_argument('-f', '--paramfile',  type=file, required=False, help='Yaml file containing parameters.')
    parser.add_argument('-d', '--outputdir',  type=str, required=False, help='Output directory')
    parser.add_argument('--debug',  action='store_true', required=False, help='Enable debug mode')

    # load arguments
    namespace = parser.parse_args(sys.argv[1:])

    # output directory
    outputdir = namespace.outputdir
    if (outputdir is None):
        outputdir = os.getcwd()
    else:
        outputdir = os.path.relpath(outputdir, os.getcwd())
        if not os.path.isdir(outputdir):
            os.makedirs(outputdir)
    print "{:<20s}{:<s}".format("outputdir", outputdir)

    # parameter file
    if namespace.paramfile is None:
        allparams = default_parameters()
        paramfile = "params_default.yml"
        with open(paramfile,'w') as fout:
            yaml.dump(allparams,fout)
    else:
        paramfile = namespace.paramfile.name
        allparams = yaml.load(namespace.paramfile)

    dest = os.path.join(outputdir, os.path.basename(paramfile))
    if (os.path.realpath(dest) != os.path.realpath(paramfile)):
        shutil.copy(paramfile,dest)
    paramfile = dest

    # load ND2 file
    ## load images
    params=allparams['get_nd2_images_args']
    images = acq.get_nd2_images(namespace.ND2,**params)
    ## print metadata
    fileout = os.path.join(outputdir, "metadata.txt")
    with open(fileout,'w') as fout:
        yaml.safe_dump(images.metadata, fout, encoding=('utf-8'), default_flow_style=False, allow_unicode=False)





