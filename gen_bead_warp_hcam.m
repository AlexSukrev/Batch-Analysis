%function f = gen_bead_warp(arg1)

% this script is used to generate a bead map and corresponding warping 
% transforms based on bead images collected through the emission filter
% wheel. IRbeads are visible 750/647 channels (100nm 715/755 beads) and 
% Visbeads are visible in 647/561/488 channels (200nm beads).
% Transforms map 750/561/488 to the 647 channel.

% Updated 06_10_18 for analysis of .hdf5 files
% Colenso Speer

% paths to input and output folders
local_exp =  arg1;
acq_path = [local_exp 'acquisition/'];
base_pth = [acq_path 'bins/'];
save_pth = [acq_path 'bead_registration/'];

% set scale for image expansion
scale = 10;

% size of field in pixels
xdiv = 640*scale; 
ydiv = 640*scale; 

% pixel size in final images
nm_per_pix = 153/scale;

% axis/label/title fontsize for plots
ax_fs = 10; 
la_fs = 10;
ti_fs = 10;

% create save path
if exist(save_pth,'dir') == 0
    mkdir(save_pth)
end

% check for beads and continue if beads are found
numbeadmov = numel(dir([acq_path 'IRbead_2_*.dax']));
if numbeadmov>1

% create workspace
workspace_nm_r2 = [save_pth 'beadworkspace_region2_' num2str(scale)...
    'x.mat'];

% set file names of .hdf5 files
track_file_nms1 = dir([base_pth 'IRbead_2_*750mlist.hdf5'] );
track_file_nms2 = dir([base_pth 'IRbead_2_*647mlist.hdf5'] );
track_file_nms3 = dir([base_pth 'Visbead_2_*647mlist.hdf5'] );
track_file_nms4 = dir([base_pth 'Visbead_2_*561mlist.hdf5'] );
track_file_nms5 = dir([base_pth 'Visbead_2_*488mlist.hdf5'] );


if exist(workspace_nm_r2,'file') >= 0 
for p = 1:4
    if p == 1
        len = 1;
        % radius tolerance for matching left/right channels
        match_radius = 1*scale; 
    elseif p==2
        len = 5;
        % radius tolerance for matching left/right channels
        match_radius = 0.5*scale; 

    else
        len = length(track_file_nms1);
        % radius tolerance for matching left/right channels
        match_radius = 0.1*scale; 

    end
        

