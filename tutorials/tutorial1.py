from openff.evaluator.datasets.thermoml import ThermoMLDataSet
from openff.evaluator.datasets.curation.components.filtering import (
    FilterByPropertyTypes,
    FilterByPropertyTypesSchema
)
from openff.evaluator.datasets.curation.components.filtering import (
    FilterByPressure,
    FilterByPressureSchema,
    FilterByTemperature,
    FilterByTemperatureSchema,
)
from openff.evaluator.datasets.curation.components.filtering import (
    FilterBySmiles,
    FilterBySmilesSchema,
)
from openff.evaluator import unit
from openff.evaluator.thermodynamics import ThermodynamicState
from openff.evaluator.substances import Substance
from openff.evaluator.datasets import MeasurementSource
from openff.evaluator.datasets import PropertyPhase
from openff.evaluator.properties import EnthalpyOfVaporization

data_set = ThermoMLDataSet.from_doi(
    "10.1016/j.fluid.2013.10.034",
    "10.1021/je1013476",
)

data_set = FilterByPropertyTypes.apply(
    data_set, FilterByPropertyTypesSchema(property_types=["Density"])
)

# First filter by temperature.
data_set = FilterByTemperature.apply(
    data_set,
    FilterByTemperatureSchema(minimum_temperature=298.0, maximum_temperature=298.2)
)
# and then by pressure
data_set = FilterByPressure.apply(
    data_set,
    FilterByPressureSchema(minimum_pressure=101.224, maximum_pressure=101.426)
)

data_set = FilterBySmiles.apply(
    data_set,
    FilterBySmilesSchema(smiles_to_include=["CCO", "CC(C)O"])
)

print(f"There are now {len(data_set)} properties after filtering")
pandas_data_set = data_set.to_pandas()
pandas_data_set[
    ["Temperature (K)", "Pressure (kPa)", "Component 1", "Density Value (g / ml)", "Source"]
].head()

thermodynamic_state = ThermodynamicState(
    temperature=298.15 * unit.kelvin, pressure=1.0 * unit.atmosphere
)
ethanol = Substance.from_components("CCO")
isopropanol = Substance.from_components("CC(C)O")
source = MeasurementSource(doi="10.1016/S0021-9614(71)80108-8")
ethanol_hvap = EnthalpyOfVaporization(
    thermodynamic_state=thermodynamic_state,
    phase=PropertyPhase.Liquid | PropertyPhase.Gas,
    substance=ethanol,
    value=42.26*unit.kilojoule / unit.mole,
    uncertainty=0.02*unit.kilojoule / unit.mole,
    source=source
)
isopropanol_hvap = EnthalpyOfVaporization(
    thermodynamic_state=thermodynamic_state,
    phase=PropertyPhase.Liquid | PropertyPhase.Gas,
    substance=isopropanol,
    value=45.34*unit.kilojoule / unit.mole,
    uncertainty=0.02*unit.kilojoule / unit.mole,
    source=source
)
data_set.add_properties(ethanol_hvap, isopropanol_hvap)
pandas_data_set = data_set.to_pandas()
pandas_data_set[
    ["Temperature (K)",
     "Pressure (kPa)",
     "Component 1",
     "Density Value (g / ml)",
     "EnthalpyOfVaporization Value (kJ / mol)",
     "Source"
     ]
].head()

data_set.json("filtered_data_set.json", format=True);
