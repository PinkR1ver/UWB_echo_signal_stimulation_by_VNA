function [freq, S11_amp, S21_amp, S11_phase, S21_phase] = S2P_read(file)

    data = readmatrix(file, 'NumHeaderLines', 5, 'Delimiter', '\t', 'OutputType', 'matrix');
    header = ["Frequency", "S11_amp", "S11_phase", "S21_amp", "S21_phase", "S12_amp", "S12_phase", "S22_amp", "S22_phase"];
    df = array2table(data, 'VariableNames', header);

    freq = df.Frequency;
    S11_amp = df.S11_amp;
    S21_amp = df.S21_amp;
    S11_phase = df.S11_phase;
    S21_phase = df.S21_phase;

end
