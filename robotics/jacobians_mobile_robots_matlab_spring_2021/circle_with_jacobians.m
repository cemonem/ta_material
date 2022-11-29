function [t, theta_1s, theta_2s, theta_1dots, theta_2dots] = circle_with_jacobians(d, x_center, y_center, r, ode45options)
%CIRCLE_WITH_JACOBIANS integrate a circle path of the end
%effector with the jacobian and ode45 solver
%   Integrates a circle path starting and ending at x_center+r,y_center
%   with 1m/s end effector speed.
%   d is the length of a single link
%   ode45options is the odeset object that is supplied to ode45.
%   t is the time instances ode45 returns in the size nx1
%   the other values correspond to these instances.
%   if the line trajectory cannot be drawn by the robot, all of them should
%   be empty array.

t = [];
theta_1s = [];
theta_2s = [];
theta_1dots = [];
theta_2dots = [];

end