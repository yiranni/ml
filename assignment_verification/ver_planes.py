import os
import pandas as pd
import json
import zipfile
import sys

def submission_checker(fp):
    global final_script
    final_script = ''
    fpt = fp + '/tests' # path for extracted files
    try:
        os.mkdir( fpt, 0o777 ) # create subdirectory for extracted files
    except FileExistsError:
        print('test subdirectory already exists') # unless it already exists
        
    def get_zip_name():
        '''Get the name of the zip file in the specified directory. Make sure only one zip file in the specified directory.'''
        zf = '' # name of zip file
        files = files = [f for f in os.listdir(fp) if os.path.isfile(os.path.join(fp, f))]
        n_zips = 0
        for f in files:
            if (f.split('.')[1] == 'zip'):
                zf = f
                n_zips += 1
            if n_zips > 1:
                raise ValueError('There is more than one zip file in this directory. It should only include a single zip file.')
        return(zf)
    
    def un_zip_file():
        '''Unzip the submission file'''
        zip_file = get_zip_name()
        if zip_file == '':
            raise ValueError('There is no zip file in the specified directory.')
        zffp = fp + '/' + zip_file
        zip_ref = zipfile.ZipFile(zffp, 'r')
        zip_ref.extractall(fpt)
        zip_ref.close()
        print(zip_file + ' unzipped')
        
    un_zip_file()
    
    def get_ipynb_name():
        '''Get the name of the ipynb file in the specified directory. Make sure only one ipynb file in the specified directory.'''
        zf = '' # name of file
        files = files = [f for f in os.listdir(fpt) if os.path.isfile(os.path.join(fpt, f))]
        n_zips = 0
        for f in files:
            if (f.split('.')[1] == 'ipynb'):
                zf = f
                n_zips += 1
            if n_zips > 1:
                raise ValueError('There is more than one ipynb file in this directory. It should only include a single ipynb file.')
        for d in os.listdir(fpt):
            if os.path.isdir(d):
                raise ValueError('No subdirectories allowed. All files should be in this directory.')
        return(zf)

    ipynb_file = get_ipynb_name()
    print('Submission notebook: ' + ipynb_file)
    
    def read_notebook():
        '''Read the contents of the Jupyter Notebook.'''
        sub_file = fpt + "/" + ipynb_file 
        jnb  = open(sub_file, "r")
        return(jnb.read())
    
    jnb_json = (read_notebook())
    
    def check_files():
        '''Check the contents of the extracted zip file, for correct file types and expected number of files.'''
        files = files = [f for f in os.listdir(fpt) if os.path.isfile(os.path.join(fpt, f))]
        ft_allowed = ['ipynb', 'pkl', 'py']
        for f in files:
            if f.split('.')[1] not in ft_allowed:
                raise ValueError('Invalid file type; only .ipynb, .pkl, and .py file extensions permitted')
            if f.split('.')[1] == 'py':
                if f.split('.')[0] != 'my_measures':
                    print('WARNING: Invalid .py file; `my_measures.py` is the only .py file permitted')

    check_files()
    
    def initial_checks():
        '''Initial checks for fits, CSV reads, and computation of performance measures.'''
        x = json.loads(jnb_json)
        has_cm = False
        has_readcsv = False
        has_fit = False
        probs = ''
        for cell in x['cells']:
            if cell['cell_type'] == "code":
                for l in cell['source']:
                    if l.find('.fit') >= 0:
                        if l.find('#') < 0 or (l.find('#') >= 0 and l.find('.fit') < l.find('#')):
                            if has_fit == False:
                                has_fit = True
                                probs += "You are using a FIT method; this is prohibited; you can only use transform methods in the submission. "
                    if l.find('.compute_measures()') >= 0:
                        if l.find('#') < 0 or (l.find('#') >= 0 and l.find('.compute_measures()') < l.find('#')):
                            if has_cm == True:
                                probs += "You are computing performance measures more than once and I don't know which to use. "
                            if has_cm == False:
                                has_cm = True
                    if l.find('read_csv') >= 0:
                        if l.find('#') < 0 or (l.find('#') >= 0 and l.find('read_csv') < l.find('#')):
                            if has_readcsv == True:
                                probs += "You are reading more than one CSV file, but should only be reading one. "
                            if has_readcsv == False:
                                has_readcsv = True
        if has_cm == False:
            probs += "Performance measures are not being computed. "
        if has_readcsv == False:
            probs += "No CSV file is being read. "
        if len(probs) > 1:
            raise ValueError(probs)

    initial_checks()
   
    print("------------------------------------------")
    print("SUCCESS!")

submission_checker(sys.argv[1])