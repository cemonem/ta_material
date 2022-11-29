function [x,y,theta,t] = draw_arc(pose1,position2)
%DRAW_ARC returns points for drawing the arc of the robot. uses
%local_planner. x,y,theta,t are all in global coordinates.

[exists, to_right, r_icr, t_final,] = local_planner(pose1, position2);

if ~exists
    x = [];
    y = [];
    t = [];
    theta = [];
    return
end

t = linspace(0,t_final,20);
if to_right
    x = r_icr+r_icr*cos(-1/r_icr*t+pi);
    y = r_icr*sin(-1/r_icr*t+pi);
else
    x = -r_icr+r_icr*cos(1/r_icr*t);
    y = r_icr*sin(1/r_icr*t);
end

body_coords = [x;y;ones(1,length(y))];
global_coords = transl2(pose1(1),pose1(2))*trot2(pose1(3))*body_coords;
x = global_coords(1,:);
y = global_coords(2,:);
if ~to_right
    theta = mod(t*1/r_icr,2*pi)+pose1(3);
else
    theta = mod(-t*1/r_icr,2*pi)+pose1(3);
end