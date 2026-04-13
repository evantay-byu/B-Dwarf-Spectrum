import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv("UltracoolSheetMain.csv")

keep_cols = [
    "name", "name_simbadable",
    "ra_j2000_formula", "dec_j2000_formula"
]
keep_cols = [c for c in keep_cols if c in df.columns]
df_small = df[keep_cols].copy()
df_small = df_small.dropna(subset=["ra_j2000_formula", "dec_j2000_formula"])

# Your six high-priority targets (match to the same column you’ll use below)
high_priority_names = {
    "SDSS J090900.73+652527.2",
    "SDSS J075840.33+324723.4",
    "2MASS J11220826-3512363",
    "SDSS J104829.21+091937.8",
    "SDSS J143553.25+112948.6",
    "SDSS J011912.22+240331.6",
}

# Quick sanity check: which of these are actually present in df_small["name"]
present_priorities = set(df_small["name"]).intersection(high_priority_names)
print("High-priority stars in catalog:", present_priorities)

ra_bins = 36
dec_bins = 36

H, ra_edges, dec_edges, _ = plt.hist2d(
    df_small["ra_j2000_formula"],
    df_small["dec_j2000_formula"],
    bins=[ra_bins, dec_bins]
)
plt.colorbar()
plt.show()

k = 1  # chunk index

for i in range(len(dec_edges) - 1):
    dec_min = dec_edges[i]
    dec_max = dec_edges[i + 1]

    for j in range(len(ra_edges) - 1):
        ra_min = ra_edges[j]
        ra_max = ra_edges[j + 1]

        mask = (
            (df_small["ra_j2000_formula"] >= ra_min) &
            (df_small["ra_j2000_formula"] <  ra_max) &
            (df_small["dec_j2000_formula"] >= dec_min) &
            (df_small["dec_j2000_formula"] <  dec_max)
        )
        current_chunk = df_small[mask]

        if len(current_chunk) >= 1:
            # Check if this chunk contains any of the six high-priority dwarfs
            chunk_names = set(current_chunk["name"])
            contains_priority = len(chunk_names.intersection(high_priority_names)) > 0

            # Add "priority" tag to filename if it is one of the 6 dwarfs
            suffix = "_priority" if contains_priority else ""
            outname = f"UltracoolChunk{k}{suffix}.csv"

            current_chunk.to_csv(outname, index=False)
            print(
                f"Wrote {outname} with {len(current_chunk)} objects "
                f"(priority={contains_priority})"
            )
            k += 1


### When working on this section, first iterate with i <dec <= i +1, then j < ra <= j + 1

### Write spectrophotometry tool chunk #

### Good enough practice in scientific computing