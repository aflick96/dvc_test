# DVC Pipeline
## Overview
This project uses DVC to manage and reproduce a machine learning pipeline that process EPL fantasy data. The data and experiment results are stored on shared network drives and can be accessed using DVC commands.

## Usage
### Remote Network Folders
- **//FLICKAT-WL1/dvc_source_data_test**: This shared network drive stores the raw EPL fantasy data. Contact admin for access. 
- **//FLICKAT-WL1/dvc_test**: This shared network drive serves as a DVC remote repository where the results of experiments are stored. Contact admin for access.

## Workflow
1. Setup
    1. Ensure DVC is installed locally ([dvc](https://dvc.org/))

2. Reproduce pipeline
    1. Clone the repository and ensure access to remote network directories.
    2. Navigate to the root directory of the cloned repo.
    3. Execute the following command to reproduce the pipeline defined in **'dvc.yaml'**:
    ```bash
    dvc repro
    ```
    This will execute the pipeline stages and ensure that the data and results are consistent with the last committed version.

3. Share results
    - To share the results or push changes to the DVC remote repo, use the **'dvc push'** command. Results are associated with commits. Push the your results and commit the changes to the dvc.lock file to share.

4. Pull pipeline data
    - To retrieve data or results from the DVC remote repo, use the **'dvc pull'** command. Results are associated with commits. Checkout the commit of interest and run **'dvc pull'** to retrieve data or results for that commit. 

# DVC
## Why use DVC?
DVC enables lightweight project management by storing metadata about large data files, rather than the files themselves. This allows the project to remain manageable in size while ensuring data consistency and reproducibility.  

## Key Files
**dvc.yaml**: Defines the pipeline stages, including the commands to execute, their dependencies, and the output files.
   - **cmd**: The command to be executed.
   - **deps**: The dependencies required for the command.
   - **outs**: The files generated as output by the command.
   - **params**: Parameters defined in **'params.yaml'** that are passed to the command.

**params.yaml**: Stores predefined variables and parameters that are used in the pipeline commands, makeing it easy to modify configurations without change the pipeline code.

**dvc.lock**: A snapshot of the current state of the pipeline, including the exact versions of data and code used in the last **successful** run. This file ensures reproducibility and must be commited to Git to preserve the state of a particular run.

## Common Commands
**dvc init**: Initiliazes DVC in the repository.

**dvc add [file/directory]**: Tracks a file or directory with DVC, creating a **'.dvc'** file that stores metadata about the data file. The **'dvc'** file is what gets committed to the reposity. 

**dvc add -d [remoteRepoName] [remoteRepoUrl]**: Adds a remote repository where DVC can store data files. This updates the **'.dvc/config'** file with the remote repository details.

**dvc push**: Uploads cached data files to the remote DVC repository.

**dvc pull**: Downloads the required data files from the remote DVC repository to your local.

**dvc status**: Shows the status of DVC tracked files and whether they need to be pushed, pulled, or reproduced.

**dvc repro [stage]**: Reproduces a specific stage of the pipeline, rerunning it if any of its dependencies have changed.