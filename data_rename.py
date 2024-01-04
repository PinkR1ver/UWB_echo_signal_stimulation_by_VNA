import os


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp06')
    save_path = os.path.join(base_path, 'data', 'exp06_csv')
    
    # create save_path if save_path not exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            
            # copy file to save_path with different name, name suffix is .csv
            
            if "S2P" in file:
                
                label = file.split('.')[0] + 'cm'
                
                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                    # header use tab as delimiter
                    header = "Frequency	S11_amp	S11_phase	S21_amp	S21_phase	S12_amp	S12_phase	S22_amp	S22_phase\n"
                    
                    with open(os.path.join(save_path, label + '.csv'), 'w') as f:
                        f.writelines(header)
                        f.writelines(lines[5:])
                        
