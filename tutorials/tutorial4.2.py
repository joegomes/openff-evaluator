from openff import ForceField
force_field = ForceField('openff-1.0.0.offxml')

# Extract the smiles of all unique components in our data set.
from openff.topology import Molecule, Topology

all_smiles = set(
    component.smiles
    for substance in data_set.substances
    for component in substance.components
)

for smiles in all_smiles:

    # Find those VdW parameters which would be applied to those components.
    molecule = Molecule.from_smiles(smiles)
    topology = Topology.from_molecules([molecule])

    labels = force_field.label_molecules(topology)[0]

    # Tag the exercised parameters as to be optimized.
    for parameter in labels["vdW"].values():
        parameter.add_cosmetic_attribute("parameterize", "epsilon, rmin_half")

# Save the annotated force field file.
force_field.to_file('forcefield/openff-1.0.0-tagged.offxml')