for k = 1:len
    % load in 750 mlist 
    track_file_nm = [base_pth track_file_nms1(k).name];
    disp(track_file_nm);
    % find molecules identified in frame 0
    X_value = h5read(track_file_nm,'/fr_0/x');
    Y_value = h5read(track_file_nm,'/fr_0/y');
    % resize x and y values for larger canvas
    A(k).M2_1.x = [X_value * scale];    
    A(k).M2_1.y = [Y_value * scale];    
    
    % load in 647 IRmlist 
    track_file_nm = [base_pth track_file_nms2(k).name];
    disp(track_file_nm);
    % find molecules identified in frame 24
    X_value = h5read(track_file_nm,'/fr_24/x');
    Y_value = h5read(track_file_nm,'/fr_24/y');
    % resize x and y values for larger canvas
    A(k).M2_2.x = [X_value * scale];    
    A(k).M2_2.y = [Y_value * scale];      
     
    % load in 647 Vismlist 
    track_file_nm = [base_pth track_file_nms3(k).name];
    disp(track_file_nm);
    % find molecules identified in frame 29
    X_value = h5read(track_file_nm,'/fr_29/x');
    Y_value = h5read(track_file_nm,'/fr_29/y');
    % resize x and y values for larger canvas
    A(k).M2_3.x = [X_value * scale];    
    A(k).M2_3.y = [Y_value * scale];     
            
    % load in 561 mlist 
    track_file_nm = [base_pth track_file_nms4(k).name];
    disp(track_file_nm);
    % find molecules identified in frame 54
    X_value = h5read(track_file_nm,'/fr_54/x');
    Y_value = h5read(track_file_nm,'/fr_54/y');
    % resize x and y values for larger canvas
    A(k).M2_4.x = [X_value * scale];    
    A(k).M2_4.y = [Y_value * scale];      
    
    % load in 488 mlist 
    track_file_nm = [base_pth track_file_nms5(k).name];
    disp(track_file_nm);
    % find molecules identified in frame 100
    X_value = h5read(track_file_nm,'/fr_100/x');
    Y_value = h5read(track_file_nm,'/fr_100/y');
    % resize x and y values for larger canvas
    A(k).M2_5.x = [X_value * scale];    
    A(k).M2_5.y = [Y_value * scale];    
    
    % Find all molecules in the canvas space
    A(k).set488_inds = find([A(k).M2_5.x]>0 & [A(k).M2_5.x]<=xdiv &...
        [A(k).M2_5.y]<=ydiv);
    A(k).set488_pos.x = double([A(k).M2_5.x(A(k).set488_inds)]);
    A(k).set488_pos.y = double([A(k).M2_5.y(A(k).set488_inds)]);
    
    A(k).set561_inds = find([A(k).M2_4.x]>0 & [A(k).M2_4.x]<=xdiv &...
        [A(k).M2_4.y]<=ydiv);
    A(k).set561_pos.x = double([A(k).M2_4.x(A(k).set561_inds)]);
    A(k).set561_pos.y = double([A(k).M2_4.y(A(k).set561_inds)]);
    
    A(k).setV647_inds = find([A(k).M2_3.x]>0 & [A(k).M2_3.x]<=xdiv &...
        [A(k).M2_3.y]<=ydiv);
    A(k).setV647_pos.x = double([A(k).M2_3.x(A(k).setV647_inds)]);
    A(k).setV647_pos.y = double([A(k).M2_3.y(A(k).setV647_inds)]);
    
    A(k).set647_inds = find([A(k).M2_2.x]>0 & [A(k).M2_2.x]<=xdiv &...
        [A(k).M2_2.y]<=ydiv);
    A(k).set647_pos.x = double([A(k).M2_2.x(A(k).set647_inds)]);
    A(k).set647_pos.y = double([A(k).M2_2.y(A(k).set647_inds)]);
    
    A(k).set750_inds = find([A(k).M2_1.x]>0 & [A(k).M2_1.x]<=xdiv &...
        [A(k).M2_1.y]<=ydiv);
    A(k).set750_pos.x = double([A(k).M2_1.x(A(k).set750_inds)]);
    A(k).set750_pos.y = double([A(k).M2_1.y(A(k).set750_inds)]);
    
    % make new transform variables
    if p==1
         tform_750start = maketform('affine',[1 0 0; 0 1 0;0 0 1]);
         tform_561start = maketform('affine',[1 0 0; 0 1 0;0 0 1]);
         tform_488start = maketform('affine',[1 0 0; 0 1 0;0 0 1]);
    else
        tform_750start = tform_750_2_647;
        tform_561start = tform_561_2_647;
        tform_488start = tform_488_2_647;
    end

    % run corr_mols script
    [A(k).matched750,A(k).unmatched750] = corr_mols(A(k).set750_pos,...
        A(k).set647_pos,tform_750start,match_radius);
    
    [A(k).matched561,A(k).unmatched561] = corr_mols(A(k).set561_pos,...
        A(k).setV647_pos,tform_561start,match_radius);
    
    [A(k).matched488,A(k).unmatched488] = corr_mols(A(k).set488_pos,...
        A(k).setV647_pos,tform_488start,match_radius);
    
    % display the bead matching efficacy
     disp([num2str(length(A(k).matched750.set1_inds)) '/' ...
        num2str((2*length(A(k).matched750.set1_inds) ...
        +length(A(k).unmatched750.set1_inds)+ ...
        length(A(k).unmatched750.set2_inds))/2) ' 750 molecules matched'])
        disp(['bead image number' num2str(k)])
     
          disp([num2str(length(A(k).matched561.set1_inds)) '/' ...
        num2str((2*length(A(k).matched561.set1_inds) ...
        +length(A(k).unmatched561.set1_inds)+ ...
        length(A(k).unmatched561.set2_inds))/2) ' 561 molecules matched'])
        disp(['bead image number' num2str(k)])
        
          disp([num2str(length(A(k).matched488.set1_inds)) '/' ...
        num2str((2*length(A(k).matched488.set1_inds) ...
        +length(A(k).unmatched488.set1_inds)+ ...
        length(A(k).unmatched488.set2_inds))/2) ' 488 molecules matched'])
        disp(['bead image number' num2str(k)])
        
    % return matched molecules, set1
    A(k).S750_1.x = ...
        A(k).M2_1.x(A(k).set750_inds(A(k).matched750.set1_inds)); 
    A(k).S750_1.y = ...
        A(k).M2_1.y(A(k).set750_inds(A(k).matched750.set1_inds)); 
    % return matched molecules, set2
    A(k).S750_2.x = ...
        A(k).M2_2.x(A(k).set647_inds(A(k).matched750.set2_inds)); 
    A(k).S750_2.y = ...
        A(k).M2_2.y(A(k).set647_inds(A(k).matched750.set2_inds));

    % return matched molecules, set1
    A(k).S561_1.x = ...
        A(k).M2_4.x(A(k).set561_inds(A(k).matched561.set1_inds)); 
    A(k).S561_1.y = ...
        A(k).M2_4.y(A(k).set561_inds(A(k).matched561.set1_inds)); 
    % return matched molecules, set2
    A(k).S561_2.x = ...
        A(k).M2_3.x(A(k).setV647_inds(A(k).matched561.set2_inds)); 
    A(k).S561_2.y = ...
        A(k).M2_3.y(A(k).setV647_inds(A(k).matched561.set2_inds)); 

    % return matched molecules, set1
    A(k).S488_1.x = ...
        A(k).M2_5.x(A(k).set488_inds(A(k).matched488.set1_inds)); 
    A(k).S488_1.y = ...
        A(k).M2_5.y(A(k).set488_inds(A(k).matched488.set1_inds)); 
    % return matched molecules, set2
    A(k).S488_2.x = ...
        A(k).M2_3.x(A(k).setV647_inds(A(k).matched488.set2_inds)); 
    A(k).S488_2.y = ...
        A(k).M2_3.y(A(k).setV647_inds(A(k).matched488.set2_inds)); 

