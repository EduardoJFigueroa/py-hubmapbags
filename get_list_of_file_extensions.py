import glob
import hubmapbags
import subprocess
from os.path import exists
from tabulate import tabulate 
import pandas as pd
from datetime import date
from os.path import basename
import os
from os.path import splitext
from pathlib import Path

token='AgzPMdPlmEwwyQd50Bkw20Gy55O6vYynVkVbJQ6pJ105yBQd7JCkCylVn46Ev51mQW4p7nGwrawjVnIby3vKbf6nJm'
def _get_number_of_files( directory, extension ):
    pathname = directory + "/**/*." + extension
    files = glob.glob(pathname, recursive=True)

    return len(files)

def get_file_frequency( directory ):
    extensions = ['.tsv', '.czi', '.xml', '.txt', '.tiff', '.gz', '.dat', '.tif', \
       '.xlsx', '.json', '.png', '.fcs', '.csv', '.pptx', '.gci', '.zip', \
       '.pdf', '.orig', '.scn', '.list', '.bam', '.raw', '.mzML']
    
    d = {}
    for key in extensions:
        d[key] =  _get_number_of_files( directory, key )
    
    return json.dumps(d)

output_directory = 'reports'

def get_list_of_files( directory ):
    return Path(directory).glob('**/*')

def compute_number_of_files( directory ):
	command = 'find "' + directory + '" -type f | wc -l'
	answer = subprocess.check_output( command, shell=True )
	return str(answer.decode( 'utf-8' ).replace('\n','').replace('"',''))

def get_number_of_records( filename ):
	if exists( filename ):
		df = pd.read_pickle( filename )
		return int(len(df))
	else:
		return None

def get_dataset_info( hubmap_id, instance='prod', token=None ):
	try:
		datasets = hubmapbags.magic.__extract_dataset_info_from_db( hubmap_id, token=token, instance=instance )
		for dataset in datasets.iterrows():
			dataset = dataset[1]
			return dataset
	except:
		print(hubmap_id)
		return None

def generate_directory( dataset ):
	return dataset['full_path']

def generate_pickle_filename( dataset ):
	data_directory = dataset['full_path']
	pickle_filename = data_directory.replace('/','_').replace(' ','_') + '.pkl'
	print( pickle_filename )
	if exists(pickle_filename):
		return pickle_filename
	else:
		return ''
	
def get_number_of_files( directory ):
	return None

assays = ['AF', 'ATACseq-bulk', 'cell-dive', 'CODEX', 'DART-FISH', 'IMC2D', 'IMC3D', \
	'lc-ms_label-free', 'lc-ms_labeled', 'lc-ms-ms_label-free', 'lc-ms-ms_labeled', \
	'LC-MS-untargeted', 'Lightsheet', 'MALDI-IMS', 'MIBI', 'NanoDESI', 'NanoPOTS', \
	'MxIF', 'PAS', 'bulk-RNA', 'SNARE-ATACseq2', 'SNARE-RNAseq2', 'scRNAseq-10xGenomics-v2', \
	'scRNAseq-10xGenomics-v3', 'sciATACseq', 'sciRNAseq', 'seqFish', \
	'snATACseq', 'snRNAseq-10xGenomics-v2', 'snRNAseq-10xGenomics-v3', 'Slide-seq', \
	'Targeted-Shotgun-LC-MS', 'TMT-LC-MS', 'WGS', 'LC-MS', 'MS', 'LC-MS_bottom_up', \
	'MS_bottom_up', 'LC-MS_top_down', 'MS_top_down']

table = []
headers = ['Status', 'Assay type', 'Extension', 'Data Type', 'File Type' ]
for assay in assays:
	print(assay)
	ids = hubmapbags.apis.get_hubmap_ids( assay, token=token )

	extensions = []
	for id in ids:
		hubmap_id = id['hubmap_id']
		dataset = get_dataset_info( hubmap_id, instance='prod', token=token )
		
		if dataset is not None:
			if id['data_type'] == assay and id['status'] == 'Published':
				status = id['status']
				hubmap_id = id['hubmap_id']
				directory = generate_directory( dataset )
				p = get_list_of_files( directory )

				for file in p:
					if file.is_file():
						table.append([status, assay, splitext(file)[1], None, None])
				break

today = date.today()
filename = 'cfde-file-extension-report-' + str(today).replace('-','') + '.tsv'
df = pd.DataFrame (table, columns=headers)
df = df.drop_duplicates()
df.to_csv( filename, index = False, sep="\t" )
df.to_pickle( filename.replace('tsv','pkl') )