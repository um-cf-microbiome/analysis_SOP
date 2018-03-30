# This script contains an example analysis pipeline
# for 16S sequencing data, and is intended for study
# of the lung microbiome in cystic fibrosis by the
# Caverly and LiPuma research groups,
# Dept. of Pediatrics and Infectious Diseases, University of Michigan.

import sys, os, pandas
sys.path.insert(0,'F://software/ml4cf/src')
job_name = 'example'
job_dir = 'F://software/analysis_SOP'
# Provide .csv file with a column labelled 'Sputum_Number'
sample_list_file = str(job_dir+'sample_list.csv')

# Import 'ml4cf' source code
import classes, eco
from eco import mothur
from classes import job, host
host_info=host.info()

# Initialize 'job.info' class, which assigns global variables for the job
job_info = job.info(job_name=str(job_name),job_dir=str(job_dir),host_info=host.info())
# Read sample list
job_info.sample_list = pandas.read_csv(job_info.sample_list_file)['Sputum_Number']
# Read list of control samples (if contained in a separate file)
#job_info.control_list = pandas.read_csv(job_info.control_list_file)['Sputum_Number']

# Analyze sequencing files with mothur

# make stability.files (list of sample names and .fastq file pairs)
mothur.make_stability_files(job_info)
# Dynamically build and run MiSeq SOP for batch job
# Original SOP: https://www.mothur.org/wiki/MiSeq_SOP

# CAUTION: The steps in this SOP are static, however,
# applying a different version of mothur, or a different
# reference database, will change the results.

# (The 'batch()' function performs calculations on an 
# as-needed basis. If the job directory has output files 
# from a previous run, the corresponding mothur calculation 
# step(s) are considered 'complete', and are omitted from 
# the batch script.)
mothur.batch(job_info)

#data.edit.zip(job_info)

# Calculate Shannon Beta using 'entropart' (R)
# https://github.com/EricMarcon/entropart
#entropart.batch(job_info)

# (3) Build dataframes
#     (3-A) Read data and build dataframes

#data_file = open(str(os.getcwd()+'NTM/data/ntm-first-positive-incomplete.csv'),'r')
#clinical_feat_file = open(str(os.getcwd()+'NTM/analysis/clinical_features.csv'),'r')
#reg_feat_file = open(str(os.getcwd()+'NTM/analysis/regression_features.csv'),'r')
#classifiers_file = open(str(os.getcwd()+'NTM/analysis/classifiers.csv'),'r')    

# Construct pandas dataframes
#                   'microbial_full': Contains all default microbial
#                   data from Mothur MiSeq-SOP, where the data was subsequently
#                   used to calculate individual OTU relative abundances
#	                  'microbial_avium': Contains microbial data for samples that
#		                tested positive for M. avium
#	                  'microbial_abscessus': Contains microbial data for samples that
#		                tested positive for M. abscessus
#	                  'clinical_full': Contains all clinical features (described in:
#	                  'data/features_description.txt')
#	                  'clinical_numeric': Contains only the clinical features
#		                whose values are numeric
#                   'clinical_no_fev1': Contains all clinical features except 'fev1'
#     (3-B) Append subject-specific regression results as features in dataframe
#      regression_results = lin_reg.lin_reg_patient(regression_input)
# (4) Train SVM model
#     (4-A) Format dataset for 'libsvm'
#     (4-B) Train SVM models with the following variations:
#            i) Each classifier (Disease yes/no, transient/persistent, MAC/Mab.)
#min_C,max_C,step_C = -2,9,2
#C_range = str(min_C+','+max_C+','+step_C)
#min_gamma,max_gamma,step_gamma = 1,-11,-2
#gamma_range = str(min_gamma+','+max_gamma+','+step_gamma)
#grid_exe_input = str('-log2c '+C_range+' -log2g '+gamma_range)
#            iii) Vary F-score threshold
#            iv) Vary SVM-included features (above F-score threshold)
# (6) Plot results
#