end

% group together into two big sets
comb_set750_1_pos.x = []; % set1 = left channel (pixel units)
comb_set750_1_pos.y = []; 
comb_set750_2_pos.x = []; % set2 = right channel (pixel units)
comb_set750_2_pos.y = [];

comb_set561_1_pos.x = []; % set1 = left channel (pixel units)
comb_set561_1_pos.y = []; 
comb_set561_2_pos.x = []; % set2 = right channel (pixel units)
comb_set561_2_pos.y = [];

comb_set488_1_pos.x = []; % set1 = left channel (pixel units)
comb_set488_1_pos.y = []; 
comb_set488_2_pos.x = []; % set2 = right channel (pixel units)
comb_set488_2_pos.y = [];

for k = 1:length(A)
    try
        comb_set750_1_pos.x = double(cat(1,comb_set750_1_pos.x,...
            A(k).S750_1(:).x));
        comb_set750_1_pos.y = double(cat(1,comb_set750_1_pos.y,...
            A(k).S750_1(:).y));
        comb_set750_2_pos.x = double(cat(1,comb_set750_2_pos.x,...
            A(k).S750_2(:).x));
        comb_set750_2_pos.y = double(cat(1,comb_set750_2_pos.y,...
            A(k).S750_2(:).y));
    catch
    end
end

