function [exists, to_right, r_icr, t_final] = local_planner(pose1, position2)
%LOCAL PLANNER calculates a circular arc toward position2 from pose1 in body
% coordinates.
% pose1 is a 3x1 array with [x y theta]' x,y are global coordinates of the
% robot and theta is the orientation
% position to is a 2x1 array with [x y]', x,y are the goal position in
% global frame.
%
% Let position2_body be the coordinates of position2 in body frame.
%
% the arc (in body coordinates) is in the following format if position2 is 
% to the right of pose1 (to_right parameter is true)
% x(t) = r_icr+r_icr*cos(-1/r_icr*t+pi), x(t_final) = position2_body(1)
% y(t) = sin(-1/r_icr*t+pi), y(t_final) = position2_body(2)
%
% 
% the arc (in body coordinates) is in the following format if position2 is 
% to the left of pose1 (to_right parameter is false)
% x(t) = -r_icr+r_icr*cos(1/r_icr*t), x(t_final) = position2_body(1)
% y(t) = sin(1/r_icr*t), y(t_final) = position2_body(2)
%
% exists is returned false if position2_body(2) <= 0 (represents whether
% solution exists or not)
%
% to_right ,r_icr, t_final are returned following the rules above.
%

% your implementation here

end