import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from rich.progress import track
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def logmag2liner(x):
    return 10 ** (x/20)


if __name__ == '__main__':
    
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'data', 'exp02')
    
    labels = []
    S21_amp_spectrum = []
    S11_amp_spectrum = []
    S21_phase_spectrum = []
    
    ref_df = pd.read_csv(os.path.join(base_path, 'ref', 'eject_gaussian_pulse_freq_amp_pair.csv'), skiprows=1, names=['freq', 'amp', 'phase'])
    
    amp_ref = ref_df['amp'].values
    
    for root, dirs, files in os.walk(data_path):  
        
        files.sort()
        
        for file in files:
            if 'S2P' in file:
                
                df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                
                frequencies = df['Frequency'].values
                S21_amp = df['S21_amp'].values    
                S11_amp = df['S11_amp'].values
                S21_phase = df['S21_phase'].values
                label = file.split('.')[0]
                
                if label.isdigit():
                    label = label + 'cm'
                labels.append(label)
                
                S21_amp_spectrum.append(S21_amp)
                S11_amp_spectrum.append(S11_amp)
                S21_phase_spectrum.append(S21_phase)
                    


    plt.figure(figsize=(5, 10))
    
    for amp_spectrum_S21, amp_spectrum_S11, label in zip(S21_amp_spectrum, S11_amp_spectrum, labels):
        plt.subplot(4, 1, 1)
        plt.plot(frequencies, amp_spectrum_S21, label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude(dB)')
        plt.title('S21 Magnitude Log Scale')
        plt.legend()
        
        plt.subplot(4, 1, 2)
        plt.plot(frequencies, np.vectorize(logmag2liner)(amp_spectrum_S21), label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.title('S21 Magnitude Linear')
        plt.legend()
        
        plt.subplot(4, 1, 3)
        plt.plot(frequencies, amp_spectrum_S11, label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude(dB)')
        plt.title('S11 Magnitude Log Scale')
        plt.legend()
        
        plt.subplot(4, 1, 4)
        plt.plot(frequencies, np.vectorize(logmag2liner)(amp_spectrum_S11), label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.title('S11 Magnitude Linear')
        plt.legend()
        
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(10, 8))
    
    for amp_spectrum_S21, amp_spectrum_S11, label in zip(S21_amp_spectrum, S11_amp_spectrum, labels):
        plt.plot(frequencies, np.vectorize(logmag2liner)(amp_spectrum_S21) * amp_ref, label=label)
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.title('S21 Magnitude Linear Multiplied by Gaussian Pulse Adjust Factor')
        plt.legend()
        
    plt.tight_layout()
    plt.show()
    
    
    plt.figure(figsize=(10, 8))
    
    for i in range(len(S21_amp_spectrum)):
        
        S21_init = np.vectorize(logmag2liner)(S21_amp_spectrum[-1]) * amp_ref
        S21 = np.vectorize(logmag2liner)(S21_amp_spectrum[i]) * amp_ref
        
        S21 = S21 - S21_init
        
        # S21[S21 <= 0] = 0
        
        plt.plot(frequencies, S21, label=labels[i])
    
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.title('S21 Magnitude Linear - S21 initial')
    plt.legend()
    plt.show()
    
    AUC_list = []
    
    for i in range(len(S21_amp_spectrum) - 1):
        
        S21_init = np.vectorize(logmag2liner)(S21_amp_spectrum[-1]) * amp_ref
        S21 = np.vectorize(logmag2liner)(S21_amp_spectrum[i]) * amp_ref
        
        S21 = S21 - S21_init
        
        AUC = np.trapz(S21, frequencies)
        AUC_list.append(AUC)
        
    # plot AUC bar plot
    plt.figure(figsize=(10, 8))
    plt.bar(labels[:-1], AUC_list)
    plt.xlabel('Distance(cm)')
    plt.ylabel('AUC')
    plt.title('S21 Amp AUC vs Distance')
    plt.show()
    
    print('AUC_list: ', AUC_list / np.max(AUC_list))
    
    y = AUC_list / np.max(AUC_list)
    x = np.array([float(label[:-2]) for label in labels[:-1]])
    
    # Define the pipeline for polynomial regression
    model = make_pipeline(PolynomialFeatures(), LinearRegression())

    # Define the hyperparameters to search over
    params = {'polynomialfeatures__degree': np.arange(1, 6)}
    
    # Perform grid search to find the best order (degree)
    grid_search = GridSearchCV(model, param_grid=params, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(x.reshape(-1, 1), y)

    # Get the best order and best model
    best_degree = grid_search.best_params_['polynomialfeatures__degree']
    best_model = grid_search.best_estimator_

    # Fit the best model and predict using the entire dataset
    best_model.fit(x.reshape(-1, 1), y)
    y_pred = best_model.predict(x.reshape(-1, 1))

    # Calculate assessment parameters
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    x_fit = np.linspace(5, 40, 100)
    y_fit = best_model.predict(x_fit.reshape(-1, 1))
    
    coefficients = best_model.named_steps['linearregression'].coef_
    
    plt.figure(figsize=(10, 8))
    plt.scatter(x, y, label='orginal data')
    plt.plot(x_fit, y_fit, label='Best Fit (Degree {})'.format(best_degree))
    
    plt.text(30, 0.85, 'MSE = {:.6f}'.format(mse), fontsize=12)
    plt.text(30, 0.80, 'R2 = {:.6f}'.format(r2), fontsize=12)
    plt.text(10, best_model.predict(np.array([10]).reshape(-1, 1)) + 0.05, 'y = {:.6f}x^3 + {:.6f}x^2 + {:.6f}x'.format(coefficients[3], coefficients[2], coefficients[1]), fontsize=12)
    
    plt.legend()
    plt.xlabel('Distance(cm)')
    plt.ylabel('AUC')
    plt.title('S21 Amp AUC vs Distance fitting curve')
    plt.show()
    
    print('Best Degree:', best_degree)
    print('Mean Squared Error:', mse)
    print('R-squared Score:', r2)
    print(grid_search.best_estimator_.named_steps['linearregression'].coef_)
        
    
    
    # ----- Generating Receiving Signal -----
    
    t = np.linspace(0, 1e-6, int(1e5))
    
    signal = np.zeros(len(t))
    
    plt.figure(figsize=(10, 15))
    
    index = 1
    y_max = -np.inf
    y_min = np.inf
    peak_list = []

    for amp_spectrum_S21, amp_phase_S21, label in zip(S21_amp_spectrum, S21_phase_spectrum, labels):
            
        signal = np.zeros(len(t))
        
        amp_spectrum_S21 = np.vectorize(logmag2liner)(amp_spectrum_S21)
        amp_spectrum_S21 = amp_spectrum_S21 * amp_ref
        amp_spectrum_S21 = amp_spectrum_S21 - S21_init
        
        for amp, phase, freq in track(zip(amp_spectrum_S21, amp_phase_S21, frequencies), description='generating receving signal for {}...'.format(label), total=len(amp_spectrum_S21)):
            component = amp * np.cos(2 * np.pi * freq * t + phase)
            
            signal += component
        
        plt.subplot(9, 1, index)  
        index += 1
        
        y_max = max(np.max(signal / len(frequencies)), y_max)
        y_min = min(np.min(signal / len(frequencies)), y_min)
        
        peak_list.append(np.max(signal / len(frequencies)) - np.min(signal / len(frequencies)))
        
        
        plt.plot(t, signal / len(frequencies), label=label)
        plt.title('Receiving signal for distance {}'.format(label))
        plt.legend()
        plt.ylabel('Magnitude')
    
    plt.xlabel('Time (s)')
    plt.tight_layout()
    
    for i in range(1, 10):
        plt.subplot(9, 1, i)
        plt.ylim(y_min * 1.05, y_max * 1.05)
    
    plt.savefig(os.path.join(base_path, 'fig', 'receiving_signal.png'), dpi=1000)
    plt.close()
    
    print(peak_list)
    
    # peak-list bar plot
    
    plt.figure(figsize=(10, 8))
    plt.bar(labels, peak_list)
    plt.xlabel('Distance(cm)')
    plt.ylabel('Peak-Peak Value')
    plt.title('Receiving Signal Peak Value vs Distance')
    plt.show()
            
        
        

    
    
    
    
        
    
    