for k = 1:length(A)
    try
        comb_set561_1_pos.x = double(cat(1,comb_set561_1_pos.x,...
            A(k).S561_1(:).x));
        comb_set561_1_pos.y = double(cat(1,comb_set561_1_pos.y,...
            A(k).S561_1(:).y));
        comb_set561_2_pos.x = double(cat(1,comb_set561_2_pos.x,...
            A(k).S561_2(:).x));
        comb_set561_2_pos.y = double(cat(1,comb_set561_2_pos.y,...
            A(k).S561_2(:).y));
    catch
    end
end

for k = 1:length(A)
    try
        comb_set488_1_pos.x = double(cat(1,comb_set488_1_pos.x,...
            A(k).S488_1(:).x));
        comb_set488_1_pos.y = double(cat(1,comb_set488_1_pos.y,...
            A(k).S488_1(:).y));
        comb_set488_2_pos.x = double(cat(1,comb_set488_2_pos.x,...
            A(k).S488_2(:).x));
        comb_set488_2_pos.y = double(cat(1,comb_set488_2_pos.y,...
            A(k).S488_2(:).y));
    catch
    end
end

% find mapping from set2 (right) onto set1 (left), save tform_right2left
set750_1_points = [comb_set750_1_pos.x comb_set750_1_pos.y];
set750_2_points = [comb_set750_2_pos.x comb_set750_2_pos.y];

set561_1_points = [comb_set561_1_pos.x comb_set561_1_pos.y];
set561_2_points = [comb_set561_2_pos.x comb_set561_2_pos.y];

set488_1_points = [comb_set488_1_pos.x comb_set488_1_pos.y];
set488_2_points = [comb_set488_2_pos.x comb_set488_2_pos.y];

if p==1
     tform_750_2_647 = cp2tform((set750_1_points),(set750_2_points),...
         'similarity');
else
try
    polyorder_R2L = 4;
    tform_750_2_647 = cp2tform(set750_1_points,set750_2_points,...
        'polynomial',polyorder_R2L);
    catch
        try
        polyorder_R2L = 3;
        tform_750_2_647 = cp2tform(set750_1_points,set750_2_points,...
            'polynomial',polyorder_R2L);
        catch
        polyorder_R2L = 2;
        tform_750_2_647 = cp2tform(set750_1_points,set750_2_points,...
            'polynomial',polyorder_R2L);
        try
        tform_750_2_647 = cp2tform((set750_1_points),(set750_2_points),...
            'similarity');
        end
    end
end
end

if p==1
     tform_561_2_647 = cp2tform((set561_1_points),(set561_2_points),...
         'similarity');
else
try
    polyorder_R2L = 4;
    tform_561_2_647 = cp2tform(set561_1_points,set561_2_points,...
        'polynomial',polyorder_R2L);
    catch
        try
        polyorder_R2L = 3;
        tform_561_2_647 = cp2tform(set561_1_points,set561_2_points,...
            'polynomial',polyorder_R2L);
        catch
        polyorder_R2L = 2;
        tform_561_2_647 = cp2tform(set561_1_points,set561_2_points,...
            'polynomial',polyorder_R2L);
        try
        tform_561_2_647 = cp2tform((set561_1_points),(set561_2_points),...
            'similarity');
        end
    end
end
end

if p==1
     tform_488_2_647 = cp2tform((set488_1_points),(set488_2_points),...
         'similarity');
else
try
    polyorder_R2L = 4;
    tform_488_2_647 = cp2tform(set488_1_points,set488_2_points,...
        'polynomial',polyorder_R2L);
    catch
        try
        polyorder_R2L = 3;
        tform_488_2_647 = cp2tform(set488_1_points,set488_2_points,...
            'polynomial',polyorder_R2L);
        catch
        polyorder_R2L = 2;
        tform_488_2_647 = cp2tform(set488_1_points,set488_2_points,...
            'polynomial',polyorder_R2L);
        try
        tform_488_2_647 = cp2tform((set488_1_points),(set488_2_points),...
            'similarity');
        end
    end
