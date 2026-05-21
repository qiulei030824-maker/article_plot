# Species configuration for PF00168 synteny analysis

SPECIES_GROUPS = {
    "cucumber": ["ChineseLong"],
    "melon": ["DHL92"],
    "watermelon": ["97103"],
    "bottle_gourd": ["USVL1VR-Ls"],
    "cucurbita": ["Cpepo","Cargyrosperma","Cmaxima_Rimu","Cmoschata_Rifu"],
    "arabidopsis": ["Athaliana"],
    "tomato": ["Slycopersicum"],
    "rice": ["Osativa"],
}

SPECIES_COLORS = {
    "ChineseLong": "#457B9D",
    "DHL92": "#1D3557",
    "97103": "#2A9D8F",
    "USVL1VR-Ls": "#E9C46A",
    "Cpepo": "#F4A261",
    "Cargyrosperma": "#E76F51",
    "Cmaxima_Rimu": "#A8DADC",
    "Cmoschata_Rifu": "#D4A373",
}

def resolve_pfam_paths(pfam_id, base_dir="/data5/qiulei/PPI"):
    import os
    paths = {
        "workdir": os.path.join(base_dir, pfam_id, "JCVI"),
        "outdir": os.path.join(base_dir, pfam_id, "03_figures"),
        "data_dir": os.path.join(base_dir, "data"),
    }
    return paths

def get_species_chain():
    return ["ChineseLong","DHL92","97103","USVL1VR-Ls","Cpepo","Cargyrosperma","Cmaxima_Rimu","Cmoschata_Rifu"]
