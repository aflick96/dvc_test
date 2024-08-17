# DVC Pipeline

# Usage
## Remote Network Folders
**//FLICKAT-WL1/dvc_source_data_test** is a shared network drive where the raw EPL fantasy data is stored.
**//FLICKAT-WL1/dvc_test** is a shared network drive dvc repository where the results of an expirement are stored.
Contact admin for access to these shared drives.

## Workflow
Ensure DVC is installed locally [dvc](https://dvc.org/)

### Share

### 1. Reproduce pipeline 
1. Clone the repository and ensure access to the remote network directories.
2. Navigate to the root directory and run **dvc repro** to reproduce the pipeline defined in dvc.yaml.

### Pull pipeline 

# DVC
## Why?
DVC allows the project to stay lightweight by storing data file meta data.  

## Files
### dvc.yaml
Defines the pipeline stages and the commands, command dependencies, and output files.
- **cmd** defines the command to execute.
- **deps** defines the command dependencies.
- **outs** defines the output files.
- **params** predefined variables to pass to a command (params.yaml).

### params.yaml
Predefined variables to pass to commands

### dvc.lock
Serves as a detailed snapshot of the state of the pipeline, including the commands, dependencies, outputs, and corresponding hashes. The file ensures the reproducibility of the pipeline by locking down the exact versions of data and code that were used in the last successful run. Since this file serves as a snapshot, committing the dvc.lock is crucial in order to save the state of a particular run.

## Commands
### dvc init
Initiliaze dvc for repository.

### dvc add [file/directory]
Creates file.dvc/directory.dvc which stores the meta data of the data file. These file are what is included in the repo.

### dvc add -d remoteRepoName remoteRepoUrl
Updates the .dvc/config file with a reference to the remote repository where data files will be pushed.

### dvc push
Migrates cached data files to remote dvc repo.

### dvc pull

### dvc status

### dvc repro [stage]