end
end

[warped_set750_2_pos.x,warped_set750_2_pos.y] = ...
    tforminv(tform_750_2_647,comb_set750_2_pos.x,comb_set750_2_pos.y);
[warped_set561_2_pos.x,warped_set561_2_pos.y] = ...
    tforminv(tform_561_2_647,comb_set561_2_pos.x,comb_set561_2_pos.y);
[warped_set488_2_pos.x,warped_set488_2_pos.y] = ...
    tforminv(tform_488_2_647,comb_set488_2_pos.x,comb_set488_2_pos.y);

set750_2_warp_error_x = comb_set750_1_pos.x - warped_set750_2_pos.x;
set750_2_warp_error_y = comb_set750_1_pos.y - warped_set750_2_pos.y;
std_set750_2_warp_error_x = std(set750_2_warp_error_x);
std_set750_2_warp_error_y = std(set750_2_warp_error_y);
std_total750_warp_error = std(sqrt(set750_2_warp_error_x.^2 + ...
    set750_2_warp_error_y.^2));

set750_2_orig_error_x = comb_set750_1_pos.x - comb_set750_2_pos.x ;
set750_2_orig_error_y = comb_set750_1_pos.y - comb_set750_2_pos.y;
std_set750_2_orig_error_x = std(set750_2_orig_error_x);
std_set750_2_orig_error_y = std(set750_2_orig_error_y);

set561_2_warp_error_x = comb_set561_1_pos.x - warped_set561_2_pos.x;
set561_2_warp_error_y = comb_set561_1_pos.y - warped_set561_2_pos.y;
std_set561_2_warp_error_x = std(set561_2_warp_error_x);
std_set561_2_warp_error_y = std(set561_2_warp_error_y);
std_total561_warp_error = std(sqrt(set561_2_warp_error_x.^2 + ...
    set561_2_warp_error_y.^2));

set561_2_orig_error_x = comb_set561_1_pos.x - comb_set561_2_pos.x;
set561_2_orig_error_y = comb_set561_1_pos.y - comb_set561_2_pos.y;
std_set561_2_orig_error_x = std(set561_2_orig_error_x);
std_set561_2_orig_error_y = std(set561_2_orig_error_y);

set488_2_warp_error_x = comb_set488_1_pos.x - warped_set488_2_pos.x;
set488_2_warp_error_y = comb_set488_1_pos.y - warped_set488_2_pos.y;
std_set488_2_warp_error_x = std(set488_2_warp_error_x);
std_set488_2_warp_error_y = std(set488_2_warp_error_y);
std_total488_warp_error = std(sqrt(set488_2_warp_error_x.^2 + ...
    set488_2_warp_error_y.^2));

set488_2_orig_error_x = comb_set488_1_pos.x - comb_set488_2_pos.x;
set488_2_orig_error_y = comb_set488_1_pos.y - comb_set488_2_pos.y;
std_set488_2_orig_error_x = std(set488_2_orig_error_x);
std_set488_2_orig_error_y = std(set488_2_orig_error_y);

[cdf750(p).y, cdf750(p).x] = ecdf(nm_per_pix*...
    sqrt(set750_2_warp_error_x.^2 + set750_2_warp_error_y.^2));
cdf90_750 = (cdf750(p).x(find(cdf750(p).y>0.9,1,'first')));
disp(['90% of 750 beads aligned to ' num2str(cdf90_750) 'nm ,using ' ...
    num2str(length(set750_1_points(:,1))) ' beads'])

[cdf488(p).y, cdf488(p).x] = ecdf(nm_per_pix*...
    sqrt(set488_2_warp_error_x.^2 + set488_2_warp_error_y.^2));
cdf90_488 = (cdf488(p).x(find(cdf488(p).y>0.9,1,'first')));
disp(['90% of 488 beads aligned to ' num2str(cdf90_488) 'nm ,using ' ...
    num2str(length(set488_1_points(:,1))) ' beads'])

