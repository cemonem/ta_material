function [theta_1s, theta_2s] = line_ik_2link_arm(d, line_trajectory, samples)
%LINE_IK_2LINK_ARM calculate IK for a line.
%   Calculates IK solutions for the points linearly interpolating line
%   parametrized by line_trajectory.
%   line_trajectory is the line the robot is supposed to draw between
%   (x_1,y_1), (x_2,y_2). It is a 1x4 array of the form [x_1 x_2 y_1 y_2]
%   samples are the number of samples, containing (x_1,y_1) and
%   (x_2,y_2) as the first and last sample.
%   d is the length of a single link.
%   theta_1s theta_2s are samples x 1 arrays, visually defined in Figure 1
%   of the hw text. If a sampled point on the line does not have an IK
%   solution, theta_1s and theta_2s are empty arrays.
%   The theta_1s, theta_2s values should be smooth, the elbow orientation
%   with respect to goal point (up or down) should not abruptly change.


% these are the points you need to calculate IK for.
tool_xs = linspace(line_trajectory(1), line_trajectory(2), samples);
tool_ys = linspace(line_trajectory(3), line_trajectory(4), samples);

theta_1s = [];
theta_2s = [];
end



