# Download the archive of all properties from the IJT journal.
import requests
request = requests.get("https://trc.nist.gov/ThermoML/IJT.tgz", stream=True)

# Make sure the request went ok.
assert request

# Unzip the files into a new 'ijt_files' directory.
import io, tarfile
tar_file = tarfile.open(fileobj=io.BytesIO(request.content))
tar_file.extractall("ijt_files")

# Download the archive of all properties from the TCA journal.
import requests
request = requests.get("https://trc.nist.gov/ThermoML/TCA.tgz", stream=True)

# Make sure the request went ok.
assert request

# Unzip the files into a new 'tca_files' directory.
import io, tarfile
tar_file = tarfile.open(fileobj=io.BytesIO(request.content))
tar_file.extractall("tca_files")

# Download the archive of all properties from the FPE journal.
import requests
request = requests.get("https://trc.nist.gov/ThermoML/FPE.tgz", stream=True)

# Make sure the request went ok.
assert request

# Unzip the files into a new 'fpe_files' directory.
import io, tarfile
tar_file = tarfile.open(fileobj=io.BytesIO(request.content))
tar_file.extractall("fpe_files")

# Download the archive of all properties from the JCT journal.
import requests
request = requests.get("https://trc.nist.gov/ThermoML/JCT.tgz", stream=True)

# Make sure the request went ok.
assert request

# Unzip the files into a new 'jct_files' directory.
import io, tarfile
tar_file = tarfile.open(fileobj=io.BytesIO(request.content))
tar_file.extractall("jct_files")

# Download the archive of all properties from the JCED journal.
import requests
request = requests.get("https://trc.nist.gov/ThermoML/JCED.tgz", stream=True)

# Make sure the request went ok.
assert request

# Unzip the files into a new 'jced_files' directory.
import io, tarfile
tar_file = tarfile.open(fileobj=io.BytesIO(request.content))
tar_file.extractall("jced_files")

# Get the names of the extracted files
import glob
file_names = glob.glob("*_files/*.xml")

# Create the data set object
from openff.evaluator.datasets.thermoml import ThermoMLDataSet
data_set = ThermoMLDataSet.from_file(*file_names)

# Save the data set to a JSON object
data_set.json(file_path="fulldata.json", format=True)
