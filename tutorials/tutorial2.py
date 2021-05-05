from openff.evaluator.datasets import PhysicalPropertyDataSet
from openff.evaluator.forcefield import SmirnoffForceFieldSource
from openff.evaluator.utils import setup_timestamp_logging
from openff.evaluator.client import RequestOptions
from openff.evaluator.backends import ComputeResources
from openff.evaluator.backends.dask import DaskLocalCluster
from openff.evaluator.server import EvaluatorServer
from openff.evaluator.client import EvaluatorClient
from openff.evaluator.properties import Density, EnthalpyOfVaporization
import time

start = time.time()

data_set_path = "filtered_data_set.json"

# If you have not yet completed that tutorial or do not have the data set file
# available, a copy is provided by the framework:

# from openff.evaluator.utils import get_data_filename
# data_set_path = get_data_filename("tutorials/tutorial01/filtered_data_set.json")

data_set = PhysicalPropertyDataSet.from_json(data_set_path)

force_field_path = "openff-1.0.0.offxml"
force_field_source = SmirnoffForceFieldSource.from_path(force_field_path)

density_schema = Density.default_simulation_schema(n_molecules=1024)
h_vap_schema = EnthalpyOfVaporization.default_simulation_schema(n_molecules=1024)

# Create an options object which defines how the data set should be estimated.
estimation_options = RequestOptions()
# Specify that we only wish to use molecular simulation to estimate the data set.
estimation_options.calculation_layers = ["SimulationLayer"]

# Add our custom schemas, specifying that the should be used by the 'SimulationLayer'
estimation_options.add_schema("SimulationLayer", "Density", density_schema)
estimation_options.add_schema("SimulationLayer", "EnthalpyOfVaporization", h_vap_schema)

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

calculation_backend = DaskLocalCluster(
    number_of_workers=4,
    resources_per_worker=ComputeResources(
        number_of_threads=1,
        number_of_gpus=1,
        preferred_gpu_toolkit=ComputeResources.GPUToolkit.CUDA
    ),
)
calculation_backend.start()

evaluator_server = EvaluatorServer(calculation_backend=calculation_backend)
evaluator_server.start(asynchronous=True)

evaluator_client = EvaluatorClient()

request, exception = evaluator_client.request_estimate(
    property_set=data_set,
    force_field_source=force_field_source,
    options=estimation_options,
)

assert exception is None

results, exception = request.results(synchronous=True, polling_interval=30)
assert exception is None

print(len(results.queued_properties))

print(len(results.estimated_properties))

print(len(results.unsuccessful_properties))
print(len(results.exceptions))

results.estimated_properties.json("estimated_data_set_1024.json", format=True);

end = time.time()
lapse = end - start
print(str(lapse).format(end-start))
