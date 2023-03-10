import os

import pandas as pd


def _build_dataframe():
    '''
    Build a dataframe with minimal information for this entity.
    '''

    headers = ['collection_id_namespace', \
               'collection_local_id', \
               'anatomy']

    df = pd.DataFrame( columns = headers )

    return df

def create_manifest( output_directory ):
    filename = os.path.join( output_directory, 'collection_anatomy.tsv' )
    df = _build_dataframe()
    df.to_csv( filename, sep="\t", index=False)
    
    return True
