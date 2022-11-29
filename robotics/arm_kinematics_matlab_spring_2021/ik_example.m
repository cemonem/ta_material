d = 2.5;
line_trajectory = [-2 3 0.5 4];
%samples = 2;
samples = 5;
%samples = 10;
%animation would be too slow after this point! Try plotting by other means
%sample = 100;
%sample = 1000;
%%
solns = ik_2link_arm(d, 1, 1)
%%
[theta_1s, theta_2s] = line_ik_2link_arm(d,line_trajectory, samples)
%%
animate_line_ik_2link_arm(d,theta_1s, theta_2s, line_trajectory)
%%