[cdf561(p).y, cdf561(p).x] = ecdf(nm_per_pix*...
    sqrt(set561_2_warp_error_x.^2 + set561_2_warp_error_y.^2));
cdf90_561 = (cdf561(p).x(find(cdf561(p).y>0.9,1,'first')));
disp(['90% of 561 beads aligned to ' num2str(cdf90_561) 'nm ,using ' ...
    num2str(length(set561_1_points(:,1))) ' beads'])
end

% save transform data
save(workspace_nm_r2,'tform_750_2_647','tform_561_2_647',...
    'tform_488_2_647');
end
end

% save output plots to demonstrate goodness of fit
if exist([save_pth 'Cumulative_distribution_for_registration_self.tif'],...
        'file') == 0

% plot deviations due to chromatic abberation
figure(1); clf
set(gcf,'position',[493 441 1512 882])
%fac = 2;
fac = 20;
subplot(2,3,2)
hold on
if numbeadmov>1
plot(comb_set561_2_pos.x,comb_set561_2_pos.y,'g.')
quiver(comb_set561_2_pos.x,comb_set561_2_pos.y,fac*...
    set561_2_orig_error_x,fac*set561_2_orig_error_y,0,'r');
axis ij
set(gca,'fontsize',ax_fs)
xlabel('x axis [pixel]','fontsize',la_fs)
ylabel('y axis [pixel]','fontsize',la_fs)
title(['561 to 647, no warping ' num2str(fac) 'x mag. residuals' ],...
    'fontsize',ti_fs)
hold off
xlim([-10 640*scale]); ylim([-20 640*scale])

%fac = 2;
fac = 20;
subplot(2,3,1)
hold on
plot(comb_set488_2_pos.x,comb_set488_2_pos.y,'g.')
quiver(comb_set488_2_pos.x,comb_set488_2_pos.y,fac*...
    set488_2_orig_error_x,fac*set488_2_orig_error_y,0,'r');
axis ij
set(gca,'fontsize',ax_fs)
xlabel('x axis [pixel]','fontsize',la_fs)
ylabel('y axis [pixel]','fontsize',la_fs)
title(['488 to 647, no warping ' num2str(fac) 'x mag. residuals' ],...
    'fontsize',ti_fs)
xlim([-10 640*scale]); ylim([-20 640*scale])

fac = 20;
subplot(2,3,5)
hold on
plot(comb_set561_2_pos.x,comb_set561_2_pos.y,'g.')
quiver(comb_set561_2_pos.x,comb_set561_2_pos.y,fac*...
    set561_2_warp_error_x,fac*set561_2_warp_error_y,0,'r');
axis ij
set(gca,'fontsize',ax_fs)
xlabel('x axis [pixel]','fontsize',la_fs)
ylabel('y axis [pixel]','fontsize',la_fs)
title(['561 to 647, Order ' num2str(polyorder_R2L) ' poly. warp (self),'...
    num2str(fac) 'x mag. residuals'],'fontsize',ti_fs)
hold off
xlim([-10 640*scale]); ylim([-20 640*scale])

fac = 20;
subplot(2,3,4)
hold on
plot(comb_set488_2_pos.x,comb_set488_2_pos.y,'g.')
quiver(comb_set488_2_pos.x,comb_set488_2_pos.y,fac*...
    set488_2_warp_error_x,fac*set488_2_warp_error_y,0,'r');
axis ij
set(gca,'fontsize',ax_fs)
xlabel('x axis [pixel]','fontsize',la_fs)
ylabel('y axis [pixel]','fontsize',la_fs)
title(['488 to 647, Order ' num2str(polyorder_R2L) ...
    ' poly. warp (self), ' num2str(fac) ...
    'x mag. residuals'],'fontsize',ti_fs)
hold off
xlim([-10 640*scale]); ylim([-20 640*scale])

