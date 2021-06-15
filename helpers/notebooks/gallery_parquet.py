# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# Show Parquet / Pyarrow API.

# %% [markdown]
# ## Imports

# %%
import logging
import os
import random

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import numpy as np

import helpers.dbg as dbg

dbg.init_logger(verbosity=logging.INFO)
_LOG = logging.getLogger(__name__)


# %%
def get_df() -> pd.DataFrame:
    """
    Create pandas random data, like:
    
                idx instr  val1  val2
    2000-01-01    0     A    99    30
    2000-01-02    0     A    54    46
    2000-01-03    0     A    85    86
    """
    num_rows = 100
    instruments = "A B C D E".split()
    cols = "id stock val1 val2".split()
    df_idx = pd.date_range(pd.Timestamp("2000-01-01"), pd.Timestamp("2000-01-15"), freq="1D")
    #print(df_idx)
    random.seed(1000)

    df = []
    for idx, inst in enumerate(instruments):
        df_tmp = pd.DataFrame({"idx": idx,
                               "instr": inst,
                               "val1": [random.randint(0, 100) for k in range(len(df_idx))],
                               "val2": [random.randint(0, 100) for k in range(len(df_idx))],
                              }, index=df_idx)
        #print(df_tmp)
        df.append(df_tmp)
    df = pd.concat(df)
    return df


# %%
def df_to_str(df: pd.DataFrame) -> str:
    txt = ""
    txt += "# df=\n%s" % df.head(3)
    txt += "\n# df.shape=\n%s" % str(df.shape)
    txt += "\n# df.dtypes=\n%s" % str(df.dtypes)
    return txt


# %% [markdown]
# # Save and load all data in one file

# %%
df = get_df()
#print(df.head())
print(df_to_str(df))

# %%
table = pa.Table.from_pandas(df)

print("table=\n%s" % table)

# %%
# Save.
file_name = "df_in_one_file.pq"
pq.write_table(table, file_name)

# %%
# Load.
df2 = pq.read_table(file_name)
print(df2)

df2 = df2.to_pandas()
print(df_to_str(df2))

# %% [markdown]
# ## Read a subset of columns

# %%
df2 = pq.read_table(file_name, columns=["idx", "val1"])
print(df2)

df2 = df2.to_pandas()
print(df_to_str(df2))

# %% [markdown]
# ## Partitioned dataset
#
# from https://arrow.apache.org/docs/python/dataset.html#reading-partitioned-data
#
# - A dataset can exploit a nested structure, where the sub-dir names hold information about which subset of the data is stored in that dir
# - E.g., "Hive" patitioning scheme "key=vale" dir names

# %%
df = get_df()
print(df_to_str(df))

# %%
base = "."
dir_name =  os.path.join(base, "parquet_dataset_partitioned")
os.system("rm -rf %s" % dir_name)

pq.write_to_dataset(table,
                    dir_name,
                    partition_cols=['idx'])

# %%
# !ls parquet_dataset_partitioned 

# %%
# Read data back.
dataset = ds.dataset(dir_name,
                     format="parquet",
                     partitioning="hive")

print("\n".join(dataset.files))

# %%
# Read everything.
df2 = dataset.to_table().to_pandas()

print(df_to_str(df2))

# %%
# Load part of the data.

df2 = dataset.to_table(filter=ds.field("idx") == 1).to_pandas()
print(df_to_str(df2))

df2 = dataset.to_table(filter=ds.field("idx") < 3).to_pandas()
print(df_to_str(df2))

# %%
df["year"] = df.index.year
df["month"] = df.index.month

df.head()

# %%
table.schema

# %%
base = "."
dir_name =  os.path.join(base, "parquet_dataset_partitioned3")
os.system("rm -rf %s" % dir_name)

pq.write_to_dataset(table,
                    dir_name,
                    partition_cols=['idx', "year", "month"])

# %%
# !ls $dir_name/idx=0/year=2000/month=1

# %%
# Read data back.
dataset = ds.dataset(dir_name,
                     format="parquet",
                     partitioning="hive")

print("\n".join(dataset.files))

# %% [markdown]
# ## Partition manually

# %%
from pyarrow.dataset import DirectoryPartitioning

partitioning = DirectoryPartitioning(pa.schema([("year", pa.int16()), ("month", pa.int8()), ("day", pa.int8())]))
print(partitioning.parse("/2009/11/3"))

#partitioning.discover()

# %% [markdown]
# ## Read subset of columns for everything

# %%
# Read data back.
dataset = ds.dataset(dir_name,
                     format="parquet",
                     partitioning="hive")

print("\n".join(dataset.files))

dataset.to_table(filter=ds.field('idx') == 2).to_pandas()

# %% [markdown]
# ## Read everything

# %%
# Read only one column.

df2 = pq.read_table("example.pq", columns=["idx", "val1"])
print(df2)

df2 = df2.to_pandas()
print(df2)

# %%
print(pa)

# %%
# We could scan manually and create the dirs manually if we don't want to add
# add a new dir.
base = "."
dir_name =  os.path.join(base, "parquet_dataset_partitioned2")
os.system("rm -rf %s" % dir_name)

grouped = df.groupby(lambda x: x.day)
for day, df_tmp in grouped:
    print(day, df_tmp)
    grouped2 = df_tmp.groupby("idx")
    for id_, df_tmp2 in grouped2:
        print(day, id_, df_tmp2)

# %%
import pyarrow.dataset as ds

import numpy as np

# %%
# How to merge PQ files

# We can filter by year, month, stock and then all save in the same dir

# %%
partitioning = 

# %%
df.schema

# %%
