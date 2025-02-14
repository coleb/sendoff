"""Test rdkit parsing of metadata on generated SDFs."""
from rdkit import Chem

from sendoff.sdblock import Pathy


def test_single_mol_read(single_mol_sdf: Pathy) -> None:
    """An sdf of a single molecule contains one molecule.

    Args:
        single_mol_sdf: pytest fixture of a Path to the sdf
    """
    mols = list(Chem.SDMolSupplier(str(single_mol_sdf)))
    assert len(mols) == 1


def test_double_mol_read(double_mol_sdf: Pathy) -> None:
    """An sdf of two molecule contains two molecules.

    Args:
        double_mol_sdf: pytest fixture of a Path to the sdf
    """
    mols = list(Chem.SDMolSupplier(str(double_mol_sdf)))
    assert len(mols) == 2


def test_titled_mol_read(single_titled_mol_sdf: Pathy) -> None:
    """An sdf of a single titled molecule contains it with the expected title.

    Args:
        single_titled_mol_sdf: pytest fixture of a Path to the sdf
    """
    mol = next(Chem.SDMolSupplier(str(single_titled_mol_sdf)))
    assert mol.GetProp("_Name") == "Title"


def test_delimiter_titled_mol_read(
    single_delimiter_titled_mol_sdf: Pathy,
) -> None:
    """An sdf of a delimiter titled molecule contains it with the expected title.

    Args:
        single_delimiter_titled_mol_sdf: pytest fixture of a Path to the sdf
    """
    mol = next(Chem.SDMolSupplier(str(single_delimiter_titled_mol_sdf)))
    assert mol.GetProp("_Name") == "$$$$"


def test_first_delimiter_titled_mol_read(
    double_first_delimiter_titled_mol_sdf: Pathy,
) -> None:
    """SDF with 1st molecule delimiter titled, containing with expected titles.

    Args:
        double_first_delimiter_titled_mol_sdf: pytest fixture of a Path to sdf
    """
    supp = Chem.SDMolSupplier(str(double_first_delimiter_titled_mol_sdf))
    mol = next(supp)
    other_mol = next(supp)
    assert mol.GetProp("_Name") == "$$$$"
    assert other_mol.GetProp("_Name") == "Title"


def test_second_delimiter_titled_mol_read(
    double_second_delimiter_titled_mol_sdf: Pathy,
) -> None:
    """SDF with 2nd molecule delimiter titled, containing with expected titles.

    Args:
        double_second_delimiter_titled_mol_sdf: pytest fixture of a Path to sdf
    """
    supp = Chem.SDMolSupplier(str(double_second_delimiter_titled_mol_sdf))
    other_mol = next(supp)
    mol = next(supp)
    assert other_mol.GetProp("_Name") == "Title"
    assert mol.GetProp("_Name") == "$$$$"


def test_single_record_mol_read(single_record_mol_sdf: Pathy) -> None:
    """An sdf of a delimiter record valued molecule contains the expected data.

    Args:
        single_record_mol_sdf: pytest fixture of a Path to the sdf
    """
    mol = next(Chem.SDMolSupplier(str(single_record_mol_sdf)))
    assert mol.GetProp("Record") == "Value"


def test_delimiter_record_mol_read(
    single_delimiter_record_mol_sdf: Pathy,
) -> None:
    """An sdf of a delimiter record valued molecule contains the expected data.

    Args:
        single_delimiter_record_mol_sdf: pytest fixture of a Path to the sdf
    """
    mol = next(Chem.SDMolSupplier(str(single_delimiter_record_mol_sdf)))
    assert mol.GetProp("Record") == "$$$$"


def test_multiline_record_mol_read(
    single_multiline_record_mol_sdf: Pathy,
) -> None:
    """An sdf of a multiline record valued molecule contains the expected data.

    Args:
        single_multiline_record_mol_sdf: pytest fixture of a Path to the sdf
    """
    mol = next(Chem.SDMolSupplier(str(single_multiline_record_mol_sdf)))
    assert mol.GetProp("Record") == "0\n1\n2\n3"


def test_empty_string_record_mol_read(
    single_empty_string_record_mol_sdf: Pathy,
) -> None:
    """An sdf of an empty string record valued molecule contains the expected data.

    Args:
        single_empty_string_record_mol_sdf: pytest fixture of a Path to the sdf
    """
    mol = next(Chem.SDMolSupplier(str(single_empty_string_record_mol_sdf)))
    assert mol.GetProp("Record") == ""


def test_multiline_record_name_mol_read(
    single_multiline_record_name_mol_sdf: Pathy,
) -> None:
    """An sdf of a multiline record name molecule cannot contain the expected data.

    Args:
        single_multiline_record_name_mol_sdf: fixture of a Path to the sdf
    """
    mol = next(Chem.SDMolSupplier(str(single_multiline_record_name_mol_sdf)))
    assert not mol.HasProp("Rec\nord")
