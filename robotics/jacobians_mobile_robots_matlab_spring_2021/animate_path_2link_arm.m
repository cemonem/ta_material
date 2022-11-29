function [] = animate_path_2link_arm(d, theta_1s, theta_2s, path, t)
%ANIMATE_PATH_2LINK_ARM Animate path drawing task with jacobians
%   d is the length of a single link
%   t is the real time at each step as an nx1 array
%   theta_1s, theta_2s are the angle values corresponding to each t (as nx1
%   arrays)
%   path is the trajectory end effector is supposed to follow,
%   a 2xn array, each row [x,y] corresponding to each t

XLIM = [-3 3];
YLIM = [-1 5];

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
goal_trajectory = line(ax, path(:,1), path(:,2),'DisplayName', 'goal trajectory','LineStyle',':','Marker','x','Color','black','LineWidth',1);


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