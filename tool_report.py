import os
import sys
import pandas as pd
import numpy as np
import datetime

def get_directory_contents(target_dir):
    if os.path.exists(target_dir):
        for subdir, dirs, files in os.walk(target_dir):
            return dirs, subdir, files
    else:
        print("No data directory")
        return None, None, None


if __name__ == "__main__":

    tool = sys.argv[1]
    target_file = 'res.csv'
    services = ["features-service", "languagetool", "ncs", "news", "ocvn", "proxyprint", "restcountries", "scout-api",
            "scs", "erc20-rest-service", "genome-nexus", "person-controller", "problem-controller", "rest-study",
            "spring-batch-rest", "spring-boot-sample-app", "user-management", "cwa-verification", "market",
            "project-tracking-system"]
    
    curdir = os.getcwd()
    target_dir = curdir + '/data'

    final_df_coverage = pd.DataFrame()
    final_df_error = pd.DataFrame()

    # read all res.csv from each tool
    data_dir, data_subdir, data_file = get_directory_contents(target_dir)
    for data_content in data_dir:
        if data_content in services:
            tool_path = data_subdir + '/' + data_content
            tool_dir, tool_subdir, tool_file = get_directory_contents(tool_path)
            for tool_content in tool_dir:
                if tool_content == tool:
                    result_path = tool_subdir + '/' + tool_content
                    result_dir, result_subdir, result_file = get_directory_contents(result_path)
                    for file_name in result_file:
                        if file_name == target_file:
                            res_df = pd.read_csv(result_subdir + '/' +file_name, names = ['line', 'branch', 'method'])

                            # create error dataframe
                            error_df = res_df.tail(1).copy()
                            error_df.columns = ['error', 'unique_error', 'cruicial']
                            error_df['service'] =''
                            error_df['tool'] = ''
                            error_df['service'].iloc[0] = data_content
                            error_df['tool'].iloc[0] = tool_content
                            cols = error_df.columns.tolist()
                            cols = cols[-2:] + cols[:-2]
                            error_df = error_df[cols]

                            # process result df
                            res_df.drop(len(res_df)-1, axis= 0, inplace=True)
                            time = []
                            base = 10
                            for i in range(len(res_df)):
                                time.append(base)
                                base+=10

                            res_df['service'] =''
                            res_df['tool'] = ''
                            res_df['service'].iloc[0] = data_content
                            res_df['tool'].iloc[0] = tool_content
                            res_df['time'] = time
                            cols = res_df.columns.tolist()
                            cols = cols[-3:] + cols[:-3]
                            res_df = res_df[cols]

                            # append to final df
                            final_df_coverage = pd.concat([final_df_coverage, res_df],ignore_index=True )
                            final_df_error = pd.concat([final_df_error, error_df],ignore_index=True )
    


    today = datetime.date.today()
    path = '/home/darko/api-tester/REST_Go/'+str(tool)+'_results_'+str(today)+'.xlsx'
    writer = pd.ExcelWriter(path, engine = 'openpyxl')
    final_df_coverage.to_excel(writer,sheet_name='coverage')
    final_df_error.to_excel(writer, sheet_name='bugs')
    writer.close()

                            

                    