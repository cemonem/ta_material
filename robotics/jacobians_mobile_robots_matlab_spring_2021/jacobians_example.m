d = 2.5;
line_trajectory = [-2 3 0.5 4];
%%
ode45options = odeset();
%ode45options = odeset('MaxStep',3,'AbsTol',1);
[t, theta_1s, theta_2s, theta_1dots, theta_2dots]= line_segment_with_jacobians(d, line_trajectory,ode45options);
%%
line_length = (line_trajectory(2)-line_trajectory(1))^2+...
    (line_trajectory(4)-line_trajectory(3))^2;
line_length = sqrt(line_length);

line_xdot = (line_trajectory(2)-line_trajectory(1))/line_length;
line_ydot = (line_trajectory(4)-line_trajectory(3))/line_length;

path = [line_trajectory(1)+t*line_xdot line_trajectory(3)+t*line_ydot];
animate_path_2link_arm(d,theta_1s, theta_2s, path,t);
%%
r = 1;
x_center = 0;
y_center = 3.99;
%%
ode45options = odeset();
[t, theta_1s, theta_2s, theta_1dots, theta_2dots]= circle_with_jacobians(d, x_center, y_center, r, ode45options);
%%
path = [x_center+r*cos(1/r*t) y_center+r*sin(1/r*t)];
animate_path_2link_arm(d,theta_1s, theta_2s, path,t);
%%
% set(gcf,'Units','inches');
% screenposition = get(gcf,'Position');
% set(gcf,...
%     'PaperPosition',[0 0 screenposition(3:4)],...
%     'PaperSize',[screenposition(3:4)]);
% print(gcf,'sneak_peek','-dpdf','-r0')
