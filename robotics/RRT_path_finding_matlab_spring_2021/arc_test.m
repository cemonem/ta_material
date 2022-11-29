pose1 = [2,3,pi/3];

[pose2s_x,pose2s_y] = ndgrid(0:0.5:5,0:0.5:5);
pose2s = [pose2s_x(:) pose2s_y(:)]';
%%
clf;
ax=gca();
hold(ax,'on');
plot_robot(ax,pose1,'r',0.3)
for pose2 = pose2s
    [x,y,theta,t] = draw_arc(pose1,pose2);
    if isempty(x)
        plot(ax,pose2(1),pose2(2),'.','Color','red')
        continue
    end
    plot(ax,x,y,'Color','blue');
    plot(ax,pose2(1),pose2(2),'.','Color','black')
    plot_robot(ax,[x(end) y(end) theta(end)],'none',0.3);

end
axis(ax,'equal')
xlim(ax,[-0.5 5.5]);
ylim(ax,[-0.5 5.5]);
xlabel(ax,'x (m)');
ylabel(ax,'y (m)');
%%
% set(gcf,'Units','inches');
% screenposition = get(gcf,'Position');
% set(gcf,...
%     'PaperPosition',[0 0 screenposition(3:4)],...
%     'PaperSize',[screenposition(3:4)]);
% print(gcf,'arcs','-dpdf','-r0');
