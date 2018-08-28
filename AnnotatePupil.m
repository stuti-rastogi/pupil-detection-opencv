path = '/Users/bobby/Downloads/pupil/Data/ICCV/';

files = dir([path, '*.png']);
numOfLandmarks = 2;
% numel(files)

for i = 1 :  numel(files)
    i
    imgName = files(i).name
    fullName = [path imgName];
    
    img = imread(fullName);
    figure(1); imshow(img); hold on;
    landmarks = zeros(numOfLandmarks,2);
    for j = 1 : numOfLandmarks        
        [x, y] = ginput(1);
        plot(x,y,'.g');
        landmarks(j,1) = round(x);
        landmarks(j,2) = round(y);
        j
    end
    hold off;
    str = strsplit(imgName,'.');
    txtName = [str{1}, '.txt'];
    txtFullName = [path, txtName]; 
    dlmwrite(txtFullName, landmarks);
end