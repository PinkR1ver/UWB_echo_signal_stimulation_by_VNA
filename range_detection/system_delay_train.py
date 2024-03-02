import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from sklearn.model_selection import train_test_split
import random
from rich.progress import track

if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'signal', 'train.csv')
    
    dataset = pd.read_csv(data_path)

    test_set_offset_global = []
    train_set_offset_global = []
    all_set_offset_global = []
    sample_global = []
    t0_predict_global = []
    
    for i in track(range(1000), description='Training...'):
        
        train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=random.randint(0, 100))
         
        t0_list = []
        
        for index, row in train_set.iterrows():
            
            t0 = row['t0']
            t0_list.append(t0)
            
        t0_predict = np.mean(t0_list)
        t0_predict_global.append(t0_predict)
        
        offset_list = []
        
        for index, row, in test_set.iterrows():
            
            offset = abs(row['t0'] - t0_predict) / row['t0']
            offset_list.append(offset)
            
        test_set_offset_global.append(np.mean(offset_list))
        
        offset_list = []
        for index, row in train_set.iterrows():
            
            offset = abs(row['t0'] - t0_predict) / row['t0']
            offset_list.append(offset)
        
        train_set_offset_global.append(np.mean(offset_list))
        
        offset_list = []
        for index, row in dataset.iterrows():
            
            offset = abs(row['t0'] - t0_predict) / row['t0']
            offset_list.append(offset)
        
        all_set_offset_global.append(np.mean(offset_list))
        
        sample_global.append(train_set.distance.values)
        
    best_point = np.argmin(all_set_offset_global)
    t0 = t0_predict_global[best_point]
    
    print(f'Best t0: {t0_predict_global[best_point]:.2e}s')
    print(f'Best offset in allset: {all_set_offset_global[best_point] * 100:.2f}%')
    print(f'Best offset in trainset: {train_set_offset_global[best_point] * 100:.2f}%')
    print(f'Best offset in testset: {test_set_offset_global[best_point] * 100:.2f}%')
    print(f'Best sample: {sample_global[best_point]}')
    print()
    
    # plot distance graph
    
    distance_list = []
    predict_distance_list = []
    offset_list = []
    
    for index, row in train_set.iterrows():
        
        predict_distance = (row['t2'] - t0) * 3e8 / 2 * 100
        distance = row['distance']
        offset = abs(distance - predict_distance) / distance
        
        distance_list.append(distance)
        predict_distance_list.append(predict_distance)
        offset_list.append(offset)
        
    print(f'Best offset in TrainSet: {np.mean(offset_list) * 100:.2f}%')
    
    distance_list = []
    predict_distance_list = []
    offset_list = []
    
    for index, row in test_set.iterrows():
        
        predict_distance = (row['t2'] - t0) * 3e8 / 2 * 100
        distance = row['distance']
        offset = abs(distance - predict_distance) / distance
        
        distance_list.append(distance)
        predict_distance_list.append(predict_distance)
        offset_list.append(offset)
        
    print(f'Best offset in TestSet: {np.mean(offset_list) * 100:.2f}%')
    
    distance_list = []
    predict_distance_list = []
    offset_list = []
    
    for index, row in dataset.iterrows():
        
        predict_distance = (row['t2'] - t0) * 3e8 / 2 * 100
        distance = row['distance']
        offset = abs(distance - predict_distance) / distance
        
        distance_list.append(distance)
        predict_distance_list.append(predict_distance)
        offset_list.append(offset)
        
    print(f'Best offset in AllSet: {np.mean(offset_list) * 100:.2f}%')
        
    # plot distance and predict distance to see the difference
    plt.plot(distance_list, predict_distance_list, 'o')
    plt.plot([0, 100], [0, 100], 'r')
    plt.xlabel('Distance(cm)')
    plt.ylabel('Predict Distance(cm)')
    plt.title('Predict Distance vs Distance')
    plt.show()
    
    for distance in distance_list:
        
        print(f'{distance} cm: {predict_distance_list[distance_list.index(distance)]:.2f} cm')

    
    # save t0
    t0_df = pd.DataFrame({'t0': [t0]})
    t0_df.to_csv(os.path.join(base_path, 'signal', 't0.csv'), index=False)
        
        