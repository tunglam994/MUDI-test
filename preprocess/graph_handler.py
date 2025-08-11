import os
import json
from tqdm import tqdm

import networkx as nx
from rdkit import Chem

import numpy as np
import torch
from torch_geometric.data import Data

def get_edge_index(mol):
    edges = []
    for bond in mol.GetBonds():
      i = bond.GetBeginAtomIdx()
      j = bond.GetEndAtomIdx()
      edges.extend([(i,j), (j,i)])

    edge_index = list(zip(*edges))
    return edge_index

def atom_feature(atom):
    return [atom.GetAtomicNum(),
            atom.GetDegree(),
            atom.GetNumImplicitHs(),
            atom.GetExplicitValence(),
            atom.GetImplicitValence(),
            atom.GetTotalValence(),
            atom.GetNumRadicalElectrons(),
            atom.GetHybridization(),
            atom.GetIsAromatic(),
            atom.IsInRing()]

def bond_feature(bond):
    return [bond.GetBondType(), 
            bond.GetStereo(),
            bond.GetIsConjugated(),
            bond.GetIsAromatic(),
            bond.IsInRing()]

def smiles_to_pyg(smiles):
    """
    Convert SMILES to a PyG Data object
    """
    if smiles == 'None':
        return Data(edge_index=torch.LongTensor([[0], [0]]),
                    x=torch.FloatTensor([[0, 0, 0, 0, 0, 0, 0, 0, 2, 2]]),
                    edge_attr=torch.FloatTensor([[0, 0, 2, 2, 2]]),
                    mol="None",
                    smiles="None")

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return Data(edge_index=torch.LongTensor([[0], [0]]),
                    x=torch.FloatTensor([[0, 0, 0, 0, 0, 0, 0, 0, 2, 2]]),
                    edge_attr=torch.FloatTensor([[0, 0, 2, 2, 2]]),
                    mol="None",
                    smiles="None")

    id_pairs = ((b.GetBeginAtomIdx(), b.GetEndAtomIdx()) for b in mol.GetBonds())
    atom_pairs = [z for (i, j) in id_pairs for z in ((i, j), (j, i))]

    bonds = (mol.GetBondBetweenAtoms(i, j) for (i, j) in atom_pairs)
    atom_features = [atom_feature(a) for a in mol.GetAtoms()]
    bond_features = [bond_feature(b) for b in bonds]

    edge_index = list(zip(*atom_pairs))
    if edge_index == []:
        edge_index = torch.LongTensor([[0], [0]])
        edge_attr = torch.FloatTensor([[0, 0, 2, 2, 2]])
    else:
        edge_index = torch.LongTensor(edge_index)
        edge_attr = torch.FloatTensor(bond_features)

    return Data(edge_index=edge_index,
                x=torch.FloatTensor(atom_features),
                edge_attr=edge_attr,
                mol=mol,
                smiles=smiles)

def smiles_to_nx(smiles):
    """
    Convert SMILES to NetworkX undirected molecular graph with atom and bond features.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    G = nx.Graph()

    for atom in mol.GetAtoms():
        feats = atom_feature(atom)
        G.add_node(atom.GetIdx(),
                   atomic_num=feats[0],
                   degree=feats[1],
                   num_implicit_h=feats[2],
                   explicit_valence=feats[3],
                   implicit_valence=feats[4],
                   total_valence=feats[5],
                   num_radical_e=feats[6],
                   hybridization=int(feats[7]),
                   is_aromatic=bool(feats[8]),
                   in_ring=bool(feats[9]))

    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        feats = bond_feature(bond)

        edge_data = {
            "bond_type": str(feats[0]),
            "stereo": int(feats[1]),
            "is_conjugated": bool(feats[2]),
            "is_aromatic": bool(feats[3]),
            "in_ring": bool(feats[4]),
        }

        G.add_edge(i, j, **edge_data)

    return G

def nx_to_pyg(G, smiles="None", mol="None"):
    """
    Convert a NetworkX graph to a PyG Data object.
    Ensures the graph is undirected and edge features are duplicated for both directions.
    """
    if G is None or G.number_of_nodes() == 0:
        return Data(edge_index=torch.LongTensor([[0], [0]]),
                    x=torch.FloatTensor([[0]*10]),
                    edge_attr=torch.FloatTensor([[0, 0, 2, 2, 2]]),
                    mol="None",
                    smiles="None")

    # Node features
    x = []
    for _, data in G.nodes(data=True):
        node_feat = [
            int(data["atomic_num"]),
            int(data["degree"]),
            int(data["num_implicit_h"]),
            int(data["explicit_valence"]),
            int(data["implicit_valence"]),
            int(data["total_valence"]),
            int(data["num_radical_e"]),
            int(data["hybridization"]),
            int(data["is_aromatic"]),
            int(data["in_ring"]),
        ]
        x.append(node_feat)
    x = torch.FloatTensor(x)

    edge_index = []
    edge_attr = []
    for u, v, data in G.edges(data=True):
        bond_feat = [
            float(data["bond_type"] == 'SINGLE'),
            int(data["stereo"]),
            int(data["is_conjugated"]),
            int(data["is_aromatic"]),
            int(data["in_ring"]),
        ]
        edge_index.extend([[int(u), int(v)], [int(v), int(u)]])
        edge_attr.extend([bond_feat, bond_feat])

    if not edge_index:
        edge_index = torch.LongTensor([[0], [0]])
        edge_attr = torch.FloatTensor([[0, 0, 2, 2, 2]])
    else:
        edge_index = torch.LongTensor(edge_index).t().contiguous()
        edge_attr = torch.FloatTensor(edge_attr)

    return Data(x=x,
                edge_index=edge_index,
                edge_attr=edge_attr,
                mol=mol,
                smiles=smiles)

def load_graphml(file_path):
    """
    Load a NetworkX graph from a .graphml file.
    """
    try:
        G = nx.read_graphml(file_path)
        for node, data in G.nodes(data=True):
            data["atomic_num"] = int(data.get("atomic_num", 0))
            data["degree"] = int(data.get("degree", 0))
            data["num_implicit_h"] = int(data.get("num_implicit_h", 0))
            data["explicit_valence"] = int(data.get("explicit_valence", 0))
            data["implicit_valence"] = int(data.get("implicit_valence", 0))
            data["total_valence"] = int(data.get("total_valence", 0))
            data["num_radical_e"] = int(data.get("num_radical_e", 0))
            data["hybridization"] = int(data.get("hybridization", 0))
            data["is_aromatic"] = data.get("is_aromatic", "False") == "True"
            data["in_ring"] = data.get("in_ring", "False") == "True"

        for u, v, data in G.edges(data=True):
            data["stereo"] = int(data.get("stereo", 0))
            data["is_conjugated"] = data.get("is_conjugated", "False") == "True"
            data["is_aromatic"] = data.get("is_aromatic", "False") == "True"
            data["in_ring"] = data.get("in_ring", "False") == "True"

        return G
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def load_graph(dir_path):
    graph_dict = {}
    for fname in os.listdir(dir_path):
        if fname.endswith('.graphml'):
            graph_id = os.path.splitext(fname)[0]
            file_path = os.path.join(dir_path, fname)
            G = load_graphml(file_path)
            pyg_data = nx_to_pyg(G, smiles="None", mol="None")
            graph_dict[graph_id] = pyg_data
    return graph_dict


if __name__ == "__main__":
    # Example usage
    graph_dict = load_graph('molecules/graphs')
    print(f"Loaded {len(graph_dict)} graphs.")