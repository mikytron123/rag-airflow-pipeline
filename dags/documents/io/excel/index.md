# Excel
Polars can read and write to Excel files from Python.
From a performance perspective, we recommend using other formats if possible, such as Parquet or CSV files.
## Read
Polars does not have a native Excel reader. Instead, it uses external libraries to parse Excel files into objects that Polars can parse. The available engines are:
* xlsx2csv: This is the current default.
* openpyxl: Typically slower than xls2csv, but can provide more flexibility for files that are difficult to parse.
* pyxlsb: For reading binary Excel files (xlsb).
* fastexcel: This reader is based on calamine and is typically the fastest reader but has fewer features than xls2csv.
Although fastexcel is not the default at this point, we recommend trying fastexcel first and using xlsx2csv or openpyxl if you encounter issues.
To use one of these engines, the appropriate Python package must be installed as an additional dependency.
 Python
```python
$ pip install xlsx2csv openpyxl pyxlsb fastexcel
```

The default Excel reader is xlsx2csv.
It is a Python library which parses the Excel file into a CSV file which Polars then reads with the native CSV reader.
We read an Excel file with `read_excel`:
 Python
 
```python
df = pl.read_excel("docs/data/path.xlsx")
```

We can specify the sheet name to read with the `sheet_name` argument. If we do not specify a sheet name, the first sheet will be read.
 Python
 
```python
df = pl.read_excel("docs/data/path.xlsx", sheet_name="Sales")
```

## Write
We need the xlswriter library installed as an additional dependency to write to Excel files.
 Python
```python
$ pip install xlsxwriter
```

Writing to Excel files is not currently available in Rust Polars, though it is possible to use this crate to write to Excel files from Rust.
Writing a `DataFrame` to an Excel file is done with the `write_excel` method:
 Python
 
```python
df = pl.DataFrame({"foo": [1, 2, 3], "bar": [None, "bak", "baz"]})
df.write_excel("docs/data/path.xlsx")
```

The name of the worksheet can be specified with the `worksheet` argument.
 Python
 
```python
df = pl.DataFrame({"foo": [1, 2, 3], "bar": [None, "bak", "baz"]})
df.write_excel("docs/data/path.xlsx", worksheet="Sales")
```

Polars can create rich Excel files with multiple sheets and formatting. For more details, see the API docs for `write_excel`.