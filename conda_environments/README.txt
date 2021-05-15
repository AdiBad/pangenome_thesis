TO LIST THE DEPENDENCIES IN A CONDA ENVIRONMENT
conda env export > mydependencies.yml

TO LOAD THE YML INTO A CONDA ENVIRONMENT
conda env create -f mydependencies.yml
