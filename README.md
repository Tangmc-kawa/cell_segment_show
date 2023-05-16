# Cell_segment_show

This is a program for visualizing cell boundaries of a spatial transcriptome data with a convex hull algorithm or image closing. The data consists of a set of points with specific indexes which represents different cells.

## Quickstart

### Create environment using conda or pip

```powershell
conda create --name <env_name> --file requirements.txt
pip install -r requirements.txt
```

### Example input

We expect a csv file with columns "x_in_pix", "y_in_pix", "z_in_pix" and "Cell Index" which represents the x, y, z position of rna points in cell with specific index.

| x_in_pix | y_in_pix | z_in_pix | Cell Index |
| -------- | -------- | -------- | ---------- |
| 1343     | 333      | 23       | 1          |
| 1336     | 367      | 24       | 2          |
| 1552     | 1483     | 16       | 4          |
| 1377     | 343      | 18       | 1          |

The position of rnas belonging to each cell will be converted to a 3d array where each point represents a rna and the point's value represents cell index. The index will be the gray scale of output 3d tif file.

If the 3d tif file is ready, you can read the tif file as a 3d array and perform convex hull on the array algorithm directly.
