import os

import pandas as pd


def _build_dataframe():
    '''
    Build a dataframe with minimal information for this entity.
    '''

    headers = ['biosample_id_namespace', \
               'biosample_local_id', \
               'association_type', \
               'disease' ]

    df = pd.DataFrame( columns = headers )

    return df

def create_manifest( output_directory ):
    filename = os.path.join( output_directory, 'biosample_disease.tsv' )
    df = _build_dataframe()
    df.to_csv( filename, sep="\t", index=False)
    
    return True
