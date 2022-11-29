function [t, theta_1s, theta_2s, theta_1dots, theta_2dots] = line_segment_with_jacobians(d, line_trajectory, ode45options)
%LINE_SEGMENT_WITH_JACOBIANS integrate a line segment path of the end
%effector with the jacobian and ode45 solver
%   integrates a line segment path with 1m/s end effector speed.
%   d is the length of a single link
%   line_trajectory is the line the robot is supposed to draw between
%   (x_1,y_1), (x_2,y_2). It is a 1x4 array of the form [x_1 x_2 y_1 y_2]
%   ode45options is the odeset object that is supplied to ode45.
%   t is the time instances ode45 returns in the size nx1
%   the other values correspond to these instances.
%   if the line trajectory cannot be drawn by the robot, all of them should
%   be empty array.

% calculate initial values from x_1 y_1

% theta_1_init, theta_2_init = something??(x_1,y_1);

theta_1_init = 0;
theta_2_init = 0;
theta_init = [theta_1_init theta_2_init];

% assuming 1m/s end effector speed, find the time span
length = (line_trajectory(2)-line_trajectory(1))^2+...
    (line_trajectory(4)-line_trajectory(3))^2;
length = sqrt(length);

tspan = [0 length];

function [current_thetasdot] = odefun(t,current_thetas)
    % use the inverse of jacobian, and end effector velocities here in
    % addition to current_thetas
    % is t necessary? :)
    current_thetasdot = 0;
end

[t, thetas] = ode45(@odefun,tspan,theta_init,ode45options);

theta_1s = thetas(:,1);
theta_2s = thetas(:,2);

% calculate these outside of ode45
theta_1dots = [];
theta_2dots = [];

end