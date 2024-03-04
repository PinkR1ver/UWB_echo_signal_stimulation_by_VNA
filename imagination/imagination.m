clear all;clc;close all;

file_path = './signal/signal.xlsx';
signal = readmatrix(file_path);

signal = signal(2:end,:); % delete first row
t = signal(:, 1); % get t
mc_signal = signal(:,2); % get mutual coupling signal

signal = signal(:, 3:end);

index = 1:25;
index = num2cell(index);

center_index = 13;
distance = 10 * 1e-2; % 10cm
speed = 3e8; % speed of light

gif_control = 0;

x_location = [0, 50, 100, 150, 200, 200, 150, 100, 50, 0, 0, 50, 100, 150, 200, 200, 150, 100, 50, 0, 0, 50, 100, 150, 200];
y_location = [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 200, 200, 200, 200, 200];
location = [x_location * 1e-3; y_location * 1e-3]';

Xbeg = 0; Xend = 0.2;
Ybeg = 0; Yend = 0.2;
Zbeg = 0; Zend = 0.2;



center_signal = signal(:, center_index) - mc_signal;

[~, peak_location] = max(center_signal);

% plot center signal
figure;
plot(t, center_signal);
hold on;
plot(t(peak_location), center_signal(peak_location), 'r*');
xlabel('Time (s)');
ylabel('Amplitude');
title('Center Signal');
legend('Center Signal', 'Peak Location');
hold off;

t2 = (t(peak_location) + t(peak_location + 1)) / 2;
t1 = distance * 2 / speed;
t0 = t2 - t1;

Nx = 100;
Ny = 100;
Nz = 100;
x_gird = linspace(Xbeg, Xend, Nx);
y_gird = linspace(Ybeg, Yend, Ny);
z_gird = linspace(Zbeg, Zend, Nz);


% imagination

image = zeros(Nx, Ny, Nz);

for i = 1:length(index)
    
    signal(:, i) = signal(:, i) - mc_signal;

    for nx = 1:Nx
        for ny = 1:Ny
            for nz = 1:Nz

                x = x_gird(nx);
                y = y_gird(ny);
                z = z_gird(nz);
                r = sqrt((x - location(i, 1))^2 + (y - location(i, 2))^2 + z^2);
                ft = r * 2 / speed; % ft: flight time
                ft = ft + t0;

                index = floor(ft / (t(2) - t(1)));
                image(nx, ny, nz) = image(nx, ny, nz) + signal(index, i);

            end
        end
    end

end

% plot image slice

% get range

max = max(max(max(image)));
min = min(min(min(image)));

for i = 48:52
    figure;
    imagesc(x_gird, y_gird, image(:, :, i));
    xlabel('X (m)');
    ylabel('Y (m)');
    title(['Z = ', num2str(z_gird(i)), 'm'])
    clim([min, max]);
    colormap('jet');
    colorbar;
end


% make this image to a .gif


if gif_control == 1

    for i = 1:Nz
        figure;
        imagesc(x_gird, y_gird, image(:, :, i));
        xlabel('X (m)');
        ylabel('Y (m)');
        title(['Z = ', num2str(z_gird(i)), 'm'])
        clim([min, max]);
        colormap('jet');
        colorbar;
        frame = getframe(gcf);
        im = frame2im(frame);
        [imind, cm] = rgb2ind(im, 256);
        if i == 1
            imwrite(imind, cm, 'image.gif', 'gif', 'Loopcount', inf, 'DelayTime', 0.1);
        else
            imwrite(imind, cm, 'image.gif', 'gif', 'WriteMode', 'append', 'DelayTime', 0.1);
        end
        close;
    end
   
end


% plot 3D image, the +-0.5% of the max value isosurface

figure
isosurface(x_gird, y_gird, z_gird, image, -0.05);
xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');
title('3D Image');
colormap('jet');
colorbar;