fac = 20;
%fac = 2;
subplot(2,3,3)
hold on
plot(comb_set750_2_pos.x,comb_set750_2_pos.y,'g.')
quiver(comb_set750_2_pos.x,comb_set750_2_pos.y,fac*...
    set750_2_orig_error_x,fac*set750_2_orig_error_y,0,'r');
axis ij
set(gca,'fontsize',ax_fs)
xlabel('x axis [pixel]','fontsize',la_fs)
ylabel('y axis [pixel]','fontsize',la_fs)
title(['750 to 647, no warping ' num2str(fac) 'x mag. residuals' ],...
    'fontsize',ti_fs)
hold off
xlim([-10 640*scale]); ylim([-20 640*scale])
fac = 20;

subplot(2,3,6)
hold on
plot(comb_set750_2_pos.x,comb_set750_2_pos.y,'g.')
quiver(comb_set750_2_pos.x,comb_set750_2_pos.y,fac*...
    set750_2_warp_error_x,fac*set750_2_warp_error_y,0,'r');
axis ij
set(gca,'fontsize',ax_fs)
xlabel('x axis [pixel]','fontsize',la_fs)
ylabel('y axis [pixel]','fontsize',la_fs)
title(['750 to 647, Order ' num2str(polyorder_R2L) ...
    ' poly. warp (self), ' num2str(fac) ...
    'x mag. residuals'],'fontsize',ti_fs)
hold off
xlim([-10 640*scale]); ylim([-20 640*scale])

end

% save out beadmap figures
saveas(gcf,[save_pth 'BeadMap_for_registration_self.tif'],'tif')
saveas(gcf,[save_pth 'BeadMap_for_registration_self.fig'],'fig')

% plot total offsets for warping
figure(2); clf
set(gcf,'position',[493 441 1312 1082])
if numbeadmov>1

subplot(1,3,2)
cdfplot(nm_per_pix*sqrt(set561_2_warp_error_x.^2 + ...
    set561_2_warp_error_y.^2))
set(gca,'fontsize',ax_fs)
xlabel('distance error [nm]','fontsize',la_fs)
ylabel('cumulative probability','fontsize',la_fs)
title({'Cumulative distribution self-warping 561 to 647'; ...
    ['STD=' num2str(std_total561_warp_error*nm_per_pix,'%0.1f') 'nm']; ...
    ['90% of 561 beads aligned to ' num2str(cdf90_561) 'nm']} ,...
    'fontsize',la_fs)
subplot(1,3,1)
cdfplot(nm_per_pix*sqrt(set488_2_warp_error_x.^2 + ...
    set488_2_warp_error_y.^2))
set(gca,'fontsize',ax_fs)
xlabel('distance error [nm]','fontsize',la_fs)
ylabel('cumulative probability','fontsize',la_fs)
title({'Cumulative distribution self-warping 488 to 647'; ...
    ['STD=' num2str(std_total488_warp_error*nm_per_pix,'%0.1f') 'nm'];...
    ['90% of 488 beads aligned to ' num2str(cdf90_488) 'nm']} ,...
    'fontsize',la_fs)

subplot(1,3,3)
cdfplot(nm_per_pix*sqrt(set750_2_warp_error_x.^2 + ...
    set750_2_warp_error_y.^2))
set(gca,'fontsize',ax_fs)
xlabel('distance error [nm]','fontsize',la_fs)
ylabel('cumulative probability','fontsize',la_fs)
title({'Cumulative distribution self-warping 750 to 647'; ...
    ['STD=' num2str(std_total750_warp_error*nm_per_pix,'%0.1f') 'nm'];...
    ['90% of 750 beads aligned to ' num2str(cdf90_750) 'nm']} ,...
    'fontsize',la_fs)
end

% save out probability distribution alignment figures
saveas(gcf,...
    [save_pth 'Cumulative_distribution_for_registration_self.fig'],'fig')
saveas(gcf,...
    [save_pth 'Cumulative_distribution_for_registration_self.tif'],'tif')
end