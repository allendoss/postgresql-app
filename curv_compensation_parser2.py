import pandas as pd
import os, json
from enum import Enum
from argparse import ArgumentParser
from unittest import TextTestRunner, TestLoader, TestCase
import numpy as np
import pathlib2
from helper import createFolder, fullPathForLocal, CurvToStandardColumnLeft, CurvToStandardColumnRight


# Following names are defined in curv
# extract right data with the right nomenclature
front_compensation_list = [
    'FOOT_TURNS_OUT',
    'KNEE_MOVES_IN',
    'KNEE_MOVES_OUT',
    'HIP_SHIFT',
    'HEEL_FOOT_RISE'
]

side_compensation_list = [
    'FORWARD_LEAN',
    'ARMS_FALL_FORWARD'
]

one_leg_squat_compensation_list = [
    'KNEE_MOVES_IN',
    'KNEE_MOVES_OUT',
    'UNCONTROLLED_TRUNK'
]


def parseCurvData(data_frame_fusionetics, assessment_type, videos_folder_path, output_folder_path):

    df_fusionetics = data_frame_fusionetics
    df_fusionetics = df_fusionetics.reset_index(drop=True)
    df_curv = df_fusionetics.copy()
    videos_folder_path = fullPathForLocal(videos_folder_path)
    compensation_col_start_index = df_curv.columns.get_loc('URL') + 1
    df_curv[df_curv.columns[compensation_col_start_index:]] = np.nan
    
    for index, row in df_curv.iterrows():
        video_folder = pathlib2.Path.home().joinpath(
            videos_folder_path,
            row['ASSESSMENT_TYPE'] + '_' + row['NAME']
        )
        json_path = pathlib2.Path.home().joinpath(
            video_folder,
            'compensations.json'
        )
        try:
            with open(json_path, 'r') as f:
                data_curv = json.load(f)
        except:
            print('json file does not exist')
            continue

        if assessment_type == '2-Leg-Squat-Front-video':
            for compensation in front_compensation_list:

                compensation_right_limb = 0
                compensation_left_limb = 0

                if data_curv['compensation_results'][compensation] is not None:

                    if data_curv['compensation_results'][compensation]:
                        if any(rep['side']=='RIGHT' for rep in data_curv['compensation_results'][compensation]['indicators']):
                            compensation_right_limb = 1

                        if any(rep['side']=='LEFT' for rep in data_curv['compensation_results'][compensation]['indicators']):
                            compensation_left_limb = 1

                df_curv.loc[index, compensation+'_RIGHT_LIMB'] = compensation_right_limb
                df_curv.loc[index, compensation+'_LEFT_LIMB'] = compensation_left_limb

        if assessment_type == '2-Leg-Squat-Side-video':

            for compensation in side_compensation_list:
                temp = 0
                if data_curv['compensation_results'][compensation] is not None:
                    if data_curv['compensation_results'][compensation]['detected']:
                        temp = 1
                df_curv.loc[index, compensation] = temp

        if assessment_type == '1-Leg-Squat-Right-video':
            for compensation in one_leg_squat_compensation_list:
                temp = 0
                if compensation == 'UNCONTROLLED_TRUNK':
                    if data_curv['compensation_results']['TRUNK_FLEXION'] is not None:
                        if data_curv['compensation_results']['TRUNK_FLEXION']['detected']:
                            temp = 1
                    if data_curv['compensation_results']['TRUNK_ROTATION'] is not None:
                        if data_curv['compensation_results']['TRUNK_ROTATION']['detected']:
                            temp = 1
                    if data_curv['compensation_results']['HIP_SHIFT'] is not None:
                        if data_curv['compensation_results']['HIP_SHIFT']['detected']:
                            temp = 1
                else:
                    if data_curv['compensation_results'][compensation] is not None:
                        if data_curv['compensation_results'][compensation]['detected']:
                            temp = 1
                df_curv.loc[index, CurvToStandardColumnRight[compensation]] = temp

        if assessment_type == '1-Leg-Squat-Left-video':
            for compensation in one_leg_squat_compensation_list:
                temp = 0
                if compensation == 'UNCONTROLLED_TRUNK':
                    if data_curv['compensation_results']['TRUNK_FLEXION'] is not None:
                        if data_curv['compensation_results']['TRUNK_FLEXION']['detected']:
                            temp = 1
                    if data_curv['compensation_results']['TRUNK_ROTATION'] is not None:
                        if data_curv['compensation_results']['TRUNK_ROTATION']['detected']:
                            temp = 1
                    if data_curv['compensation_results']['HIP_SHIFT'] is not None:
                        if data_curv['compensation_results']['HIP_SHIFT']['detected']:
                            temp = 1
                else:
                    if data_curv['compensation_results'][compensation] is not None:
                        if data_curv['compensation_results'][compensation]['detected']:
                            temp = 1
                df_curv.loc[index, CurvToStandardColumnLeft[compensation]] = temp

    createFolder(output_folder_path)
    # TODO: better to drop it but will cause issues while comparing
    # 253 rows with 254 rows of another table
    df_curv = df_curv.replace(np.nan, '0')
    df_curv[df_curv.columns[compensation_col_start_index:]] = df_curv[df_curv.columns[compensation_col_start_index:]].astype(np.uint8)

    parent_directory = pathlib2.Path.cwd()
    output_file_path = pathlib2.Path.home().joinpath(
        parent_directory,
        output_folder_path,
        assessment_type+'_'+'curv.csv'
    )
    df_curv = df_curv.reset_index(drop=True)
    df_curv.to_csv(output_file_path, index=False, sep=',', encoding='utf-8')
    return df_curv
