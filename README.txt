-------------------------------
Instructions
-------------------------------
1.install pandas if you do not have it in your python setup. Run "pip install pandas"

2.There are 2 versions of the script. They are namely PkCleanse.py and PkCleanse.ipynb. Both are the same, the latter being the Jupyter Notebook version/format. The former you can run with the Python 3 interpreter.

3.Deploy the Pakistan Largest Ecommerce Dataset.csv and the .py or .ipynb file in the same folder.

4.Script throws out some output on the screen. You may pipe the output to a file e.g. "python PkCleanse.py > PkCleanse.out.txt". Alternatively, you may omit the "> PkCleanse.out.txt" to have the script output shown on the screen

5.The script is commented within to explain the steps.

6.The script generates 3 files as an output. 
-A Exception report which gives all the detected data quality issues and their details, Exception_Report.csv 
-The final cieansed file data_cleansed.csv
-The MV reconciliation report data_mv_mismatch_report.csv which gives the rows where the MV is analysed to be of questionable data quality. Note, the records in this file is not omitted from the cleansed file as it constitute a huge amount of the total data and moreover, we have decided that we will focus on other features within the dataset for analysis and escalate this finding to the client. The assumption is we can trust the grand total column for now and will not look into the MV column till the data quality root cause is identify.




