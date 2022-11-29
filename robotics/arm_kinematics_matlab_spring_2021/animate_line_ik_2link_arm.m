function [] = animate_line_ik_2link_arm(d, theta_1s, theta_2s, line_trajectory)
%ANIMATE_LINE_IK_2LINK_ARM Animate line drawing task with sampled IK
%   d is the length of a single link
%   theta_1s, theta_2s are the solutions of n linearly interpolated samples
%   taken from the line parametrized by line_trajectory. theta_1s theta_2s
%   are nx1 arrays, visually defined in Figure 1 of the hw text.
%   line_trajectory is the line the robot is supposed to draw between
%   (x_1,y_1), (x_2,y_2). It is a 1x4 array of the form [x_1 x_2 y_1 y_2]

XLIM = [-3 3];
YLIM = [-1 5];
SUBSAMPLES = 10;

line_pts_x = linspace(line_trajectory(1), line_trajectory(2), length(theta_1s));
line_pts_y = linspace(line_trajectory(3), line_trajectory(4), length(theta_1s));

theta_1s = subsample(theta_1s, SUBSAMPLES);
theta_2s = subsample(theta_2s, SUBSAMPLES);

x1 = cos(theta_1s).*d;
y1 = sin(theta_1s).*d;
x2 = x1 + cos(theta_1s+theta_2s).*d;
y2 = y1 + sin(theta_1s+theta_2s).*d;

clf;
set(gcf,'Position',[200 200 500 500]);
ax = gca;
axis equal;
xlabel(ax,'x(m)');
ylabel(ax,'y(m)')
xlim(ax, XLIM);
ylim(ax, YLIM);

end_effector_x = [x2(1)];
end_effector_y = [y2(1)];
end_effector = line(ax, end_effector_x, end_effector_y, 'DisplayName', 'actual trajectory');
goal_trajectory = line(ax, line_pts_x, line_pts_y, 'DisplayName', 'goal trajectory','Marker','x','Color','black','LineWidth',2);


link1 = line(ax, [0 x1(1)], [0 y1(1)], 'Color', 'cyan', 'LineWidth', 3,'Marker','.','MarkerSize',20, 'HandleVisibility','off');
link2 = line(ax, [x1(1) x2(1)], [y1(1) y2(1)], 'Color', '#FFA500', 'LineWidth', 3,'Marker','.','MarkerSize',20, 'HandleVisibility','off');

legend('show');

for i = 2:length(x1)
    set(link1, 'XData', [0 x1(i)]);
    set(link1, 'YData', [0 y1(i)]);
    set(link2, 'XData', [x1(i) x2(i)]);
    set(link2, 'YData', [y1(i) y2(i)]);
    end_effector_x = [end_effector_x; x2(i)];
    end_effector_y = [end_effector_y; y2(i)];
    set(end_effector, 'XData', end_effector_x);
    set(end_effector, 'YData', end_effector_y);
    drawnow;
    pause(0.1);
end

end

function [result] = subsample(arr, n)
    result = [];
    for i = 1:length(arr)-1
        result = [result;linspace(arr(i),arr(i+1),n)'];
    end
end
